# -*- coding: utf-8 -*-

import mysql.connector 
from form_nota import NotaDialog 
from penjualan import Penjualan 
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMessageBox, QTableWidgetItem

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 750) # Ukuran diperlebar agar muat kiri-kanan
        Dialog.setWindowTitle("SISTEM KASIR DEALER")

        # Style Global
        Dialog.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #333;
            }
            QTableWidget {
                alternating-background-color: #f9f9f9;
                selection-background-color: #007bff;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)

        # Layout Utama (Vertikal: Judul di atas, Konten di bawah)
        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)

        # JUDUL
        title = QtWidgets.QLabel("TRANSAKSI PENJUALAN DEALER")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.mainLayout.addWidget(title)

        # KONTEN UTAMA (HORIZONTAL: KIRI & KANAN)
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.setSpacing(20)

        # =========================================================
        # PANEL KIRI (Data Pembeli & Cari Barang)
        # =========================================================
        self.leftPanel = QtWidgets.QVBoxLayout()

        # 1. FORM PEMBELI
        self.formGroup = QtWidgets.QGroupBox("1. Informasi Pelanggan")
        formLayout = QtWidgets.QFormLayout()
        formLayout.setSpacing(10)
        
        self.line_nama = QtWidgets.QLineEdit()
        self.line_nama.setPlaceholderText("Nama Lengkap...")
        self.line_telp = QtWidgets.QLineEdit()
        self.line_telp.setPlaceholderText("08xxxxxx")
        self.line_telp.setValidator(QtGui.QIntValidator())
        
        formLayout.addRow("Nama Pembeli:", self.line_nama)
        formLayout.addRow("No. Telepon:", self.line_telp)
        self.formGroup.setLayout(formLayout)
        self.leftPanel.addWidget(self.formGroup)

        # 2. PENCARIAN PRODUK
        self.searchGroup = QtWidgets.QGroupBox("2. Cari & Pilih Mobil")
        searchLayout = QtWidgets.QVBoxLayout()
        
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Ketik merk mobil di sini...")
        self.search_input.setStyleSheet("font-size: 14px; padding: 8px;")
        searchLayout.addWidget(self.search_input)

        self.table_search = QtWidgets.QTableWidget()
        self.table_search.setColumnCount(4)
        self.table_search.setHorizontalHeaderLabels(["ID", "Nama Mobil", "Harga", "Aksi"])
        
        # Rapikan Tabel Search
        self.table_search.verticalHeader().setVisible(False)
        self.table_search.setAlternatingRowColors(True)
        self.table_search.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        headerS = self.table_search.horizontalHeader()
        headerS.setSectionResizeMode(1, QHeaderView.Stretch) # Nama Mobil Stretch
        headerS.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        headerS.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        headerS.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        searchLayout.addWidget(self.table_search)
        self.searchGroup.setLayout(searchLayout)
        self.leftPanel.addWidget(self.searchGroup)

        # Masukkan Left Panel ke Content Layout (Ratio 50%)
        self.contentLayout.addLayout(self.leftPanel, 50)


        # =========================================================
        # PANEL KANAN (Keranjang & Pembayaran)
        # =========================================================
        self.rightPanel = QtWidgets.QVBoxLayout()

        # 3. KERANJANG
        self.cartGroup = QtWidgets.QGroupBox("3. Keranjang Belanja")
        cartLayout = QtWidgets.QVBoxLayout()
        
        self.table_cart = QtWidgets.QTableWidget()
        self.table_cart.setColumnCount(6)
        self.table_cart.setHorizontalHeaderLabels(["ID", "Nama Produk", "Harga", "Qty", "Subtotal", "Aksi"])
        self.table_cart.setColumnHidden(0, True) # Sembunyikan ID
        
        # Rapikan Tabel Cart
        self.table_cart.verticalHeader().setVisible(False)
        self.table_cart.setAlternatingRowColors(True)
        headerC = self.table_cart.horizontalHeader()
        headerC.setSectionResizeMode(1, QHeaderView.Stretch) # Nama Produk Stretch
        headerC.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Qty kecil
        headerC.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Tombol hapus kecil
        
        cartLayout.addWidget(self.table_cart)
        self.cartGroup.setLayout(cartLayout)
        self.rightPanel.addWidget(self.cartGroup)

        # 4. PEMBAYARAN
        self.bayarGroup = QtWidgets.QGroupBox("4. Pembayaran")
        bayarLayout = QtWidgets.QVBoxLayout()
        
        # Grid untuk angka-angka agar rapi
        gridBayar = QtWidgets.QGridLayout()
        gridBayar.setVerticalSpacing(10)
        
        # Label Total Besar
        lbl_total_txt = QtWidgets.QLabel("TOTAL TAGIHAN")
        lbl_total_txt.setStyleSheet("font-size: 14px; color: #555;")
        self.label_total = QtWidgets.QLabel("0")
        self.label_total.setAlignment(QtCore.Qt.AlignRight)
        self.label_total.setStyleSheet("font-size: 28px; font-weight: bold; color: #007bff;")
        
        # Input Diskon & Bayar
        lbl_diskon = QtWidgets.QLabel("Diskon (Rp):")
        self.line_diskon = QtWidgets.QLineEdit()
        self.line_diskon.setValidator(QtGui.QIntValidator())
        self.line_diskon.setAlignment(QtCore.Qt.AlignRight)
        
        lbl_bayar = QtWidgets.QLabel("Uang Diterima (Rp):")
        self.line_nominal = QtWidgets.QLineEdit()
        self.line_nominal.setValidator(QtGui.QIntValidator())
        self.line_nominal.setAlignment(QtCore.Qt.AlignRight)
        self.line_nominal.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")

        # Kembalian
        lbl_kembali = QtWidgets.QLabel("Kembalian:")
        self.label_kembalian = QtWidgets.QLabel("0")
        self.label_kembalian.setAlignment(QtCore.Qt.AlignRight)
        self.label_kembalian.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")

        # Susun Grid
        # Baris 0: Total
        gridBayar.addWidget(lbl_total_txt, 0, 0)
        gridBayar.addWidget(self.label_total, 0, 1)
        # Baris 1: Garis Pembatas
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        gridBayar.addWidget(line, 1, 0, 1, 2)
        # Baris 2: Diskon
        gridBayar.addWidget(lbl_diskon, 2, 0)
        gridBayar.addWidget(self.line_diskon, 2, 1)
        # Baris 3: Input Bayar
        gridBayar.addWidget(lbl_bayar, 3, 0)
        gridBayar.addWidget(self.line_nominal, 3, 1)
        # Baris 4: Kembalian
        gridBayar.addWidget(lbl_kembali, 4, 0)
        gridBayar.addWidget(self.label_kembalian, 4, 1)

        bayarLayout.addLayout(gridBayar)
        self.bayarGroup.setLayout(bayarLayout)
        self.rightPanel.addWidget(self.bayarGroup)

        # TOMBOL SIMPAN
        self.btn_simpan = QtWidgets.QPushButton("✅ CETAK NOTA & SIMPAN TRANSAKSI")
        self.btn_simpan.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_simpan.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.btn_simpan.clicked.connect(self.proses_transaksi)
        self.rightPanel.addWidget(self.btn_simpan)

        # Masukkan Right Panel ke Content Layout (Ratio 50%)
        self.contentLayout.addLayout(self.rightPanel, 50)

        # Tambahkan Content Layout ke Main Layout
        self.mainLayout.addLayout(self.contentLayout)

        # ================= LOGIC SETUP =================
        try:
            self.logic = Penjualan()
            self.data_mobil_cache = []
            self.load_data_dari_db()
        except Exception as e:
            print(f"Error Init: {e}")

        self.search_input.textChanged.connect(self.filter_produk)
        self.line_nominal.textChanged.connect(self.hitung_kembalian)
        self.line_diskon.textChanged.connect(self.hitung_kembalian)

    def load_data_dari_db(self):
        try:
            raw_data = self.logic.ambil_data_barang()
            self.data_mobil_cache = []
            for row in raw_data:
                # Asumsi row[3] adalah stok
                if row[3] > 0: 
                    nama = row[1]
                    if len(row) > 4 and row[4]: nama += f" (Sport {row[4]} km/h)"
                    elif len(row) > 5 and row[5]: nama += f" (EV {row[5]} kWh)"
                    
                    self.data_mobil_cache.append({
                        "id": row[0], "nama": nama, "harga": row[2], "stok": row[3]
                    })
            self.filter_produk()
        except Exception as e:
            print(f"Gagal load data: {e}")

    def filter_produk(self):
        keyword = self.search_input.text().lower()
        hasil = [m for m in self.data_mobil_cache if keyword in m['nama'].lower()]
        self.table_search.setRowCount(0)
        for row, data in enumerate(hasil):
            self.table_search.insertRow(row)
            self.table_search.setItem(row, 0, QTableWidgetItem(str(data['id'])))
            self.table_search.setItem(row, 1, QTableWidgetItem(data['nama']))
            self.table_search.setItem(row, 2, QTableWidgetItem(f"{data['harga']:,}"))
            
            btn = QtWidgets.QPushButton("Pilih")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setStyleSheet("background-color: #007bff; color: white; border-radius: 3px;")
            btn.clicked.connect(lambda _, d=data: self.tambah_ke_keranjang(d))
            self.table_search.setCellWidget(row, 3, btn)

    def tambah_ke_keranjang(self, data):
        target_id = str(data['id'])
        harga_satuan = int(data['harga'])
        stok_tersedia = int(data['stok'])
        
        row_found = -1
        for i in range(self.table_cart.rowCount()):
            item_id = self.table_cart.item(i, 0).text()
            if item_id == target_id:
                row_found = i
                break
        
        if row_found >= 0:
            current_qty = int(self.table_cart.item(row_found, 3).text())
            if current_qty + 1 > stok_tersedia:
                QMessageBox.warning(None, "Stok Habis", f"Stok hanya tersedia {stok_tersedia} unit!")
                return

            new_qty = current_qty + 1
            new_subtotal = new_qty * harga_satuan
            
            self.table_cart.setItem(row_found, 3, QTableWidgetItem(str(new_qty)))
            self.table_cart.setItem(row_found, 4, QTableWidgetItem(f"{new_subtotal:,}"))
        else:
            row = self.table_cart.rowCount()
            self.table_cart.insertRow(row)
            
            self.table_cart.setItem(row, 0, QTableWidgetItem(str(target_id)))
            self.table_cart.setItem(row, 1, QTableWidgetItem(data['nama']))
            self.table_cart.setItem(row, 2, QTableWidgetItem(f"{harga_satuan:,}"))
            self.table_cart.setItem(row, 3, QTableWidgetItem("1"))
            self.table_cart.setItem(row, 4, QTableWidgetItem(f"{harga_satuan:,}"))
            
            btn_del = QtWidgets.QPushButton("Hapus")
            btn_del.setCursor(QtCore.Qt.PointingHandCursor)
            btn_del.setStyleSheet("background-color: #dc3545; color: white; border-radius: 3px;")
            btn_del.clicked.connect(lambda _, b=btn_del: self.hapus_dari_keranjang(b))
            self.table_cart.setCellWidget(row, 5, btn_del)

        self.hitung_total_belanja()

    def hapus_dari_keranjang(self, tombol_yg_diklik):
        if tombol_yg_diklik:
            idx = self.table_cart.indexAt(tombol_yg_diklik.pos())
            if idx.isValid(): 
                self.table_cart.removeRow(idx.row())
            self.hitung_total_belanja()

    def hitung_total_belanja(self):
        total = 0
        for i in range(self.table_cart.rowCount()):
            try:
                subtotal_text = self.table_cart.item(i, 4).text().replace(",", "")
                total += int(subtotal_text)
            except ValueError:
                pass
        self.label_total.setText(f"{total:,}")
        self.hitung_kembalian()

    def hitung_kembalian(self):
        try:
            total = int(self.label_total.text().replace(",", ""))
            diskon = int(self.line_diskon.text()) if self.line_diskon.text() else 0
            bayar = int(self.line_nominal.text()) if self.line_nominal.text() else 0
            grand = max(total - diskon, 0)
            kembali = bayar - grand
            self.label_kembalian.setText(f"{kembali:,}")
            
            if kembali < 0: 
                self.label_kembalian.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
            else: 
                self.label_kembalian.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
            
            return grand, bayar, kembali, diskon
        except: 
            return 0,0,0,0

    def proses_transaksi(self):
        if not self.line_nama.text() or self.table_cart.rowCount() == 0:
            QMessageBox.warning(None, "Info", "Data pelanggan atau keranjang kosong")
            return

        grand, bayar, kembali, diskon = self.hitung_kembalian()
        
        if kembali < 0:
            QMessageBox.warning(None, "Info", "Uang pembayaran kurang!")
            return
        
        items_db = []
        items_nota = []
        
        for i in range(self.table_cart.rowCount()):
            id_barang = self.table_cart.item(i, 0).text()
            qty = self.table_cart.item(i, 3).text()
            subtotal = self.table_cart.item(i, 4).text().replace(",", "")
            
            items_db.append({
                "id": id_barang,
                "qty": qty,
                "subtotal": subtotal
            })
            items_nota.append({
                "nama": self.table_cart.item(i, 1).text(),
                "qty": qty,
                "subtotal": int(subtotal)
            })
            
        sukses, msg = self.logic.simpan_transaksi(
            {"nama": self.line_nama.text(), "telp": self.line_telp.text()}, items_db
        )
        
        if sukses:
            nota = NotaDialog()
            nota.set_nota_data({
                "pembeli": self.line_nama.text(), 
                "telp": self.line_telp.text(),
                "items": items_nota, 
                "total": int(self.label_total.text().replace(",","")),
                "diskon": diskon, 
                "grand_total": grand, 
                "bayar": bayar, 
                "kembali": kembali
            })
            nota.exec_()
            self.reset_form()
            self.load_data_dari_db()
        else:
            QMessageBox.critical(None, "Error", msg)

    def reset_form(self):
        self.line_nama.clear()
        self.line_telp.clear()
        self.table_cart.setRowCount(0)
        self.line_nominal.clear()
        self.line_diskon.clear()
        self.label_total.setText("0")
        self.label_kembalian.setText("0")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())