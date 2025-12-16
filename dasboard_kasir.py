import sys
from form_penjualan import Ui_Dialog as Ui_FormPenjualan
from riwayat_penjualan import RiwayatPenjualan
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 450)
        Dialog.setStyleSheet("background-color: #f8f9fa;") 
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 30, 850, 50))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("💸 DASHBOARD KASIR")
        self.label.setStyleSheet("color: #333;") 
        self.groupMenu = QtWidgets.QGroupBox(Dialog)
        self.groupMenu.setGeometry(QtCore.QRect(50, 100, 380, 250))
        self.groupMenu.setTitle("Menu Transaksi")
        self.groupMenu.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #dcdcdc; 
                border-radius: 8px; 
                margin-top: 10px; 
                background-color: white;
                font-weight: bold;
                color: #555;
            } 
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px; 
            }
        """)
        style_default = """
            QPushButton { 
                background-color: #ffffff; 
                border: 1px solid #ced4da; 
                color: #495057; 
                border-radius: 6px; 
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover { 
                background-color: #e9ecef; 
                border: 1px solid #adb5bd;
            }
        """
        self.btn_jual = QtWidgets.QPushButton(self.groupMenu)
        self.btn_jual.setGeometry(QtCore.QRect(40, 60, 300, 60))
        self.btn_jual.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_jual.setObjectName("btn_jual")
        self.btn_jual.setText("  Transaksi Penjualan Baru")
        self.btn_jual.setStyleSheet(style_default)
        
        self.btn_riwayat = QtWidgets.QPushButton(self.groupMenu)
        self.btn_riwayat.setGeometry(QtCore.QRect(40, 140, 300, 60))
        self.btn_riwayat.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_riwayat.setObjectName("btn_riwayat")
        self.btn_riwayat.setText("  Laporan & Riwayat")
        self.btn_riwayat.setStyleSheet(style_default)
        
        self.groupSystem = QtWidgets.QGroupBox(Dialog)
        self.groupSystem.setGeometry(QtCore.QRect(480, 100, 320, 150))
        self.groupSystem.setTitle("Sistem")
        self.groupSystem.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #dcdcdc; 
                border-radius: 8px; 
                margin-top: 10px; 
                background-color: white;
                font-weight: bold;
                color: #555;
            }
        """)

        style_logout = """
            QPushButton { 
                background-color: #fff5f5; 
                border: 1px solid #ffcccc; 
                color: #e02424; 
                border-radius: 6px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #fee2e2; 
                border: 1px solid #f8b4b4;
            }
        """

        # Tombol Logout
        self.btn_logout = QtWidgets.QPushButton(self.groupSystem)
        self.btn_logout.setGeometry(QtCore.QRect(35, 50, 250, 70))
        self.btn_logout.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_logout.setObjectName("btn_logout")
        self.btn_logout.setText("🚪 Log Out")
        self.btn_logout.setStyleSheet(style_logout)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setWindowTitle("Dashboard Kasir")


class DashboardKasirForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Connect Tombol ke Fungsi
        self.ui.btn_jual.clicked.connect(self.buka_form_jual)
        self.ui.btn_riwayat.clicked.connect(self.buka_riwayat)
        self.ui.btn_logout.clicked.connect(self.aksi_logout)

    def buka_form_jual(self):
        try:
            self.window_jual = QtWidgets.QDialog()
            self.ui_jual = Ui_FormPenjualan()
            self.ui_jual.setupUi(self.window_jual)
            self.window_jual.exec_() 
        except NameError:
            self.show_error("Ui_FormPenjualan (form_penjualan.py)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka form penjualan:\n{e}")

    def buka_riwayat(self):
        try:
            self.window_riwayat = RiwayatPenjualan()
            self.window_riwayat.show()
        except NameError:
            self.show_error("RiwayatPenjualan (riwayat_penjualan.py)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka riwayat:\n{e}")

    def aksi_logout(self):
        tanya = QMessageBox.question(
            self, "Konfirmasi", "Yakin ingin mengakhiri sesi kasir?",
            QMessageBox.Yes | QMessageBox.No
        )
        if tanya == QMessageBox.Yes:
            self.close()

    def show_error(self, form_name):
        QMessageBox.critical(self, "Error", f"Class '{form_name}' tidak ditemukan.\nPastikan file import sudah benar dan berada di folder yang sama.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardKasirForm()
    window.show()
    sys.exit(app.exec_())