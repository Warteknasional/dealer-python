from mobil import Mobil, Mobil_Listrik, Mobil_Sport
from penjualan import Penjualan

# List global untuk menyimpan semua objek mobil
daftar_mobil=[]

# Objek penjualan global
penjualan_showroom = Penjualan()

def cari_mobil(merk):
    """Mencari objek mobil berdasarkan merk."""
    for mobil in daftar_mobil:
        if mobil.get_merk().lower() == merk.lower():
            return mobil
    return None

def menu_kelola_mobil():
    """Mengelola menu untuk manipulasi objek mobil yang sudah ada."""
    while True:
        print("\n=== SUBMENU KELOLA MOBIL ===")
        print("1. Tambah Mobil Baru")
        print("2. Lihat Semua Mobil")
        print("3. Update Stok Mobil")
        print("4. Hapus Mobil")
        print("5. Kembali ke Menu Utama")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            merk = input("Masukkan merk mobil: ")
            harga = int(input("Masukkan harga: "))
            stok = int(input("Masukkan stok: "))
            jenis = input("Apakah mobil listrik (L) atau sport (S)? [Tipe lain default]: ")
            if jenis.lower() == "l":
                kapasitas = int(input("Masukkan kapasitas baterai (kWh): "))
                mobil_baru = Mobil_Listrik(merk, harga, stok, kapasitas)
            elif jenis.lower() == "s":
                kecepatan = int(input("Masukkan kecepatan maksimal (km/h): "))
                mobil_baru = Mobil_Sport(merk, harga, stok, kecepatan)
            else:
                mobil_baru = Mobil(merk, harga, stok)
            daftar_mobil.append(mobil_baru)
            print(f"✅ Mobil {merk} berhasil ditambahkan.")

        elif pilihan == "2":
            if not daftar_mobil:
                print("Daftar mobil kosong.")
            else:
                print("\n--- DAFTAR MOBIL SAAT INI ---")
                for mobil in daftar_mobil:
                    print(mobil)
                    
        elif pilihan == "3":
            merk_mobil = input("Masukkan merk mobil yang ingin di-update stoknya: ")
            mobil_ditemukan = cari_mobil(merk_mobil)
            if mobil_ditemukan:
                jumlah_tambah = int(input("Masukkan jumlah stok yang akan ditambahkan: "))
                mobil_ditemukan.tambah_mobil(jumlah_tambah)
            else:
                print("❌ Mobil tidak ditemukan.")

        elif pilihan == "4":
            merk_mobil = input("Masukkan merk mobil yang ingin dihapus: ")
            mobil_ditemukan = cari_mobil(merk_mobil)
            if mobil_ditemukan:
                daftar_mobil.remove(mobil_ditemukan)
                print(f"✅ Mobil {merk_mobil} berhasil dihapus.")
            else:
                print("❌ Mobil tidak ditemukan.")

        elif pilihan == "5":
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")


def menu_penjualan():
    """Mengelola menu untuk transaksi penjualan."""
    while True:
        print("\n=== SUBMENU PENJUALAN ===")
        print("1. Jual Kendaraan")
        print("2. Lihat Total Penjualan")
        print("3. Kembali ke Menu Utama")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            merk_mobil = input("Masukkan merk mobil yang ingin dijual: ")
            mobil_dijual = cari_mobil(merk_mobil)
            if mobil_dijual:
                try:
                    jumlah = int(input(f"Masukkan jumlah unit {mobil_dijual.get_merk()} yang akan dijual: "))
                    # Memanggil metode dari objek global
                    penjualan_showroom.jual_kendaraan(mobil_dijual, jumlah)
                except ValueError:
                    print("❌ Input jumlah tidak valid. Masukkan angka.")
            else:
                print("❌ Mobil tidak ditemukan.")
        
        elif pilihan == "2":
            print(f"\nTotal penjualan saat ini: Rp{penjualan_showroom.get_total_penjualan():,.2f}")
        
        elif pilihan == "3":
            break
        
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")


def main():
    """Fungsi utama untuk menjalankan program."""
    while True:
        print("\n=== MENU UTAMA SHOWROOM ===")
        print("1. Kelola Mobil")
        print("2. Penjualan")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            menu_kelola_mobil()
        elif pilihan == "2":
            menu_penjualan()
        elif pilihan == "3":
            print("👋 Terima kasih telah menggunakan sistem showroom!")
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")

main()