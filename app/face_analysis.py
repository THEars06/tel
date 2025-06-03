import os
import cv2
import numpy as np
import time
import random

# TensorFlow'u güvenli şekilde import et
try:
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True
    print("✅ TensorFlow başarıyla yüklendi")
except ImportError as e:
    print(f"⚠️ TensorFlow bulunamadı: {e}")
    print("🔄 Test modu etkinleştiriliyor...")
    TENSORFLOW_AVAILABLE = False
    load_model = None

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

# Android işlemleri için (manuel butonlar için)
from plyer import sms, call

# 📍 Dosya yolları
BASE_DIR     = os.path.dirname(__file__)
MODEL_PATH   = os.path.join(BASE_DIR, 'models', 'emotion_model.h5')
CASCADE_PATH = os.path.join(BASE_DIR, 'data', 'haarcascade_frontalface_default.xml')

# 😶‍🌫️ Duygu etiketleri (modelinize göre ayarlayın)
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# 🎯 Yüklemeler (Error handling ile)
try:
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if TENSORFLOW_AVAILABLE and load_model:
        emotion_model = load_model(MODEL_PATH, compile=False)
        print("✅ Model ve cascade dosyaları yüklendi")
    else:
        emotion_model = None
        print("⚠️ TensorFlow mevcut değil - test modu aktif")
except Exception as e:
    print(f"❌ Model yükleme hatası: {e}")
    face_cascade = None
    emotion_model = None

def analyze_face(image_path: str) -> int:
    """📊 Analiz kısmı (Android uyumlu geliştirilmiş sürüm)"""
    try:
        # Model kontrolü
        if face_cascade is None or not TENSORFLOW_AVAILABLE or emotion_model is None:
            print("❌ Model dosyaları yüklenemedi veya TensorFlow mevcut değil - test modu")
            # Test için rastgele ama güvenli bir değer döndür
            test_value = random.randint(20, 40)
            print(f"🎲 Test değeri: {test_value}")
            return test_value
        
        img = cv2.imread(image_path)
        if img is None:
            print("❌ Görüntü okunamadı.")
            return 25  # Güvenli değer

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print("😐 Yüz algılanamadı.")
            return 25  # Güvenli değer

        x, y, w, h = faces[0]
        roi = gray[y:y + h, x:x + w]
        roi = cv2.resize(roi, (64, 64)).astype("float32") / 255.0
        roi = np.expand_dims(roi, axis=0)       # (1, 64, 64)
        roi = np.expand_dims(roi, axis=-1)      # (1, 64, 64, 1)

        preds = emotion_model.predict(roi)[0]
        fear = float(preds[EMOTIONS.index("fear")])
        sad = float(preds[EMOTIONS.index("sad")])
        hazard = int((fear + sad) * 100)

        print(f"→ Fear: {fear:.2f}, Sad: {sad:.2f}, Hazard: %{hazard}")
        return hazard
        
    except Exception as e:
        print(f"❌ Analiz hatası: {e}")
        return 25  # Güvenli değer

