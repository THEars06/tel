#!/usr/bin/env python3
"""
🔥 NEUALHELPPASS - Tek Seferde Android APK Oluşturucu
Google Colab'da bu kodu tek bir hücrede çalıştırın!
"""

SINGLE_CELL_CODE = '''
# 🔥 NEUALHELPPASS Android APK - Tek Adımda Oluştur
print("🚀 NEUALHELPPASS Android APK oluşturuluyor...")

# 1. Sistem hazırlığı
!apt update > /dev/null 2>&1
!apt install -y python3-pip git zip unzip default-jdk > /dev/null 2>&1
!pip install buildozer cython > /dev/null 2>&1

# 2. Android SDK
!wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
!unzip -q commandlinetools-linux-8512546_latest.zip
!mkdir -p /opt/android-sdk/cmdline-tools
!mv cmdline-tools /opt/android-sdk/cmdline-tools/latest

import os
os.environ['ANDROID_HOME'] = '/opt/android-sdk'
os.environ['PATH'] = os.environ['PATH'] + ':/opt/android-sdk/cmdline-tools/latest/bin'

# 3. Proje klasörü
!mkdir -p /content/neualhelppass/app
%cd /content/neualhelppass/app

# 4. Ana uygulama dosyası
with open('main.py', 'w', encoding='utf-8') as f:
    f.write("""
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Arka plan
        with self.canvas.before:
            Color(0.29, 0.14, 0.59, 1)  # Mor renk
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Başlık
        title = Label(
            text='NEUALHELPPASS\\n\\nKıbrıs Güvenlik\\nUygulaması',
            font_size='28sp',
            halign='center',
            color=(1, 1, 1, 1),
            text_size=(None, None)
        )
        
        # Butonlar
        face_btn = Button(
            text='🔍 Yüz Analizi',
            size_hint_y=None,
            height='60dp',
            font_size='18sp',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        score_btn = Button(
            text='⭐ Güvenlik Puanı',
            size_hint_y=None,
            height='60dp',
            font_size='18sp',
            background_color=(1, 0.6, 0, 1)
        )
        
        map_btn = Button(
            text='🗺️ Güvenlik Haritası',
            size_hint_y=None,
            height='60dp',
            font_size='18sp',
            background_color=(0.2, 0.6, 1, 1)
        )
        
        emergency_btn = Button(
            text='🚨 ACİL DURUM',
            size_hint_y=None,
            height='60dp',
            font_size='20sp',
            background_color=(1, 0.2, 0.2, 1)
        )
        
        layout.add_widget(title)
        layout.add_widget(face_btn)
        layout.add_widget(score_btn)
        layout.add_widget(map_btn)
        layout.add_widget(emergency_btn)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class NEUALHELPPASSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    NEUALHELPPASSApp().run()
""")

# 5. Buildozer konfigürasyonu
with open('buildozer.spec', 'w', encoding='utf-8') as f:
    f.write("""[app]
title = NEUALHELPPASS
package.name = neualhelppass
package.domain = org.neualhelppass
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET,CAMERA,SEND_SMS,CALL_PHONE,ACCESS_FINE_LOCATION
android.api = 31
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
""")

print("✅ Dosyalar hazırlandı, APK oluşturuluyor...")

# 6. APK oluştur
!buildozer android debug

# 7. APK'yı indir
from google.colab import files
import glob

apk_files = glob.glob("bin/*.apk")
if apk_files:
    print(f"🎉 APK başarıyla oluşturuldu: {apk_files[0]}")
    files.download(apk_files[0])
    print("📱 APK dosyası bilgisayarınıza indirildi!")
    print("🔧 Android cihazınızda 'Bilinmeyen kaynaklar'ı etkinleştirin")
    print("📲 APK'yı Android cihazınıza aktarın ve kurun")
else:
    print("❌ APK oluşturulamadı, hata kontrolü:")
    !ls -la bin/
    
print("🏁 İşlem tamamlandı!")
'''

print("📱 NEUALHELPPASS Android APK - Süper Basit Yöntem")
print("=" * 55)
print()
print("🔥 Google Colab'da BU KODU TEK BİR HÜCREDE ÇALIŞTIRIN:")
print()
print(SINGLE_CELL_CODE)
print()
print("⚡ ADIMLAR:")
print("1. https://colab.research.google.com adresine git")
print("2. 'New notebook' tıkla")
print("3. Yukarıdaki UZUN kodu kopyala-yapıştır")
print("4. Ctrl+Enter bas ve bekle (5-10 dakika)")
print("5. APK dosyasını indir ve Android'e kur!")
print()
print("🎯 Bu kadar basit!") 