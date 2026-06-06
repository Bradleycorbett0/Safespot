name: Build SafeSpot APK

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install Linux packages
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git zip unzip tar wget curl \
            build-essential \
            clang lld \
            libffi-dev libssl-dev \
            autoconf automake libtool pkg-config \
            zlib1g-dev libncurses5-dev

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3
        with:
          packages: 'platforms;android-33 build-tools;33.0.2 platform-tools ndk;25.2.9519653 cmdline-tools;latest'
          accept-android-sdk-licenses: true

      - name: Link Android SDK to Buildozer
        run: |
          mkdir -p ~/.buildozer/android/platform
          ln -sf $ANDROID_SDK_ROOT ~/.buildozer/android/platform/android-sdk

      - name: Verify AIDL installation
        run: |
          find $ANDROID_SDK_ROOT/build-tools -name "aidl" -type f
          ls -la $ANDROID_SDK_ROOT/build-tools/33.0.2/ | grep aidl || echo "AIDL check"

      - name: Hard clean old build
        run: |
          rm -rf bin
          rm -rf ~/.gradle/caches
          rm -rf ~/.cache/pip

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install cython==0.29.36
          python -m pip install buildozer==1.5.0

      - name: Show Buildozer config
        run: |
          cat buildozer.spec
          grep -n "requirements" buildozer.spec || true
          grep -n "p4a.branch" buildozer.spec || true

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: SafeSpot-APK
          path: bin/*.apk
