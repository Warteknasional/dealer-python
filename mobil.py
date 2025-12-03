from connection import koneksi

class Mobil:
    def __init__(self, merk: str, harga: int, stok: int):
        self.__merk = merk
        self.__harga = harga
        self.__stok = stok
        self.mydb, self.mycursor = koneksi()
        self.__id = None

    # ======== GETTER & SETTER ========
    @property
    def merk(self):
        return self.__merk

    @merk.setter
    def merk(self, value):
        if value != "":
            self.__merk = value

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, value):
        if value >= 0:
            self.__harga = value

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, value):
        if value >= 0:
            self.__stok = value

    @property
    def id(self):
        return self.__id

    # ========== METHOD DATABASE ==========
    def simpan(self):
        sql = "INSERT INTO mobil (merk, harga, stok) VALUES (%s, %s, %s)"
        val = (self.__merk, self.__harga, self.__stok)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.__id = self.mycursor.lastrowid
        print(f"✅ Mobil {self.__merk} berhasil disimpan (ID: {self.__id}).")

    def update(self):
        sql = "UPDATE mobil SET harga=%s, stok=%s WHERE merk=%s"
        val = (self.__harga, self.__stok, self.__merk)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"✅ Mobil {self.__merk} berhasil diperbarui di database.")

    @staticmethod
    def hapus_semua():
        mydb, mycursor = koneksi()
        mycursor.execute("DELETE FROM mobil")
        mydb.commit()
        print("🗑️ Seluruh mobil berhasil dihapus dari database.")

    @staticmethod
    def tampilkan_semua():
        mydb, mycursor = koneksi()
        mycursor.execute("SELECT * FROM mobil")
        hasil = mycursor.fetchall()
        if hasil:
            print("\nDaftar Mobil:")
            for row in hasil:
                print(f"ID: {row[0]}, Merk: {row[1]}, Harga: {row[2]}, Stok: {row[3]}")
        else:
            print("⚠️ Tidak ada data mobil dalam database.")

    @staticmethod
    def get_by_merk(merk):
        mydb, mycursor = koneksi()
        sql = "SELECT id, merk, harga, stok FROM mobil WHERE merk=%s"
        mycursor.execute(sql, (merk,))
        result = mycursor.fetchone()

        if result:
            obj = Mobil(result[1], result[2], result[3])
            obj.__id = result[0]
            return obj
        return None

    def __str__(self):
        return f"Merk: {self.__merk}, Harga: {self.__harga}, Stok: {self.__stok}"

class Mobil_Listrik(Mobil):
    def __init__(self, merk: str, harga: int, stok: int, kapasitas: int):
        super().__init__(merk, harga, stok)
        self.__kapasitas = kapasitas

    @property
    def kapasitas(self):
        return self.__kapasitas

    @kapasitas.setter
    def kapasitas(self, value):
        if value >= 0:
            self.__kapasitas = value

    def simpan(self):
        super().simpan()
        sql = "INSERT INTO mobil_listrik (mobil_id, kapasitas) VALUES (%s, %s)"
        val = (self.id, self.__kapasitas)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🔋 Mobil listrik {self.merk} berhasil disimpan ke tabel mobil_listrik.")

    def update(self):
        super().update()
        sql = """
        UPDATE mobil_listrik ml
        JOIN mobil m ON ml.mobil_id = m.id
        SET ml.kapasitas = %s
        WHERE m.merk = %s
        """
        self.mycursor.execute(sql, (self.__kapasitas, self.merk))
        self.mydb.commit()
        print(f"✅ Mobil listrik {self.merk} berhasil diperbarui.")

    def hapus(self):
        sql = """
        DELETE ml FROM mobil_listrik ml
        JOIN mobil m ON ml.mobil_id = m.id
        WHERE m.merk = %s
        """
        self.mycursor.execute(sql, (self.merk,))
        self.mydb.commit()

        sql2 = "DELETE FROM mobil WHERE merk=%s"
        self.mycursor.execute(sql2, (self.merk,))
        self.mydb.commit()
        print(f"🗑️ Mobil listrik {self.merk} berhasil dihapus sepenuhnya.")

    def __str__(self):
        return f"Mobil Listrik - Merk: {self.merk}, Harga: {self.harga}, Stok: {self.stok}, Kapasitas: {self.__kapasitas} kWh"
class Mobil_Sport(Mobil):
    def __init__(self, merk: str, harga: int, stok: int, kecepatan: int):
        super().__init__(merk, harga, stok)
        self.__kecepatan = kecepatan

    @property
    def kecepatan(self):
        return self.__kecepatan

    @kecepatan.setter
    def kecepatan(self, value):
        if value >= 0:
            self.__kecepatan = value

    def simpan(self):
        super().simpan()
        sql = "INSERT INTO mobil_sport (mobil_id, kecepatan) VALUES (%s, %s)"
        val = (self.id, self.__kecepatan)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🏎️ Mobil sport {self.merk} berhasil disimpan.")

    def update(self):
        super().update()
        sql = """
        UPDATE mobil_sport ms
        JOIN mobil m ON ms.mobil_id = m.id
        SET ms.kecepatan = %s
        WHERE m.merk = %s
        """
        self.mycursor.execute(sql, (self.__kecepatan, self.merk))
        self.mydb.commit()
        print(f"✅ Mobil sport {self.merk} berhasil diperbarui.")

    def hapus(self):
        sql = """
        DELETE ms FROM mobil_sport ms
        JOIN mobil m ON ms.mobil_id = m.id
        WHERE m.merk = %s
        """
        self.mycursor.execute(sql, (self.merk,))
        self.mydb.commit()

        sql2 = "DELETE FROM mobil WHERE merk=%s"
        self.mycursor.execute(sql2, (self.merk,))
        self.mydb.commit()
        print(f"🗑️ Mobil sport {self.merk} berhasil dihapus sepenuhnya.")

    def __str__(self):
        return f"Mobil Sport - Merk: {self.merk}, Harga: {self.harga}, Stok: {self.stok}, Kecepatan: {self.__kecepatan} km/h"
