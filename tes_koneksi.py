import mysql.connector
import sys

print("1. Mulai Test Koneksi...")

try:
    # Coba konek manual tanpa file connection.py dulu
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="showroom" # Pastikan nama database BENAR
    )
    
    if mydb.is_connected():
        print("2. BERHASIL! Koneksi Database Sukses.")
        db_Info = mydb.get_server_info()
        print("3. Versi MySQL Server:", db_Info)
        
        cursor = mydb.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("4. Terhubung ke database:", record)
        
except mysql.connector.Error as e:
    print("!!! ERROR DATABASE:", e)
    
except Exception as e:
    print("!!! ERROR LAIN:", e)

print("5. Selesai.")