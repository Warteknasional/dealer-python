from connection import koneksi

class DB:
    def __init__(self):
        self.mydb, self.mycursor = koneksi()

    def insert_mobil(self, merk, harga, stok):
        sql = "INSERT INTO mobil (merk, harga, stok) VALUES (%s, %s, %s)"
        val = (merk, harga, stok)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "mobil telah ditambahkan.")

    def select_mobil(self):
        self.mycursor.execute("SELECT * FROM mobil")
        hasil = self.mycursor.fetchall()
        if not hasil:
            print("Belum ada data mobil.")
        else:
            print("\nDaftar Mobil:")
            for row in hasil:
                print(f"ID: {row[0]}, Merk: {row[1]}, Harga: {row[2]}, Stok: {row[3]}")

    def update_mobil(self, merk, harga, stok):
        sql = "UPDATE mobil SET harga = %s, stok = %s WHERE merk = %s"
        val = (harga, stok, merk)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "mobil telah diupdate.")

    def delete_mobil(self, merk):
        sql = "DELETE FROM mobil WHERE merk = %s"
        val = (merk,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "mobil telah dihapus.")

