import sys
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class NotaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cetak Nota")
        self.resize(400, 600)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.text_area.setStyleSheet("""
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            font-family: 'Consolas', 'Monospace'; 
            font-size: 11px;
            padding: 15px;
            color: #333;
        """)
        layout.addWidget(self.text_area)

        self.btn_print = QtWidgets.QPushButton("Tutup / Print")
        self.btn_print.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_print.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50; 
                color: white; 
                padding: 12px;
                font-weight: bold;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        self.btn_print.clicked.connect(self.accept)
        layout.addWidget(self.btn_print)

    def format_rupiah(self, nominal):
        return f"{nominal:,}".replace(",", ".")

    def set_nota_data(self, data):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        W = 40
        GARIS = "=" * W
        MINUS = "-" * W

        txt  = f"{'DEALER MAJU JAYA'.center(W)}\n"
        txt += f"{'Jl. Raya Utama No. 123'.center(W)}\n"
        txt += f"{GARIS}\n"
        txt += f"Tgl : {now}\n"
        txt += f"Plg : {data['pembeli']}\n"
        txt += f"Tel : {data['telp']}\n"
        txt += f"{MINUS}\n"
        
        for item in data['items']:
            nama = item['nama'][:38]
            qty = str(item['qty'])
            sub = self.format_rupiah(item['subtotal'])
            
            txt += f"{nama}\n"
            txt += f"{qty}x {sub:>36}\n"

        txt += f"{MINUS}\n"

        def row(label, val):
            return f"{label:<15} : {self.format_rupiah(val):>21}\n"

        txt += row("TOTAL", data['total'])
        txt += row("DISKON", data['diskon'])
        txt += f"{MINUS}\n"
        txt += row("GRAND TOTAL", data['grand_total'])
        txt += row("TUNAI", data['bayar'])
        txt += row("KEMBALI", data['kembali'])
        
        txt += f"{GARIS}\n"
        txt += f"{'TERIMA KASIH'.center(W)}\n"
        txt += f"{'Simpan struk ini sebagai bukti'.center(W)}\n"

        self.text_area.setText(txt)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = NotaDialog()
    win.set_nota_data()
    win.show()
    sys.exit(app.exec_())