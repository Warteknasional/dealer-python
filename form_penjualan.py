import mysql.connector 
import sys
from form_nota import NotaDialog 
from penjualan import Penjualan 
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        Dialog.setWindowTitle("Sistem Kasir Dealer")

        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)

        font_title = QtGui.QFont()
        font_title.setPointSize(20)
        font_title.setBold(True)

        font_label_big = QtGui.QFont()
        font_label_big.setPointSize(16)
        font_label_big.setBold(True)

        title = QtWidgets.QLabel("TRANSAKSI PENJUALAN")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(font_title)
        self.mainLayout.addWidget(title)

        formGroup = QtWidgets.QGroupBox("1. Informasi Pelanggan")
        formLayout = QtWidgets.QHBoxLayout()
        
        self.line_nama = QtWidgets.QLineEdit()
        self.line_nama.setPlaceholderText("Nama Lengkap Pembeli")
        
        self.line_telp = QtWidgets.QLineEdit()
        self.line_telp.setPlaceholderText("Nomor Telepon / WA")
        self.line_telp.setValidator(QtGui.QIntValidator())
        
        formLayout.addWidget(QtWidgets.QLabel("Nama:"))
        formLayout.addWidget(self.line_nama, 2)
        formLayout.addWidget(QtWidgets.QLabel("No. Telp:"))
        formLayout.addWidget(self.line_telp, 1)
        
        formGroup.setLayout(formLayout)
        self.mainLayout.addWidget(formGroup)

        splitLayout = QtWidgets.QHBoxLayout()

        leftLayout = QtWidgets.QVBoxLayout()
        
        searchGroup = QtWidgets.QGroupBox("2. Katalog Mobil")
        searchInnerLayout = QtWidgets.QVBoxLayout()
        
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Cari Merk Mobil...")
        searchInnerLayout.addWidget(self.search_input)

        self.table_search = QtWidgets.QTableWidget()
        self.table_search.setColumnCount(4)
        self.table_search.setHorizontalHeaderLabels(["ID", "Nama Mobil", "Harga", "Aksi"])
        self.table_search.setAlternatingRowColors(True)
        
        header = self.table_search.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        self.table_search.setColumnWidth(3, 80)
        self.table_search.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        searchInnerLayout.addWidget(self.table_search)
        searchGroup.setLayout(searchInnerLayout)
        
        leftLayout.addWidget(searchGroup)
        splitLayout.addLayout(leftLayout, 5)

        rightLayout = QtWidgets.QVBoxLayout()

        cartGroup = QtWidgets.QGroupBox("3. Keranjang Belanja")
        cartInnerLayout = QtWidgets.QVBoxLayout()
        
        self.table_cart = QtWidgets.QTableWidget()
        self.table_cart.setColumnCount(6)
        self.table_cart.setHorizontalHeaderLabels(["ID", "Item", "@Harga", "Qty", "Subtotal", "Hapus"])
        self.table_cart.setAlternatingRowColors(True)
        self.table_cart.setColumnHidden(0, True)
        
        headerCart = self.table_cart.horizontalHeader()
        headerCart.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        headerCart.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        headerCart.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        headerCart.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.table_cart.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        cartInnerLayout.addWidget(self.table_cart)
        cartGroup.setLayout(cartInnerLayout)
        rightLayout.addWidget(cartGroup)

        bayarGroup = QtWidgets.QGroupBox("4. Pembayaran")
        bayarForm = QtWidgets.QFormLayout()
        
        self.label_total = QtWidgets.QLabel("0")
        self.label_total.setFont(font_label_big)
        
        self.line_diskon = QtWidgets.QLineEdit()
        self.line_diskon.setValidator(QtGui.QIntValidator())
        self.line_diskon.setAlignment(QtCore.Qt.AlignRight)
        
        self.line_nominal = QtWidgets.QLineEdit()
        self.line_nominal.setValidator(QtGui.QIntValidator())
        self.line_nominal.setFont(QtGui.QFont("Arial", 12))
        self.line_nominal.setAlignment(QtCore.Qt.AlignRight)
        
        self.label_kembalian = QtWidgets.QLabel("0")
        self.label_kembalian.setFont(font_label_big)
        self.label_kembalian.setAlignment(QtCore.Qt.AlignRight)

        bayarForm.addRow("Total Belanja:", self.label_total)
        bayarForm.addRow("Diskon (Rp):", self.line_diskon)
        bayarForm.addRow("Uang Diterima:", self.line_nominal)
        bayarForm.addRow("Kembalian:", self.label_kembalian)
        
        bayarGroup.setLayout(bayarForm)
        rightLayout.addWidget(bayarGroup)

        self.btn_simpan = QtWidgets.QPushButton("PROSES TRANSAKSI & CETAK")
        self.btn_simpan.setMinimumHeight(50)
        self.btn_simpan.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font_btn = QtGui.QFont()
        font_btn.setBold(True)
        self.btn_simpan.setFont(font_btn)
        self.btn_simpan.clicked.connect(self.proses_transaksi)
        rightLayout.addWidget(self.btn_simpan)

        splitLayout.addLayout(rightLayout, 4)
        self.mainLayout.addLayout(splitLayout)

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
                if len(row) > 3 and row[3] > 0:
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
            self.table_search.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data['id'])))
            self.table_search.setItem(row, 1, QtWidgets.QTableWidgetItem(data['nama']))
            self.table_search.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{data['harga']:,}"))
            
            btn = QtWidgets.QPushButton("Pilih")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.clicked.connect(lambda _, d=data: self.tambah_ke_keranjang(d))
            self.table_search.setCellWidget(row, 3, btn)

    def tambah_ke_keranjang(self, data):
        for i in range(self.table_cart.rowCount()):
            item_id = self.table_cart.item(i, 0).text()
            if item_id == str(data['id']):
                qty_lama = int(self.table_cart.item(i, 3).text())
                harga = int(data['harga'])
                
                if qty_lama + 1 > data['stok']:
                    QtWidgets.QMessageBox.warning(None, "Stok Habis", "Stok tidak mencukupi!")
                    return

                qty_baru = qty_lama + 1
                self.table_cart.setItem(i, 3, QtWidgets.QTableWidgetItem(str(qty_baru)))
                self.table_cart.setItem(i, 4, QtWidgets.QTableWidgetItem(str(qty_baru * harga)))
                self.hitung_total_belanja()
                return

        row = self.table_cart.rowCount()
        self.table_cart.insertRow(row)
        
        self.table_cart.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data['id'])))
        self.table_cart.setItem(row, 1, QtWidgets.QTableWidgetItem(data['nama']))
        self.table_cart.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data['harga'])))
        self.table_cart.setItem(row, 3, QtWidgets.QTableWidgetItem("1"))
        self.table_cart.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data['harga'])))
        
        btn_del = QtWidgets.QPushButton("Hapus")
        btn_del.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
            return grand, bayar, kembali, diskon
        except: return 0,0,0,0

    def proses_transaksi(self):
        if not self.line_nama.text() or self.table_cart.rowCount() == 0:
            QtWidgets.QMessageBox.warning(None, "Data Kurang", "Harap isi Nama Pembeli dan pilih Barang!")
            return
        grand, bayar, kembali, diskon = self.hitung_kembalian()
        if kembali < 0:
            QtWidgets.QMessageBox.warning(None, "Uang Kurang", "Nominal pembayaran kurang!")
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
            QtWidgets.QMessageBox.critical(None, "Error Database", msg)

    def reset_form(self):
        self.line_nama.clear()
        self.line_telp.clear()
        self.table_cart.setRowCount(0)
        self.line_nominal.clear()
        self.line_diskon.clear()
        self.label_total.setText("0")
        self.label_kembalian.setText("0")
        self.search_input.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())