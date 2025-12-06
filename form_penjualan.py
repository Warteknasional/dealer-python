# -*- coding: utf-8 -*-

# --- IMPORT DRIVER DI SINI (PALING ATAS - ANTI CRASH) ---
import mysql.connector 

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from form_nota import NotaDialog 
from penjualan import Penjualan 

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 700) # Sedikit diperlebar
        Dialog.setWindowTitle("SISTEM KASIR DEALER")

        mainLayout = QtWidgets.QVBoxLayout(Dialog)

        # JUDUL
        title = QtWidgets.QLabel("TRANSAKSI PENJUALAN")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        mainLayout.addWidget(title)

        # === BAGIAN 1: DATA PEMBELI ===
        formGroup = QtWidgets.QGroupBox("Informasi Pelanggan")
        formLayout = QtWidgets.QFormLayout()
        self.line_nama = QtWidgets.QLineEdit()
        self.line_telp = QtWidgets.QLineEdit()
        self.line_telp.setValidator(QtGui.QIntValidator())
        formLayout.addRow("Nama Pembeli:", self.line_nama)
        formLayout.addRow("No. Telepon:", self.line_telp)
        formGroup.setLayout(formLayout)
        mainLayout.addWidget(formGroup)

        # === BAGIAN 2: PENCARIAN PRODUK ===
        searchGroup = QtWidgets.QGroupBox("Cari Mobil")
        searchLayout = QtWidgets.QVBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Ketik merk mobil...")
        searchLayout.addWidget(self.search_input)

        self.table_search = QtWidgets.QTableWidget()
        self.table_search.setColumnCount(4)
        self.table_search.setHorizontalHeaderLabels(["ID", "Nama Mobil", "Harga", "Aksi"])
        self.table_search.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table_search.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        searchLayout.addWidget(self.table_search)
        searchGroup.setLayout(searchLayout)
        mainLayout.addWidget(searchGroup)

        # === BAGIAN 3: KERANJANG ===
        cartGroup = QtWidgets.QGroupBox("Keranjang Belanja")
        cartLayout = QtWidgets.QVBoxLayout()
        self.table_cart = QtWidgets.QTableWidget()
        self.table_cart.setColumnCount(6)
        self.table_cart.setHorizontalHeaderLabels(["ID", "Nama Produk", "Harga", "Qty", "Subtotal", "Aksi"])
        self.table_cart.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table_cart.setColumnHidden(0, True) # Hidden ID
        self.table_cart.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        cartLayout.addWidget(self.table_cart)
        cartGroup.setLayout(cartLayout)
        mainLayout.addWidget(cartGroup)

        # === BAGIAN 4: PEMBAYARAN ===
        bayarGroup = QtWidgets.QGroupBox("Rincian Pembayaran")
        bayarForm = QtWidgets.QFormLayout()
        self.label_total = QtWidgets.QLabel("0")
        self.label_total.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")
        self.line_diskon = QtWidgets.QLineEdit()
        self.line_diskon.setValidator(QtGui.QIntValidator())
        self.line_nominal = QtWidgets.QLineEdit()
        self.line_nominal.setValidator(QtGui.QIntValidator())
        self.label_kembalian = QtWidgets.QLabel("0")
        self.label_kembalian.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        bayarForm.addRow("Total Belanja (Rp):", self.label_total)
        bayarForm.addRow("Diskon (Rp):", self.line_diskon)
        bayarForm.addRow("Bayar (Rp):", self.line_nominal)
        bayarForm.addRow("Kembalian (Rp):", self.label_kembalian)
        bayarGroup.setLayout(bayarForm)
        mainLayout.addWidget(bayarGroup)

        # TOMBOL PROSES
        self.btn_simpan = QtWidgets.QPushButton("CETAK NOTA & SIMPAN")
        self.btn_simpan.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 12px;")
        self.btn_simpan.clicked.connect(self.proses_transaksi)
        mainLayout.addWidget(self.btn_simpan)

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
                if row[3] > 0: # Stok > 0
                    nama = row[1]
                    # Cek Sport/Listrik (Index 4 & 5)
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
            self.table_search.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data['id'])))
            self.table_search.setItem(row, 1, QtWidgets.QTableWidgetItem(data['nama']))
            self.table_search.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{data['harga']:,}"))
            
            btn = QtWidgets.QPushButton("Pilih")
            btn.setStyleSheet("background-color: #007bff; color: white;")
            btn.clicked.connect(lambda _, d=data: self.tambah_ke_keranjang(d))
            self.table_search.setCellWidget(row, 3, btn)

    def tambah_ke_keranjang(self, data):
        row = self.table_cart.rowCount()
        self.table_cart.insertRow(row)
        
        # Masukkan Data
        self.table_cart.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data['id'])))
        self.table_cart.setItem(row, 1, QtWidgets.QTableWidgetItem(data['nama']))
        self.table_cart.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data['harga'])))
        self.table_cart.setItem(row, 3, QtWidgets.QTableWidgetItem("1"))
        self.table_cart.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data['harga'])))
        
        # --- PERBAIKAN TOMBOL HAPUS ---
        btn_del = QtWidgets.QPushButton("Hapus")
        btn_del.setStyleSheet("background-color: #dc3545; color: white;")
        
        # Kita pakai LAMBDA agar tombol spesifik dikirim ke fungsi
        # 'b=btn_del' artinya kita simpan tombol ini ke variabel 'b'
        btn_del.clicked.connect(lambda _, b=btn_del: self.hapus_dari_keranjang(b))
        
        self.table_cart.setCellWidget(row, 5, btn_del)
        self.hitung_total_belanja()

    def hapus_dari_keranjang(self, tombol_yg_diklik):
        # --- PERBAIKAN LOGIC HAPUS ---
        # Kita tidak pakai self.sender() lagi, tapi pakai parameter 'tombol_yg_diklik'
        if tombol_yg_diklik:
            idx = self.table_cart.indexAt(tombol_yg_diklik.pos())
            if idx.isValid(): 
                self.table_cart.removeRow(idx.row())
            self.hitung_total_belanja()

    def hitung_total_belanja(self):
        total = 0
        for i in range(self.table_cart.rowCount()):
            try: total += int(self.table_cart.item(i, 4).text())
            except: pass
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
            if kembali < 0: self.label_kembalian.setStyleSheet("color: red; font-size: 18px;")
            else: self.label_kembalian.setStyleSheet("color: green; font-size: 18px;")
            return grand, bayar, kembali, diskon
        except: return 0,0,0,0

    def proses_transaksi(self):
        if not self.line_nama.text() or self.table_cart.rowCount() == 0:
            QtWidgets.QMessageBox.warning(None, "Info", "Data tidak lengkap")
            return
        grand, bayar, kembali, diskon = self.hitung_kembalian()
        if kembali < 0:
            QtWidgets.QMessageBox.warning(None, "Info", "Uang kurang")
            return
        
        items_db = []
        items_nota = []
        for i in range(self.table_cart.rowCount()):
            items_db.append({
                "id": self.table_cart.item(i, 0).text(),
                "qty": self.table_cart.item(i, 3).text(),
                "subtotal": self.table_cart.item(i, 4).text()
            })
            items_nota.append({
                "nama": self.table_cart.item(i, 1).text(),
                "qty": self.table_cart.item(i, 3).text(),
                "subtotal": int(self.table_cart.item(i, 4).text())
            })
            
        sukses, msg = self.logic.simpan_transaksi(
            {"nama": self.line_nama.text(), "telp": self.line_telp.text()}, items_db
        )
        
        if sukses:
            nota = NotaDialog()
            nota.set_nota_data({
                "pembeli": self.line_nama.text(), "telp": self.line_telp.text(),
                "items": items_nota, "total": int(self.label_total.text().replace(",","")),
                "diskon": diskon, "grand_total": grand, "bayar": bayar, "kembali": kembali
            })
            nota.exec_()
            self.reset_form()
            self.load_data_dari_db()
        else:
            QtWidgets.QMessageBox.critical(None, "Error", msg)

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