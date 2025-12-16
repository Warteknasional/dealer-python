from connection import koneksi

class User:
    def __init__(self, name="", username="", password="", posisi=""):
        # Enkapsulasi Data
        self.__id = None
        self.__name = name
        self.__username = username
        self.__password = password
        self.__posisi = posisi
        
        # === PERBAIKAN DI SINI ===
        # koneksi() mengembalikan 2 nilai (tuple), jadi kita harus pisahkan
        # Variabel pertama jadi koneksi, variabel kedua jadi cursor
        try:
            self.__conn, self.__cursor = koneksi()
        except Exception as e:
            print(f"Gagal koneksi: {e}")
            self.__conn = None
            self.__cursor = None

    def __del__(self):
        # Tutup koneksi saat objek dihapus dari memori
        if self.__conn:
            try:
                self.__conn.close()
            except:
                pass

    # ==========================
    # SETTER & GETTER
    # ==========================
    @property
    def name(self): return self.__name
    @name.setter
    def name(self, value): self.__name = value

    @property
    def username(self): return self.__username
    @username.setter
    def username(self, value): self.__username = value

    @property
    def password(self): return self.__password
    @password.setter
    def password(self, value): self.__password = value

    @property
    def posisi(self): return self.__posisi
    @posisi.setter
    def posisi(self, value): self.__posisi = value

    # ==========================
    # DATABASE METHODS
    # ==========================
    
    # 1. SIMPAN (INSERT)
    def simpan(self):
        if not self.__cursor: return False
        try:
            # Pastikan nama kolom 'posisi' sesuai database kamu
            sql = "INSERT INTO users (name, username, password, posisi) VALUES (%s, %s, %s, %s)"
            val = (self.__name, self.__username, self.__password, self.__posisi)
            self.__cursor.execute(sql, val)
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error Simpan: {e}")
            return False

    # 2. CARI USER BY ID (PENTING UNTUK EDIT!)
    def select_user_by_id(self, user_id):
        if not self.__cursor: return None
        sql = "SELECT id, name, username, password, posisi FROM users WHERE id=%s"
        self.__cursor.execute(sql, (user_id,))
        return self.__cursor.fetchone()

    # 3. UPDATE
    def update(self, user_id):
        if not self.__cursor: return False
        try:
            if self.__password:
                sql = "UPDATE users SET name=%s, username=%s, password=%s, posisi=%s WHERE id=%s"
                val = (self.__name, self.__username, self.__password, self.__posisi, user_id)
            else:
                sql = "UPDATE users SET name=%s, username=%s, posisi=%s WHERE id=%s"
                val = (self.__name, self.__username, self.__posisi, user_id)
            
            self.__cursor.execute(sql, val)
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error Update: {e}")
            return False

    # 4. DELETE
    def hapus(self, user_id):
        if not self.__cursor: return False
        try:
            sql = "DELETE FROM users WHERE id=%s"
            self.__cursor.execute(sql, (user_id,))
            self.__conn.commit()
            return True
        except Exception as e:
            return False
            
    # 5. SELECT ALL
    def select_all_users(self):
        if not self.__cursor: return []
        sql = "SELECT id, name, username, posisi FROM users"
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()
    
    def authenticate(self, username, password):
        if not self.__cursor: return None
        sql = "SELECT id, name, username, posisi FROM users WHERE username=%s AND password=%s"
        self.__cursor.execute(sql, (username, password))
        return self.__cursor.fetchone()
    