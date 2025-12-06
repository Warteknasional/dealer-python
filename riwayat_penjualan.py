# -*- coding: utf-8 -*-

# --- PENTING: IMPORT DRIVER DI PALING ATAS (ANTI-CRASH) ---
import mysql.connector 

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from penjualan import Penjualan  # <--- Import Logic Database

class RiwayatPenjualan(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Riwayat Penjualan")
        self.resize(800, 520) # Saya perlebar sedikit biar muat
        self.setStyleSheet("background-color: #ffffff;")

        main_layout = QtWidgets.QVBoxLayout(self)

        # ============================
        # TITLE + OMSET
        # ============================
        top_layout = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("Riwayat Penjualan")
        title.setStyleSheet("font-size: 17px; font-weight: bold; color: #333;")
        top_layout.addWidget(title)

        top_layout.addStretch()

        self.label_omset = QtWidgets.QLabel("Omset: Rp 0")
        self.label_omset.setStyleSheet("""
            font-size: 13px; color: #555; padding: 4px 8px;
            border: 1px solid #e0e0e0; border-radius: 4px;
        """)
        top_layout.addWidget(self.label_omset)

        main_layout.addLayout(top_layout)

        # ============================
        # SEARCH BAR
        # ============================
        self.input_search = QtWidgets.QLineEdit()
        self.input_search.setPlaceholderText("Cari tanggal (YYYY-MM-DD) atau nama pembeli...")
        self.input_search.setStyleSheet("""
            padding: 6px; border: 1px solid #e6e6e6;
            border-radius: 4px; font-size: 12px;
        """)
        self.input_search.textChanged.connect(self.filter_data)
        main_layout.addWidget(self.input_search)

        # ============================
        # TABLE (Update Kolom)
        # ============================
        self.table = QtWidgets.QTableWidget()
        # Kolom: Tanggal, Pembeli, Mobil, Qty, Total
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(["Tanggal", "Pembeli", "Mobil", "Qty", "Total (Rp)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) # Nama pembeli lebar
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch) # Nama mobil lebar

        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #fafafa; padding: 6px;
                font-size: 12px; border: none; font-weight: bold;
            }
        """)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e6e6e6; border-radius: 4px; font-size: 12px;
            }
        """)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        main_layout.addWidget(self.table)

        # ============================
        # BUTTON KEMBALI / REFRESH
        # ============================
        btn_layout = QtWidgets.QHBoxLayout()
        
        self.btn_refresh = QtWidgets.QPushButton("Refresh Data")
        self.btn_refresh.clicked.connect(self.load_data_db)
        self.btn_refresh.setStyleSheet("background-color: #e0f7fa; padding: 8px; border-radius: 4px;")
        btn_layout.addWidget(self.btn_refresh)
        
        btn_layout.addStretch()
        
        self.btn_back = QtWidgets.QPushButton("Tutup")
        self.btn_back.setStyleSheet("background-color: #f5f5f5; padding: 8px; border-radius: 4px;")
        self.btn_back.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_back)

        main_layout.addLayout(btn_layout)

        # === LOGIC ===
        self.logic = Penjualan()
        self.data_cache = [] # Untuk menyimpan data asli dari DB
        
        # Load Data Pertama Kali
        self.load_data_db()

    def load_data_db(self):
        """Mengambil data riwayat dari database lewat Logic"""
        try:
            # Panggil fungsi ambil_riwayat dari penjualan.py
            raw_data = self.logic.ambil_riwayat()
            # Raw data format: (tanggal, nama_pelanggan, merk_mobil, jumlah, total_harga)
            
            self.data_cache = []
            total_omset = 0
            
            for row in raw_data:
                # Konversi datetime ke string
                tgl = row[0].strftime("%Y-%m-%d %H:%M") if row[0] else "-"
                
                # Masukkan ke cache
                self.data_cache.append({
                    "tanggal": tgl,
                    "pembeli": row[1],
                    "mobil": row[2],
                    "qty": row[3],
                    "total": row[4]
                })
                
                total_omset += row[4]
            
            # Update Label Omset
            self.label_omset.setText(f"Omset: Rp {total_omset:,}")
            
            # Tampilkan ke tabel
            self.tampilkan_tabel(self.data_cache)
            
        except Exception as e:
            print(f"Gagal load riwayat: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Gagal memuat data: {e}")

    def tampilkan_tabel(self, data_list):
        """Menampilkan list data ke QTableWidget"""
        self.table.setRowCount(0)
        self.table.setRowCount(len(data_list))
        
        for row, item in enumerate(data_list):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['tanggal']))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['pembeli']))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['mobil']))
            
            qty_item = QtWidgets.QTableWidgetItem(str(item['qty']))
            qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row, 3, qty_item)
            
            total_str = f"{item['total']:,}"
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(total_str))

    def filter_data(self):
        """Filter data berdasarkan input search (Tanggal / Nama)"""
        keyword = self.input_search.text().lower()
        
        filtered = [
            d for d in self.data_cache 
            if keyword in d['tanggal'].lower() or keyword in d['pembeli'].lower()
        ]
        
        self.tampilkan_tabel(filtered)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RiwayatPenjualan()
    window.show()
    sys.exit(app.exec_())