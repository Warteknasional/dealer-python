from connection import koneksi

# =========================================================
# SUPERCLASS: MOBIL (MOBIL UMUM)
# =========================================================
class Mobil:
    def __init__(self, merk: str, harga: int, stok: int):
        # Langsung public attribute (tanpa underscore ganda)
        self.merk = merk
        self.harga = harga
        self.stok = stok
        self.id = None
        
        try:
            self.mydb, self.mycursor = koneksi()
        except:
            self.mydb = None
            self.mycursor = None

    # ========== METHOD DATABASE ==========
    def simpan(self):
        # Default status saat simpan adalah 'aktif'
        sql = "INSERT INTO mobil (merk, harga, stok, status) VALUES (%s, %s, %s, 'aktif')"
        val = (self.merk, self.harga, self.stok)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.id = self.mycursor.lastrowid
        print(f"✅ Mobil Umum {self.merk} berhasil disimpan (ID: {self.id}).")

    def update_by_id(self, uid):
        sql = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        # Filter hanya yang aktif
        sql = "SELECT id, merk, harga, stok FROM mobil WHERE id=%s AND status='aktif'"
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil(res[1], res[2], res[3])
            obj.id = res[0]
            return obj
        return None

    @staticmethod
    def hapus_by_id(uid):
        """
        SOFT DELETE:
        Tidak menghapus baris data (agar tidak error di tabel penjualan),
        tapi hanya mengubah status menjadi 'nonaktif'.
        """
        mydb, mycursor = koneksi()
        sql = "UPDATE mobil SET status = 'nonaktif' WHERE id=%s"
        mycursor.execute(sql, (uid,))
        mydb.commit()
        print(f"⚠️ Mobil ID {uid} telah dinonaktifkan (Soft Delete).")
        return True

    # === FITUR VIEW ALL (JOIN 3 TABEL) ===
    @staticmethod
    def get_all_mobil():
        mydb, mycursor = koneksi()
        # Tambahkan WHERE m.status = 'aktif' agar mobil yang dihapus tidak muncul
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, s.kecepatan, l.kapasitas
            FROM mobil m
            LEFT JOIN mobil_sport s ON m.id = s.mobil_id
            LEFT JOIN mobil_listrik l ON m.id = l.mobil_id
            WHERE m.status = 'aktif'
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
        self.kapasitas = kapasitas  # Langsung public

    def simpan(self):
        # Simpan ke tabel induk dulu (otomatis status='aktif')
        super().simpan() 
        # Simpan ke tabel anak
        sql = "INSERT INTO mobil_listrik (mobil_id, kapasitas) VALUES (%s, %s)"
        val = (self.id, self.kapasitas)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🔋 Mobil Listrik {self.merk} berhasil disimpan.")

    def update_by_id(self, uid):
        # Update Induk
        sql1 = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val1 = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql1, val1)
        
        # Update Anak
        sql2 = "UPDATE mobil_listrik SET kapasitas=%s WHERE mobil_id=%s"
        val2 = (self.kapasitas, uid)
        self.mycursor.execute(sql2, val2)
        
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, l.kapasitas 
            FROM mobil m 
            JOIN mobil_listrik l ON m.id = l.mobil_id 
            WHERE m.id = %s AND m.status='aktif'
        """
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil_Listrik(res[1], res[2], res[3], res[4])
            obj.id = res[0]
            return obj
        return None

    # Tidak perlu def hapus_by_id() lagi disini.
    # Karena kita pakai Soft Delete di Parent, otomatis anak ikut "hilang" dari view.

# =========================================================
# SUBCLASS: MOBIL SPORT
# =========================================================
class Mobil_Sport(Mobil):
    def __init__(self, merk: str, harga: int, stok: int, kecepatan: int):
        super().__init__(merk, harga, stok)
        self.kecepatan = kecepatan # Langsung public

    def simpan(self):
        super().simpan() 
        sql = "INSERT INTO mobil_sport (mobil_id, kecepatan) VALUES (%s, %s)"
        val = (self.id, self.kecepatan)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"🏎️ Mobil Sport {self.merk} berhasil disimpan.")

    def update_by_id(self, uid):
        # Update Induk
        sql1 = "UPDATE mobil SET merk=%s, harga=%s, stok=%s WHERE id=%s"
        val1 = (self.merk, self.harga, self.stok, uid)
        self.mycursor.execute(sql1, val1)
        
        # Update Anak
        sql2 = "UPDATE mobil_sport SET kecepatan=%s WHERE mobil_id=%s"
        val2 = (self.kecepatan, uid)
        self.mycursor.execute(sql2, val2)
        
        self.mydb.commit()
        return True

    @staticmethod
    def get_by_id(uid):
        mydb, mycursor = koneksi()
        sql = """
            SELECT m.id, m.merk, m.harga, m.stok, s.kecepatan 
            FROM mobil m 
            JOIN mobil_sport s ON m.id = s.mobil_id 
            WHERE m.id = %s AND m.status='aktif'
        """
        mycursor.execute(sql, (uid,))
        res = mycursor.fetchone()
        if res:
            obj = Mobil_Sport(res[1], res[2], res[3], res[4])
            obj.id = res[0]
            return obj
        return None