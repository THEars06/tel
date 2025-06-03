#!/usr/bin/env python3
"""
NEUALHELPPASS Android APK Builder
Google Colab'da çalıştırılmak üzere tasarlanmıştır
"""

COLAB_SETUP_CODE = '''
# Google Colab'da çalıştırın:

# 1. Gerekli paketleri kurun
!apt update
!apt install -y python3-pip git zip unzip default-jdk
!pip install buildozer cython

# 2. Android SDK kurulumu
!wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
!unzip commandlinetools-linux-8512546_latest.zip
!mkdir -p /opt/android-sdk/cmdline-tools
!mv cmdline-tools /opt/android-sdk/cmdline-tools/latest
!export ANDROID_HOME=/opt/android-sdk
!export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# 3. Projeyi yükleyin
!git clone https://github.com/kullanici/NEUALHELPPASS.git
!cd NEUALHELPPASS/app

# 4. APK oluşturun
!buildozer android debug

# 5. APK'yı indirin
from google.colab import files
files.download('/content/NEUALHELPPASS/app/bin/neualhelppass-1.0-debug.apk')
'''

GITHUB_ACTION_YML = '''
# .github/workflows/build_android.yml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y default-jdk
        pip install buildozer cython
    
    - name: Build APK
      run: |
        cd app
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: neualhelppass-apk
        path: app/bin/*.apk
'''

print("🏗️ NEUALHELPPASS Android APK Oluşturma Kılavuzu")
print("=" * 50)
print()
print("📱 Buildozer Windows'ta çalışmaz. Alternatif yöntemler:")
print()
print("1️⃣ GOOGLE COLAB (Önerilen):")
print("   - Google Colab'a gidin: https://colab.research.google.com")
print("   - Yeni notebook oluşturun")
print("   - Aşağıdaki kodu çalıştırın:")
print()
print(COLAB_SETUP_CODE)
print()
print("2️⃣ GITHUB ACTIONS:")
print("   - GitHub repo'ya .github/workflows/build_android.yml ekleyin:")
print()
print(GITHUB_ACTION_YML)
print()
print("3️⃣ LINUX VIRTüAL MACHINE:")
print("   - VirtualBox ile Ubuntu kurun")
print("   - Buildozer'ı Ubuntu'da çalıştırın")
print()
print("4️⃣ WSL2 (Windows Subsystem for Linux):")
print("   - WSL2 Ubuntu kurun")
print("   - Linux ortamında buildozer çalıştırın")
print()
print("✅ En kolay yöntem Google Colab'dır!") 