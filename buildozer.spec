[app]

# App details
title = SafeSpot
package.name = safespot
package.domain = com.bradleycorbettjones.safespot
version = 1.0

# Source and files
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Dependencies
requirements = python3,kivy

# Orientation / fullscreen
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET

# Android API + Build Tools
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2

# Architectures
android.archs = armeabi-v7a, arm64-v8a

# NDK (required!)
android.ndk = 25b
android.ndk_path = /usr/local/android-ndk-r25b

# Java version
android.gradle_dependencies = 
android.gradle_version = 7.5

# Enable backup
android.allow_backup = True

# Build formats
android.release_artifact = aab
android.debug_artifact = apk

# Icon + presplash (optional)
# icon.filename = icon.png
# presplash.filename = presplash.png


[buildozer]

log_level = 2
warn_on_root = 1
