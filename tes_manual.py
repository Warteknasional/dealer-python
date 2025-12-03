from connection import koneksi

print("\n=== DEBUGGER DATABASE SHOWROOM ===")

try:
    # 1. Cek Koneksi
    db_conn = koneksi()
    if isinstance(db_conn, tuple):
        conn, cursor = db_conn
    else:
        conn = db_conn
        cursor = conn.cursor()

    # 2. Cek Kita Ada di Database Mana
    cursor.execute("SELECT DATABASE()")
    nama_db = cursor.fetchone()[0]
    print(f"📂 Terhubung ke: '{nama_db}'")

    if nama_db != 'showroom':
        print("❌ SALAH DATABASE! Cek file connection.py")
        exit()

    # 3. Cek Nama Kolom di Tabel User
    print("🔍 Mengecek struktur tabel 'user'...")
    cursor.execute("DESCRIBE user")
    kolom = cursor.fetchall()
    
    nama_kolom_posisi = ""
    list_kolom = []
    
    for k in kolom:
        list_kolom.append(k[0])
        if k[0] == 'posisi':
            nama_kolom_posisi = 'posisi'
        elif k[0] == 'level':
            nama_kolom_posisi = 'level'

    print(f"📋 Kolom ditemukan: {list_kolom}")

    if not nama_kolom_posisi:
        print("❌ Masalah Ditemukan: Tidak ada kolom 'posisi' atau 'level' di tabel user!")
        print("   Silakan buat ulang tabelnya.")
    else:
        print(f"✅ Kolom jabatan yang benar adalah: '{nama_kolom_posisi}'")

        # 4. Tes Insert Manual Sesuai Nama Kolom
        print(f"🚀 Mencoba insert ke kolom '{nama_kolom_posisi}'...")
        
        sql = f"INSERT INTO user (name, username, password, {nama_kolom_posisi}) VALUES (%s, %s, %s, %s)"
        val = ('Tes Showroom', 'tes_showroom', '123', 'admin')
        
        cursor.execute(sql, val)
        conn.commit() # KOMIT AGAR DISIMPAN
        
        print(f"✅ SUKSES! Data user 'tes_showroom' berhasil masuk.")
        print("👉 Coba cek di phpMyAdmin sekarang.")

except Exception as e:
    print(f"❌ ERROR: {e}")