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

# ------------------------------
# CRITICAL FIX FOR GITHUB BUILDS
# ------------------------------
android.sdk_path = $ANDROIDSDK
android.ndk_path = $ANDROIDNDK

# NDK version
android.ndk = 25b

# Java / Gradle
android.gradle_version = 7.5

# Backup
android.allow_backup = True

# Build formats
android.release_artifact = aab
android.debug_artifact = apk

# Icons (optional)
# icon.filename = icon.png
# presplash.filename = presplash.png


[buildozer]
log_level = 2
warn_on_root = 1