class FifthScreen(Screen):
    hazard_status = NumericProperty(0)
    latitude = NumericProperty(35.1856)  # Kıbrıs varsayılan koordinatları
    longitude = NumericProperty(33.3823)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam = None
        self.camera_active = False

    def on_pre_enter(self):
        """Sayfaya girerken kamerayı başlat"""
        print("🎬 Face Analysis sayfasına girildi")
        # Widget'ların tamamen yüklenmesi için gecikme
        Clock.schedule_once(lambda dt: self.start_camera_preview(), 3.0)

    def on_leave(self):
        """Sayfadan çıkarken kamerayı durdur"""
        self.stop_camera_preview()

    def start_camera_preview(self):
        """Kamera preview'ını başlat"""
        try:
            print("📹 Kamera preview başlatılıyor...")
            
            # Widget'ın hazır olduğundan emin ol
            if not hasattr(self, 'ids') or 'camera_widget' not in self.ids:
                print("⚠️ Widget henüz hazır değil, tekrar denenecek...")
                Clock.schedule_once(lambda dt: self.start_camera_preview(), 1.0)
                return
            
            # Önceki kamerayı kapat
            if self.cam:
                self.cam.release()
                
            self.cam = cv2.VideoCapture(0)
            if self.cam and self.cam.isOpened():
                # Kamera ayarları
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cam.set(cv2.CAP_PROP_FPS, 15)
                
                self.camera_active = True
                print("✅ Kamera açıldı ve yapılandırıldı")
                
                # İlk preview'ı başlat
                self.update_camera_preview()
                print("✅ Kamera preview başlatıldı")
            else:
                print("❌ Kamera açılamadı!")
                self.show_camera_placeholder()
        except Exception as e:
            print(f"⚠️ Kamera başlatma hatası: {e}")
            self.show_camera_placeholder()

    def show_camera_placeholder(self):
        """Kamera çalışmıyorsa placeholder göster"""
        try:
            if 'camera_widget' in self.ids:
                self.ids.camera_widget.clear_widgets()
                
                # Basit placeholder ekle
                from kivy.uix.label import Label
                placeholder = Label()
                placeholder.text = "📷\nKamera Yükleniyor..."
                placeholder.color = (1, 1, 1, 1)
                placeholder.font_size = '20sp'
                
                self.ids.camera_widget.add_widget(placeholder)
                print("📷 Kamera placeholder gösterildi")
        except Exception as e:
            print(f"⚠️ Placeholder hatası: {e}")

    def update_camera_preview(self):
        """Kamera görüntüsünü güncelle - tamamen yeniden yazıldı"""
        if not self.camera_active or not self.cam or not self.cam.isOpened():
            print("🔴 Kamera aktif değil, preview durduruluyor")
            return
            
        try:
            ret, frame = self.cam.read()
            if ret and frame is not None:
                # Görüntüyü işle
                frame = cv2.flip(frame, 1)  # Ayna etkisi
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Kivy texture'a çevir
                h, w = frame_rgb.shape[:2]
                texture = Texture.create(size=(w, h))
                texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                texture.flip_vertical()
                
                # Widget'a güvenli erişim - basitleştirilmiş
                camera_widget = self.ids.get('camera_widget', None)
                if camera_widget:
                    # Widget'ları temizle
                    camera_widget.clear_widgets()
                    
                    # Yeni image widget oluştur - basit ayarlarla
                    camera_image = Image()
                    camera_image.texture = texture
                    camera_image.size_hint = (1, 1)
                    
                    # Widget'ı ekle
                    camera_widget.add_widget(camera_image)
                else:
                    print("⚠️ Camera widget bulunamadı")
            
            # Sonraki frame için schedule et
            if self.camera_active:
                Clock.schedule_once(lambda dt: self.update_camera_preview(), 1.0/10.0)  # 10 FPS
                
        except Exception as e:
            print(f"⚠️ Kamera preview hatası: {e}")
            # Hata olursa tekrar dene
            if self.camera_active:
                Clock.schedule_once(lambda dt: self.update_camera_preview(), 1.0)

    def stop_camera_preview(self):
        """Kamera preview'ını durdur"""
        self.camera_active = False
        if self.cam:
            try:
                self.cam.release()
                print("🔴 Kamera kapatıldı")
            except:
                pass
            finally:
                self.cam = None
        print("🔴 Kamera preview durduruldu")

    def capture_with_opencv(self):
        """Fotoğraf çek ve analiz et"""
        print("📸 Fotoğraf çekiliyor ve analiz ediliyor...")
        
        try:
            if self.cam and self.cam.isOpened():
                # Mevcut kameradan fotoğraf çek
                ret, frame = self.cam.read()
                if ret and frame is not None:
                    # Fotoğrafı kaydet
                    app = App.get_running_app()
                    app_dir = app.user_data_dir
                    photo_path = os.path.join(app_dir, 'latest_face.jpg')
                    
                    cv2.imwrite(photo_path, frame)
                    print(f"✅ Fotoğraf kaydedildi: {photo_path}")
                    
                    # Analiz et
                    self.hazard_status = analyze_face(photo_path)
                    print(f"😨 Analiz sonucu: Tehlike seviyesi %{self.hazard_status}")
                    
                    self.handle_analysis_result()
                else:
                    print("⚠️ Kameradan görüntü alınamadı")
                    self.hazard_status = 25
                    self.handle_analysis_result()
            else:
                print("⚠️ Kamera kullanılamıyor, test modu")
                self.hazard_status = 30
                self.handle_analysis_result()
                
        except Exception as e:
            print(f"⚠️ Fotoğraf çekme hatası: {e}")
            self.hazard_status = 25
            self.handle_analysis_result()

    def handle_analysis_result(self):
        """Analiz sonucuna göre işlem yap"""
        try:
            if self.hazard_status >= 60:
                print("🚨 Acil durum! Yüzde 60 üzeri tehlike seviyesi.")
                self.trigger_emergency()
            else:
                print(f"📍 Normal durum - Kıbrıs konumu gösteriliyor: ({self.latitude}, {self.longitude})")
                Clock.schedule_once(self._center_map, 0.5)
        except Exception as e:
            print(f"❌ Sonuç işleme hatası: {e}")

    def trigger_emergency(self):
        """Acil durum tetikleme"""
        try:
            location_link = f"https://maps.google.com/?q={self.latitude},{self.longitude}"

            # SMS gönder
            try:
                sms.send(
                    recipient='112',
                    message=f"Emergency! Danger level: %{self.hazard_status}\nLocation: {location_link}"
                )
                print("📲 Acil SMS gönderildi.")
            except Exception as sms_error:
                print(f"⚠️ SMS gönderimi başarısız: {sms_error}")

            # Arama yap
            try:
                call.makecall(tel='112')
                print("📞 Acil arama başlatıldı.")
            except Exception as call_error:
                print(f"⚠️ Arama başarısız: {call_error}")

            # Acil durum ekranına geç
            App.get_running_app().root.current = "emergency"
            
        except Exception as e:
            print(f"❌ Acil durum işlemi genel hatası: {e}")

    def _center_map(self, *args):
        try:
            if 'mapview' in self.ids:
                print("🗺️ Harita Kıbrıs'a ortalanıyor...")
                self.ids.mapview.center_on(self.latitude, self.longitude)
        except Exception as e:
            print(f"⚠️ Harita ortalama hatası: {e}")

    def manual_call_emergency(self):
        try:
            call.makecall(tel='112')
            print("📞 Manuel acil çağrı başlatıldı.")
        except Exception as e:
            print(f"❌ Manuel arama başarısız: {e}")

    def manual_send_location(self):
        try:
            # Koordinat kontrolü
            if self.latitude == 0 or self.longitude == 0:
                self.latitude = 35.1856
                self.longitude = 33.3823

            location_link = f"https://maps.google.com/?q={self.latitude},{self.longitude}"
            sms.send(
                recipient='112',
                message=f"Manual Emergency! Location: {location_link}"
            )
            print("📲 Manuel SMS gönderildi.")
        except Exception as e:
            print(f"❌ Manuel SMS gönderimi başarısız: {e}")
