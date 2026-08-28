[app]

title = Video Downloader
package.name = videodownloader
package.domain = org.kiarash

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 0.1

requirements = python3,kivy,yt-dlp

orientation = portrait
fullscreen = 0

android.permissions = android.permission.INTERNET

android.debug_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1