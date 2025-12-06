# -*- coding: utf-8 -*-
import sys
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class NotaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Window Setting
        self.setWindowTitle("Nota Pembelian")
        self.resize(420, 650) # Sedikit diperlebar agar muat
        self.setStyleSheet("background-color: #ffffff;")

        main_layout = QtWidgets.QVBoxLayout(self)

        # HEADER UI
        header = QtWidgets.QLabel("PREVIEW NOTA")
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            padding: 15px; 
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
        """)
        main_layout.addWidget(header)

        # AREA NOTA (TEXT EDIT)
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            background-color: #f8f9fa;
            border: 1px solid #ced4da;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 10pt;
            padding: 15px;
            color: #212529;
        """)
        main_layout.addWidget(self.text_area)

        # BUTTON TUTUP / PRINT
        self.btn_close = QtWidgets.QPushButton("Tutup / Print")
        self.btn_close.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 12px;
                font-weight: bold;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_close.clicked.connect(self.accept) # Menutup dialog
        main_layout.addWidget(self.btn_close)

    def format_rupiah(self, nominal):
        """Helper untuk format angka ke format Indonesia (Titik sebagai pemisah)"""
        return f"{nominal:,}".replace(",", ".")

    def set_nota_data(self, data):
        """
        Menyusun teks struk dengan perataan yang rapi (Rata Kanan untuk Harga).
        """
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        # Lebar Kertas (Karakter)
        W = 42 
        # Garis Pemisah
        LINE = "=" * W
        DASH = "-" * W

        # -- BAGIAN HEADER --
        struk  = f"{LINE}\n"
        struk += f"{'DEALER MOBIL MAJU JAYA'.center(W)}\n"
        struk += f"{'Jl. bismillah kaya'.center(W)}\n"
        struk += f"{LINE}\n"
        struk += f"Tanggal : {now}\n"
        struk += f"Kasir   : Admin\n" # Bisa ditambah data kasir kalau ada
        struk += f"Pembeli : {data['pembeli']}\n"
        struk += f"No Telp : {data['telp']}\n"
        struk += f"{DASH}\n"
        
        # -- BAGIAN ITEM --
        # Format Header Tabel: Nama (Kiri), Qty (Tengah), Total (Kanan)
        struk += f"{'ITEM':<20} {'QTY':^5} {'SUBTOTAL':>15}\n"
        struk += f"{DASH}\n"

        for item in data['items']:
            # Potong nama jika terlalu panjang (maks 20 karakter)
            nama_barang = item['nama'][:20]
            qty = str(item['qty'])
            subtotal = self.format_rupiah(item['subtotal'])

            # Baris 1: Nama Barang
            struk += f"{nama_barang:<20}\n"
            # Baris 2: Qty dan Harga (Rata kanan)
            struk += f"{'':<20} {qty:^5} {subtotal:>15}\n"

        struk += f"{DASH}\n"

        # -- BAGIAN TOTAL (Rata Kanan) --
        # Helper lambda untuk baris total agar rapi
        def baris_total(label, nilai):
            nilai_fmt = self.format_rupiah(nilai)
            return f"{label:<20} : Rp {nilai_fmt:>14}\n"

        struk += baris_total("TOTAL BELANJA", data['total'])
        struk += baris_total("DISKON", data['diskon'])
        struk += f"{DASH}\n"
        struk += baris_total("GRAND TOTAL", data['grand_total'])
        struk += baris_total("TUNAI", data['bayar'])
        struk += baris_total("KEMBALI", data['kembali'])
        
        struk += f"{LINE}\n"
        struk += f"{'TERIMA KASIH ATAS KUNJUNGAN ANDA'.center(W)}\n"
        struk += f"{'BARANG YANG DIBELI TIDAK DAPAT'.center(W)}\n"
        struk += f"{'DIKEMBALIKAN'.center(W)}\n"
        struk += f"{LINE}\n"

        self.text_area.setText(struk)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Data dummy untuk test tampilan
    dummy_data = {
        "pembeli": "Budi Santoso",
        "telp": "08123456789",
        "items": [
            {"nama": "Toyota Avanza G", "qty": 1, "subtotal": 250000000},
            {"nama": "Aksesoris Kaca Film", "qty": 2, "subtotal": 1500000}
        ],
        "total": 251500000,
        "diskon": 500000,
        "grand_total": 251000000,
        "bayar": 251000000,
        "kembali": 0
    }

    window = NotaDialog()
    window.set_nota_data(dummy_data) # Test data
    window.show()
    sys.exit(app.exec_())