from mobil import Mobil

class Penjualan:
    def __init__(self):
        self.daftar_mobil = []
        self._total_penjualan = 0

    def get_total_penjualan(self):
        return self._total_penjualan

    def jual_kendaraan(self, mobil: Mobil, jumlah: int):
        if mobil.stok >= jumlah and jumlah > 0:
            mobil.stok -= jumlah        # Kurangi stok langsung
            mobil.update()              # Update stok ke DB

            self.daftar_mobil.append({
                'mobil': mobil.merk,
                'jumlah': jumlah,
                'harga_satuan': mobil.harga
            })

            self.hitung_total_penjualan()

            print(f"✅ Berhasil menjual {jumlah} unit {mobil.merk}. Sisa stok: {mobil.stok}")
        else:
            print(f"❌ Stok tidak cukup! Stok saat ini: {mobil.stok}")

    def hitung_total_penjualan(self):
        self._total_penjualan = sum(
            item['jumlah'] * item['harga_satuan'] 
            for item in self.daftar_mobil
        )
        print(f"Total penjualan saat ini: Rp{self._total_penjualan:,.2f}")
