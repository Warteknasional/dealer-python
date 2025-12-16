# -*- coding: utf-8 -*-

import mysql.connector 
import sys
import pandas as pd  # <--- WAJIB INSTALL: pip install pandas openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate 
from penjualan import Penjualan 

class RiwayatPenjualan(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Laporan Penjualan & Export Excel")
        self.resize(950, 600)
        self.setStyleSheet("background-color: #ffffff; font-family: Segoe UI;")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ============================
        # 1. HEADER (JUDUL & OMSET)
        # ============================
        top_frame = QtWidgets.QFrame()
        top_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; border: 1px solid #ddd;")
        top_layout = QtWidgets.QHBoxLayout(top_frame)

        title_layout = QtWidgets.QVBoxLayout()
        lbl_title = QtWidgets.QLabel("Laporan Penjualan")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; border: none;")
        lbl_subtitle = QtWidgets.QLabel("Filter tanggal lalu export data ke Excel")
        lbl_subtitle.setStyleSheet("font-size: 12px; color: #7f8c8d; border: none;")
        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)

        top_layout.addLayout(title_layout)
        top_layout.addStretch()

        # Label Omset Besar
        self.label_omset = QtWidgets.QLabel("Rp 0")
        self.label_omset.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_omset.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: #27ae60; 
            border: none; background: transparent;
        """)
        top_layout.addWidget(QtWidgets.QLabel("Total Omset: "))
        top_layout.addWidget(self.label_omset)

        main_layout.addWidget(top_frame)

        # ============================
        # 2. FILTER AREA
        # ============================
        filter_group = QtWidgets.QGroupBox("Filter Data")
        filter_layout = QtWidgets.QHBoxLayout(filter_group)
        filter_layout.setSpacing(10)

        # -- Kalender Mulai --
        filter_layout.addWidget(QtWidgets.QLabel("Dari:"))
        self.date_start = QtWidgets.QDateEdit()
        self.date_start.setCalendarPopup(True) 
        self.date_start.setDisplayFormat("yyyy-MM-dd")
        self.date_start.setDate(QDate.currentDate().addDays(-7)) 
        self.date_start.setFixedWidth(120)
        self.date_start.dateChanged.connect(self.filter_data) 
        filter_layout.addWidget(self.date_start)

        # -- Kalender Sampai --
        filter_layout.addWidget(QtWidgets.QLabel("Sampai:"))
        self.date_end = QtWidgets.QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDisplayFormat("yyyy-MM-dd")
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setFixedWidth(120)
        self.date_end.dateChanged.connect(self.filter_data)
        filter_layout.addWidget(self.date_end)

        # -- Garis Pemisah --
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        filter_layout.addWidget(line)

        # -- Search Nama --
        self.input_search = QtWidgets.QLineEdit()
        self.input_search.setPlaceholderText("🔍 Cari nama pembeli...")
        self.input_search.textChanged.connect(self.filter_data)
        filter_layout.addWidget(self.input_search)

        # -- Tombol Reset --
        btn_reset = QtWidgets.QPushButton("Reset Filter")
        btn_reset.setCursor(QtCore.Qt.PointingHandCursor)
        btn_reset.clicked.connect(self.reset_filter)
        filter_layout.addWidget(btn_reset)

        main_layout.addWidget(filter_group)

        # ============================
        # 3. TABLE
        # ============================
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(["Tanggal & Jam", "Pembeli", "Mobil", "Qty", "Total (Rp)"])
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) 
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch) 
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        # Style Table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: none;
            }
        """)
        main_layout.addWidget(self.table)

        # ============================
        # 4. FOOTER BUTTONS
        # ============================
        btn_layout = QtWidgets.QHBoxLayout()
        
        self.btn_refresh = QtWidgets.QPushButton("🔄 Refresh Database")
        self.btn_refresh.clicked.connect(self.load_data_db)
        self.btn_refresh.setFixedWidth(150)
        btn_layout.addWidget(self.btn_refresh)
        
        btn_layout.addStretch()

        # --- TOMBOL EXCEL BARU ---
        self.btn_excel = QtWidgets.QPushButton("📊 Export ke Excel")
        self.btn_excel.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_excel.setFixedWidth(150)
        self.btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #217346; 
                color: white; 
                font-weight: bold; 
                border-radius: 4px; padding: 8px;
            }
            QPushButton:hover { background-color: #1e6b41; }
        """)
        self.btn_excel.clicked.connect(self.export_excel)
        btn_layout.addWidget(self.btn_excel)
        
        self.btn_close = QtWidgets.QPushButton("Tutup")
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setFixedWidth(100)
        btn_layout.addWidget(self.btn_close)

        main_layout.addLayout(btn_layout)

        # === LOGIC INIT ===
        self.logic = Penjualan()
        self.data_cache = [] 
        self.current_filtered_data = [] # Menyimpan data yg sedang tampil untuk di-export
        self.load_data_db()

    def load_data_db(self):
        try:
            raw_data = self.logic.ambil_riwayat()
            
            self.data_cache = []
            for row in raw_data:
                tgl_obj = row[0]
                tgl_str = tgl_obj.strftime("%Y-%m-%d") if tgl_obj else "1900-01-01"
                tgl_display = tgl_obj.strftime("%d-%m-%Y %H:%M") if tgl_obj else "-"

                self.data_cache.append({
                    "date_obj": tgl_str,
                    "display_date": tgl_display,
                    "pembeli": row[1],
                    "mobil": row[2],
                    "qty": row[3],
                    "total": row[4]
                })
            
            self.filter_data()
            
        except Exception as e:
            print(f"Error Load: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Gagal memuat data database")

    def filter_data(self):
        start_date = self.date_start.date().toString("yyyy-MM-dd")
        end_date = self.date_end.date().toString("yyyy-MM-dd")
        keyword = self.input_search.text().lower()

        self.current_filtered_data = [] # Reset list export
        current_omset = 0

        for item in self.data_cache:
            tgl_item = item['date_obj']
            in_date_range = (start_date <= tgl_item <= end_date)
            in_name_search = keyword in item['pembeli'].lower()

            if in_date_range and in_name_search:
                self.current_filtered_data.append(item)
                current_omset += item['total']

        # Update UI Table
        self.tampilkan_tabel(self.current_filtered_data)
        
        # Update UI Omset
        self.label_omset.setText(f"Rp {current_omset:,}".replace(",", "."))

    def tampilkan_tabel(self, data_list):
        self.table.setRowCount(0)
        self.table.setRowCount(len(data_list))
        
        for row, item in enumerate(data_list):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(item['display_date']))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['pembeli']))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(item['mobil']))
            
            item_qty = QtWidgets.QTableWidgetItem(str(item['qty']))
            item_qty.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row, 3, item_qty)
            
            rp = f"{item['total']:,}".replace(",", ".")
            item_total = QtWidgets.QTableWidgetItem(rp)
            item_total.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.table.setItem(row, 4, item_total)

    def reset_filter(self):
        self.input_search.clear()
        self.date_start.setDate(QDate.currentDate().addDays(-30))
        self.date_end.setDate(QDate.currentDate())

    # =========================================================
    #  LOGIC EXPORT EXCEL
    # =========================================================
    def export_excel(self):
        # 1. Cek apakah ada data
        if not self.current_filtered_data:
            QtWidgets.QMessageBox.warning(self, "Kosong", "Tidak ada data untuk diexport!")
            return

        # 2. Buka Dialog Simpan File
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Simpan File Excel", "Laporan_Penjualan.xlsx", "Excel Files (*.xlsx)"
        )

        if filename:
            try:
                # 3. Siapkan Data untuk Pandas
                # Kita perlu merapikan data agar sesuai kolom Excel yang diinginkan
                data_export = []
                for item in self.current_filtered_data:
                    data_export.append({
                        "Tanggal Transaksi": item['display_date'],
                        "Nama Pembeli": item['pembeli'],
                        "Mobil": item['mobil'],
                        "Jumlah (Qty)": item['qty'],
                        "Total Harga": item['total']
                    })

                # 4. Buat DataFrame & Simpan
                df = pd.DataFrame(data_export)
                
                # Opsional: Hitung total bawah di Excel
                # df.loc['Total'] = df.sum(numeric_only=True) 

                df.to_excel(filename, index=False)

                QtWidgets.QMessageBox.information(self, "Sukses", f"Data berhasil disimpan ke:\n{filename}")
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Gagal", f"Terjadi kesalahan saat menyimpan:\n{e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RiwayatPenjualan()
    window.show()
    sys.exit(app.exec_())