from connection import koneksi

# =========================================================
# SUPERCLASS: MOBIL (MOBIL UMUM)
# =========================================================
class Mobil:
    def __init__(self, merk: str, harga: int, stok: int):
        self.__merk = merk
        self.__harga = harga
        self.__stok = stok
        self.__id = None
        
        try:
            self.mydb, self.mycursor = koneksi()
        except:
            self.mydb = None
            self.mycursor = None

    # ======== GETTER & SETTER ========
    @property
    def merk(self): return self.__merk
    @merk.setter
    def merk(self, value): self.__merk = value

    @property
    def harga(self): return self.__harga
    @harga.setter
    def harga(self, value): 
        if value >= 0: self.__harga = value

    @property
    def stok(self): return self.__stok
    @stok.setter
    def stok(self, value): 
        if value >= 0: self.__stok = value

    @property
    def id(self): return self.__id
    @id.setter 
    def id(self, value): self.__id = value

    # ========== METHOD DATABASE ==========
    def simpan(self):
        sql = "INSERT INTO mobil (merk, harga, stok) VALUES (%s, %s, %s)"
        val = (self.__merk, self.__harga, self.__stok)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.__id = self.mycursor.lastrowid
        print(f"✅ Mobil Umum {self.__merk} berhasil disimpan (ID: {self.__id}).")

    def update_by_id(self, uid):
        sql = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        sql = "SELECT id, merk, harga, stok FROM mobil WHERE id=%s"
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil(res[1], res[2], res[3])
            obj.id = res[0]
            return obj
        return None

    @staticmethod
    def hapus_by_id(uid):
        mydb, mycursor = koneksi()
        sql = "DELETE FROM mobil WHERE id=%s"
        mycursor.execute(sql, (uid,))
        mydb.commit()
        return True

    # === FITUR VIEW ALL (JOIN 3 TABEL) ===
    @staticmethod
    def get_all_mobil():
        mydb, mycursor = koneksi()
        # Teknik LEFT JOIN: Menggabungkan 3 tabel sekaligus
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, s.kecepatan, l.kapasitas
            FROM mobil m
            LEFT JOIN mobil_sport s ON m.id = s.mobil_id
            LEFT JOIN mobil_listrik l ON m.id = l.mobil_id
            ORDER BY m.id ASC
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

# =========================================================
# SUBCLASS: MOBIL LISTRIK
# =========================================================
class Mobil_Listrik(Mobil):
    def __init__(self, merk: str, harga: int, stok: int, kapasitas: int):
        super().__init__(merk, harga, stok)
        self.__kapasitas = kapasitas

    @property
    def kapasitas(self): return self.__kapasitas
    @kapasitas.setter
    def kapasitas(self, value):
        if value >= 0: self.__kapasitas = value

    def simpan(self):
        super().simpan() 
        sql = "INSERT INTO mobil_listrik (mobil_id, kapasitas) VALUES (%s, %s)"
        val = (self.id, self.__kapasitas)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🔋 Mobil Listrik {self.merk} berhasil disimpan.")

    def update_by_id(self, uid):
        # Update Induk
        sql1 = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val1 = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql1, val1)
        
        # Update Anak (FIXED: Tabel mobil_listrik)
        sql2 = "UPDATE mobil_listrik SET kapasitas=%s WHERE mobil_id=%s"
        val2 = (self.kapasitas, uid)
        self.mycursor.execute(sql2, val2)
        
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        # FIXED: Join mobil_listrik
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, l.kapasitas 
            FROM mobil m 
            JOIN mobil_listrik l ON m.id = l.mobil_id 
            WHERE m.id = %s
        """
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil_Listrik(res[1], res[2], res[3], res[4])
            obj.id = res[0]
            return obj
        return None

    @staticmethod
    def hapus_by_id(uid):
        mydb, mycursor = koneksi()
        # Hapus anak dulu (FIXED: Tabel mobil_listrik)
        sql1 = "DELETE FROM mobil_listrik WHERE mobil_id=%s"
        mycursor.execute(sql1, (uid,))
        # Hapus induk
        sql2 = "DELETE FROM mobil WHERE id=%s"
        mycursor.execute(sql2, (uid,))
        mydb.commit()
        return True

# =========================================================
# SUBCLASS: MOBIL SPORT
# =========================================================
class Mobil_Sport(Mobil):
    def __init__(self, merk: str, harga: int, stok: int, kecepatan: int):
        super().__init__(merk, harga, stok)
        self.__kecepatan = kecepatan

    @property
    def kecepatan(self): return self.__kecepatan
    @kecepatan.setter
    def kecepatan(self, value):
        if value >= 0: self.__kecepatan = value

    def simpan(self):
        super().simpan() 
        sql = "INSERT INTO mobil_sport (mobil_id, kecepatan) VALUES (%s, %s)"
        val = (self.id, self.__kecepatan)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🏎️ Mobil Sport {self.merk} berhasil disimpan.")

    def update_by_id(self, uid):
        # Update Induk
        sql1 = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val1 = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql1, val1)
        
        # Update Anak (FIXED: Tabel mobil_sport)
        sql2 = "UPDATE mobil_sport SET kecepatan=%s WHERE mobil_id=%s"
        val2 = (self.kecepatan, uid)
        self.mycursor.execute(sql2, val2)
        
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        # FIXED: Join mobil_sport
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, s.kecepatan 
            FROM mobil m 
            JOIN mobil_sport s ON m.id = s.mobil_id 
            WHERE m.id = %s
        """
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil_Sport(res[1], res[2], res[3], res[4])
            obj.id = res[0]
            return obj
        return None

    @staticmethod
    def hapus_by_id(uid):
        mydb, mycursor = koneksi()
        # Hapus anak dulu (FIXED: Tabel mobil_sport)
        sql1 = "DELETE FROM mobil_sport WHERE mobil_id=%s"
        mycursor.execute(sql1, (uid,))
        # Hapus induk
        sql2 = "DELETE FROM mobil WHERE id=%s"
        mycursor.execute(sql2, (uid,))
        mydb.commit()
        return True