# Live Beat Monitor

An assistant for live performances with backing tracks.

## Download

You can download LiveBeatMonitor compiled application from the [latest release](https://github.com/ivbignal/live-beat-monitor/releases/latest/) here:

[![Mac Icon]][Mac Link] 
[![Win Icon]][Win Link] 
[![Lin Icon]][Lin Link] 

## How to use

Create show folder, which will contain all your tracks. Note that name of this folder will be interpreted as show name.

Use track names to configure them. Available extensions:
- `.mp3` `.wav` - TRACK types, follow this naming pattern: `<position>-<title>-<bpm>-<counter_delay>`; eg. `1-Intro-80.50-00.50.wav`.
- `.md` - TEXT types, write some side help text in markdown format to show in Perform mode.

Open a show folder in LiveBeatMonitor (ignore errors if present - they tell you about files that weren't able to process).

Navigate using arrow keys or `PgUp`/`PgDown`, hit `space` to play/pause, hit `enter` to stop and reset to beginning.

Use `Perform mode` button to toggle fullscreen window which you can place on the on-stage separate monitor or leave on main monitor of your laptop if you planning to place it in front of yout band on stage.

Use `[` and `]` to change font scale of text track.

Use `Esc` to toggle Perform mode.

Use `o` key to dive into open show folder selection dialog.

<!---------------------------------------------------------------------------->

[Mac Icon]: https://img.shields.io/badge/MacOS_app-2b2b2b?style=for-the-badge&logoColor=white&logo=Apple
[Mac Link]: https://github.com/ivbignal/live-beat-monitor/releases/latest/download/LiveBeatMonitor_mac.tar.gz 'Download MacOS App'

[Win Icon]: https://img.shields.io/badge/Windows_app-0061ff?style=for-the-badge&logoColor=white&logo=Windows
[Win Link]: https://github.com/ivbignal/live-beat-monitor/releases/latest/download/LiveBeatMonitor_win.zip 'Download MacOS App'

[Lin Icon]: https://img.shields.io/badge/Linux_app-F02020?style=for-the-badge&logoColor=white&logo=Linux
[Lin Link]: https://github.com/ivbignal/live-beat-monitor/releases/latest/download/LiveBeatMonitor_linux.tar.gz 'Download MacOS App'
