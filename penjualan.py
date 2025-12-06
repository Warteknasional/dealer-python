
from mobil import Mobil

class Penjualan:
    def __init__(self):
        from connection import koneksi 
        print(" [DEBUG Penjualan] -> Memulai koneksi di Logic...")
        self.mydb, self.mycursor = koneksi()

    def ambil_data_barang(self):
        """
        Mengambil data dari tabel mobil (lewat class Mobil yang sudah ada).
        """
        # Kita pakai method static yang sudah kamu buat di mobil.py
        return Mobil.get_all_mobil()

    def simpan_transaksi(self, data_pembeli, keranjang):
        from connection import koneksi
        
        # Cek koneksi
        if not hasattr(self, 'mydb') or self.mydb is None or not self.mydb.is_connected():
            self.mydb, self.mycursor = koneksi()

        try:
            for item in keranjang:
                id_mobil = item['id']
                qty = int(item['qty'])
                subtotal = int(item['subtotal'])
                
                # Query SQL
                sql_jual = "INSERT INTO penjualan (id_mobil, nama_pelanggan, nomor_pelanggan, jumlah, total_harga) VALUES (%s, %s, %s, %s, %s)"
                val_jual = (id_mobil, data_pembeli['nama'], data_pembeli['telp'], qty, subtotal)
                self.mycursor.execute(sql_jual, val_jual)

                sql_update = "UPDATE mobil SET stok = stok - %s WHERE id = %s"
                self.mycursor.execute(sql_update, (qty, id_mobil))

            self.mydb.commit()
            return True, "Berhasil"
        except Exception as e:
            print(f"Error SQL: {e}")
            return False, str(e)
        
    def ambil_riwayat(self):
        """Mengambil data gabungan tabel penjualan dan mobil untuk history"""
        sql = """
            SELECT p.tanggal, p.nama_pelanggan, m.merk, p.jumlah, p.total_harga 
            FROM penjualan p
            JOIN mobil m ON p.id_mobil = m.id
            ORDER BY p.tanggal DESC
        """
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()