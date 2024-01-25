# Chromium Media Player

Use Chrome and a ![media-player](https://github.com/inbasic/media-player) extension to play local videos.

It can be set as the default video file opener, just like you would use other Windows desktop software: double-click to open a local video file in Chrome.

![图片](https://github.com/puff-dayo/Chromium-Media-Player/assets/84665734/087e95eb-1bf9-4251-aea5-c14484f1a4ac)

## Why?

Because NVIDIA release ![RTX Video HDR](https://www.nvidia.com/en-us/geforce/news/geforce-rtx-4070-ti-super-rtx-video-hdr-game-ready-driver/), a new AI-enhanced HDR feature to all GeForce RTX GPUs, instantly converting any Standard Dynamic Range (SDR) video playing in select internet browsers into vibrant High Dynamic Range (HDR).

Sadly, RTX Video HDR and RTX Video Super Resolution work only on Chromium-based browsers such as Google Chrome or Microsoft Edge.

This is why I wrote this program.

## How to Use

Simply download the `ChromiumMediaPlayer.exe` from Release, and run it to configure.

In Windows Explorer, right-click -> choose Open With -> navigate to the folder where `ChromiumMediaPlayer.exe` is located, and choose to open with it or set it as the default.

(Set the browser path manually for other Chromium browsers. (Only tested on Windows 11 21H2, Chrome 120))

Read https://webextension.org/listing/the-media-player.html for keyboard shortcuts and other usage FAQs.

## How to Compile

Install Python 3.10 and nuitka, and run 
`nuitka --windows-icon-from-ico=icon-256.ico --output-filename=ChromiumVideoPlayer.exe --standalone main.py` .

No other package is required.

## How it Works

Local files are served as local http server.

Huge thanks to devs of the ![media-player](https://github.com/inbasic/media-player) extension!
