import mysql.connector

def koneksi():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom"
        )
        cursor = mydb.cursor()
        print("✅ Koneksi ke database berhasil.")
        return mydb, cursor
    except mysql.connector.Error as err:
        print(f"❌ Gagal terkoneksi ke database: {err}")
        return None, None

