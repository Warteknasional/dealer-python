# -*- coding: utf-8 -*-
import sys
from user import User
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# --- UI ASLI ---
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 30, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Tambah User")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 90, 70, 20))
        self.label_2.setText("Nama")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(180, 90, 150, 20))

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 120, 70, 20))
        self.label_3.setText("Username")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 120, 150, 20))

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 150, 70, 20))
        self.label_4.setText("Password")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 150, 150, 20))

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(100, 180, 70, 20))
        self.label_6.setText("Posisi")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(180, 180, 150, 22))
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 230, 160, 30))
        self.pushButton.setText("Simpan")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

# --- LOGIKA OOP ---
class InsertUserForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(['admin', 'gudang', 'kasir'])
        self.ui.pushButton.clicked.connect(self.simpan_data)

    def simpan_data(self):
        # 1. Ambil input
        nama = self.ui.lineEdit.text()
        user = self.ui.lineEdit_2.text()
        pw = self.ui.lineEdit_3.text()
        posisi = self.ui.comboBox.currentText()

        # 2. Validasi
        if not nama or not user or not pw:
            QMessageBox.warning(self, "Warning", "Semua data harus diisi!")
            return

        # 3. Proses Simpan (OOP Style)
        try:
            obj_user = User()
            obj_user.name = nama       # Setter
            obj_user.username = user   # Setter
            obj_user.password = pw     # Setter
            obj_user.posisi = posisi   # Setter
            
            if obj_user.simpan():
                QMessageBox.information(self, "Sukses", "Data Berhasil Disimpan!")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.ui.lineEdit_3.clear()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal menyimpan ke database.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InsertUserForm()
    window.show()
    sys.exit(app.exec_())