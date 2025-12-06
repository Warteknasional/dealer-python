# --- JANGAN ADA IMPORT APA-APA DI SINI ---
# (Biarkan kosong atau komentar saja)

def koneksi():
    try:
        # --- Import HANYA dilakukan di sini ---
        import mysql.connector 
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom"
        )
        
        if mydb.is_connected():
            print("✅ Koneksi Database Berhasil.")
            return mydb, mydb.cursor()
        else:
            return None, None
       
    except Exception as err:
        print(f"❌ Error Koneksi: {err}")
        return None, None

# Hapus pemanggilan koneksi() di bawah kalau mau dipakai di form
# koneksi()