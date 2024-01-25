import sys
import os
import socketserver
import subprocess
import threading
from http import server
from subprocess import run as run_cmd
from webbrowser import open as web_open
from configparser import ConfigParser
from string import ascii_uppercase
import urllib.request
import urllib.parse

port = 37639


def change_working_directory():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(f"Changed working directory to: {os.getcwd()}")


change_working_directory()


def print_current_working_directory():
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")


print_current_working_directory()



def read_settings():
    config = ConfigParser()
    config.read('settings.ini')
    return config


def write_settings(config):
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)


def install_video_player():
    url = "https://chromewebstore.google.com/detail/media-player/mgmhnaapafpejpkhdhijgkljhpcpecpj"
    web_open(url)


def configure_browser_path():
    browser_path = input("Input chrome.exe path: ")
    config = read_settings()
    config['Settings'] = {'browserlocation': browser_path}
    write_settings(config)
    print("Updated chrome.exe path.")


def check_browser_path():
    config = read_settings()

    browser_path = config.get('Settings', 'browserlocation', fallback=None)
    if browser_path and os.path.isfile(browser_path):
        print(f"Status: Browser detected at {browser_path}.")
        return

    chrome_relative_path = "Program Files\\Google\\Chrome\\Application\\chrome.exe"
    for drive in ascii_uppercase:
        potential_path = f"{drive}:\\{chrome_relative_path}"
        if os.path.isfile(potential_path):
            print(f"Status: Browser detected at {potential_path}.")
            config['Settings']['browserlocation'] = potential_path
            write_settings(config)
            return

    print("Status: Browser NOT detected.")


def add_file_association():
    try:
        run_cmd("start ms-settings:defaultapps", shell=True)
    except Exception as e:
        print(f"Error: {e}")


def path_to_file_url(file_path):
    absolute_path = os.path.abspath(file_path)
    file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(absolute_path))
    return file_url



def open_with_browser(file_path):
    file_name = os.path.basename(file_path)
    file_directory = os.path.dirname(file_path)

    class CustomHTTPRequestHandler(server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=file_directory, **kwargs)

    def run_server():
        with socketserver.TCPServer(("127.0.0.1", port), CustomHTTPRequestHandler) as httpd:
            print(f"Serving at port {port}")
            httpd.serve_forever()

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    config = read_settings()
    browser_location = config['Settings']['browserlocation']
    print(f"Opening {file_path}")
    encoded_file_name = urllib.parse.quote(file_name)
    url = f"http://127.0.0.1:{port}/{encoded_file_name}"

    command = f'"{browser_location}" --app=chrome-extension://mgmhnaapafpejpkhdhijgkljhpcpecpj/data/player/index.html?src="{url}"'
    subprocess.run(command)
    input("Press Enter to exit...")


def main_menu():
    print("""
    Chromium Media Player - Version 1.0
    
    Useful information:
     -     Shortcut to turn on/off HDR: Win+Alt+B
     -  AI-HDR required driver version: 551.23 (24 Jan, 2024)
     -        Media-player github repo: https://github.com/inbasic/media-player/
     -    Keyboard shortcuts in player: https://webextension.org/listing/the-media-player.html
     
    Options:
      1. Install Media Player Extension
      2. Manually Configure chrome.exe Path
      3. Open MS Default-app Settings
      0. Finish Configuration
    """)
    check_browser_path()
    print("Input an option number：")


def main():
    not_close = True
    while not_close:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            open_with_browser(file_path)
            not_close = False
        else:
            main_menu()
            choice = input()
            if choice == '1':
                install_video_player()
            elif choice == '2':
                configure_browser_path()
            elif choice == '3':
                add_file_association()
            elif choice == '0':
                not_close = False
            else:
                print("Invalid option number.")


if __name__ == "__main__":
    try:
        main()
    finally:
        pass
