import sqlite3
import os

def initialize_database():
    """Veritabanını ve gerekli tabloları oluştur"""
    db_path = "users.db"
    
    # Veritabanı dosyası varsa sil (temiz başlangıç için)
    if os.path.exists(db_path):
        print(f"🗑️ Eski veritabanı siliniyor: {db_path}")
        os.remove(db_path)
    
    print("🗄️ Yeni veritabanı oluşturuluyor...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users tablosu oluştur
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birth_year INTEGER,
            phone_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User sessions tablosu oluştur
    cursor.execute('''
        CREATE TABLE user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Security scores tablosu oluştur
    cursor.execute('''
        CREATE TABLE security_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lat REAL,
            lon REAL,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Test kullanıcısı ekle
    cursor.execute('''
        INSERT INTO users (id_number, password, birth_year, phone_number)
        VALUES (?, ?, ?, ?)
    ''', ("12345678901", "test123", 1990, "+905551234567"))
    
    conn.commit()
    conn.close()
    
    print("✅ Veritabanı başarıyla oluşturuldu!")
    print("👤 Test kullanıcısı: ID: 12345678901, Şifre: test123")

if __name__ == "__main__":
    initialize_database() 