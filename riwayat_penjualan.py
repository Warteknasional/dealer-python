import sys
import datetime
import pandas as pd
from penjualan import Penjualan
from form_nota import NotaDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QHeaderView

class RiwayatPenjualan(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Laporan Riwayat Penjualan")
        self.resize(1000, 600)

        self.logic = Penjualan()
        self.all_data_cache = []
        self.filtered_data = []

        self.setup_ui()
        self.load_data_awal()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        top_layout = QtWidgets.QHBoxLayout()
        
        lbl_title = QtWidgets.QLabel("Data Penjualan")
        font_title = QtGui.QFont()
        font_title.setPointSize(14)
        font_title.setBold(True)
        lbl_title.setFont(font_title)

        self.lbl_omset = QtWidgets.QLabel("Total Omset: Rp 0")
        font_omset = QtGui.QFont()
        font_omset.setPointSize(12)
        font_omset.setBold(True)
        self.lbl_omset.setFont(font_omset)

        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        top_layout.addWidget(self.lbl_omset)
        main_layout.addLayout(top_layout)

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Periode:"))

        self.date_from = QtWidgets.QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd-MM-yyyy")
        self.date_from.setDate(QtCore.QDate.currentDate().addDays(-30))
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QtWidgets.QLabel("s/d"))

        self.date_to = QtWidgets.QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd-MM-yyyy")
        self.date_to.setDate(QtCore.QDate.currentDate())
        filter_layout.addWidget(self.date_to)

        btn_filter = QtWidgets.QPushButton("Filter")
        btn_filter.clicked.connect(self.apply_filter)
        filter_layout.addWidget(btn_filter)

        filter_layout.addStretch()

        btn_excel = QtWidgets.QPushButton("Export Excel")
        btn_excel.clicked.connect(self.export_excel)
        filter_layout.addWidget(btn_excel)

        main_layout.addLayout(filter_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Pelanggan", "Item", "Qty", "Total (Rp)", "Aksi"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        main_layout.addWidget(self.table)

    def load_data_awal(self):
        try:
            raw_data = self.logic.ambil_riwayat() 
            self.all_data_cache = []
            
            for row in raw_data:
                tgl_obj = row[0] if isinstance(row[0], datetime.datetime) else datetime.datetime.now()
                self.all_data_cache.append({
                    "date_obj": tgl_obj,
                    "tanggal_str": tgl_obj.strftime("%d-%m-%Y %H:%M"),
                    "pembeli": row[1],
                    "mobil": row[2],
                    "qty": row[3],
                    "total": row[4]
                })
            
            self.apply_filter()

        except Exception as e:
            QMessageBox.critical(self, "Error Database", f"Gagal mengambil data: {e}")

    def apply_filter(self):
        start_date = self.date_from.date().toPyDate()
        end_date = self.date_to.date().toPyDate()

        self.filtered_data = []
        total_omset = 0

        for item in self.all_data_cache:
            item_date = item['date_obj'].date()
            if start_date <= item_date <= end_date:
                self.filtered_data.append(item)
                total_omset += item['total']

        self.lbl_omset.setText(f"Total Omset: Rp {total_omset:,}".replace(",", "."))
        self.render_table()

    def render_table(self):
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.filtered_data))

        for i, row_data in enumerate(self.filtered_data):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(row_data['tanggal_str']))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(row_data['pembeli']))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(row_data['mobil']))
            
            qty_item = QtWidgets.QTableWidgetItem(str(row_data['qty']))
            qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(i, 3, qty_item)

            price_str = f"{row_data['total']:,}".replace(",", ".")
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(price_str))

            btn_nota = QtWidgets.QPushButton("Nota")
            btn_nota.setCursor(QtCore.Qt.PointingHandCursor)
            btn_nota.clicked.connect(lambda _, d=row_data: self.view_nota(d))
            self.table.setCellWidget(i, 5, btn_nota)

    def view_nota(self, data):
        nota_dialog = NotaDialog(self)
        
        dummy_items = [{
            "nama": data['mobil'],
            "qty": data['qty'],
            "subtotal": data['total']
        }]
        
        nota_data = {
            "pembeli": data['pembeli'],
            "telp": "-",
            "items": dummy_items,
            "total": data['total'],
            "diskon": 0,
            "grand_total": data['total'],
            "bayar": data['total'],
            "kembali": 0
        }
        
        nota_dialog.set_nota_data(nota_data)
        nota_dialog.exec_()

    def export_excel(self):
        if not self.filtered_data:
            QMessageBox.warning(self, "Info", "Data kosong.")
            return

        try:
            export_list = []
            for d in self.filtered_data:
                export_list.append({
                    "Tanggal": d['tanggal_str'],
                    "Nama Pelanggan": d['pembeli'],
                    "Item Mobil": d['mobil'],
                    "Jumlah (Qty)": d['qty'],
                    "Total Harga": d['total']
                })
            
            df = pd.DataFrame(export_list)
            filename, _ = QFileDialog.getSaveFileName(self, "Simpan Excel", "Laporan_Penjualan.xlsx", "Excel Files (*.xlsx)")
            
            if filename:
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Sukses", "Data berhasil diexport.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal export: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = RiwayatPenjualan()
    win.show()
    sys.exit(app.exec_())