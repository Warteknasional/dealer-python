import mysql.connector
import sys
from form_insert_user import InsertUserForm
from form_edit_user import EditUserForm
from form_delete_user import DeleteUserForm
from form_view_user import ViewUserForm
from riwayat_penjualan import RiwayatPenjualan
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 600)
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 40, 850, 50))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("color: #2c3e50;")
        
        self.groupUser = QtWidgets.QGroupBox(Dialog)
        self.groupUser.setGeometry(QtCore.QRect(50, 120, 350, 400))
        self.groupUser.setTitle("Kelola Pengguna")
        self.groupUser.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #ccc; border-radius: 8px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")

        self.btn_insert = QtWidgets.QPushButton(self.groupUser)
        self.btn_insert.setGeometry(QtCore.QRect(25, 40, 300, 45))
        
        self.btn_update = QtWidgets.QPushButton(self.groupUser)
        self.btn_update.setGeometry(QtCore.QRect(25, 100, 300, 45))
        
        self.btn_delete = QtWidgets.QPushButton(self.groupUser)
        self.btn_delete.setGeometry(QtCore.QRect(25, 160, 300, 45))
        
        self.btn_view = QtWidgets.QPushButton(self.groupUser)
        self.btn_view.setGeometry(QtCore.QRect(25, 220, 300, 45))

        self.groupLaporan = QtWidgets.QGroupBox(Dialog)
        self.groupLaporan.setGeometry(QtCore.QRect(450, 120, 350, 150))
        self.groupLaporan.setTitle("Laporan & Transaksi")
        self.groupLaporan.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #ccc; border-radius: 8px; margin-top: 10px; }")

        self.btn_riwayat = QtWidgets.QPushButton(self.groupLaporan)
        self.btn_riwayat.setGeometry(QtCore.QRect(25, 40, 300, 80))
        self.btn_riwayat.setStyleSheet("background-color: #d1ecf1; color: #0c5460; font-weight: bold; font-size: 14px; border-radius: 5px;")
        
        self.btn_logout = QtWidgets.QPushButton(Dialog)
        self.btn_logout.setGeometry(QtCore.QRect(450, 350, 350, 100))
        self.btn_logout.setStyleSheet("background-color: #f8d7da; color: #721c24; font-weight: bold; font-size: 16px; border-radius: 8px;")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dashboard Admin"))
        self.label.setText(_translate("Dialog", "DASHBOARD ADMIN"))
        
        self.btn_insert.setText(_translate("Dialog", "Insert Data User"))
        self.btn_update.setText(_translate("Dialog", "Update Data User"))
        self.btn_delete.setText(_translate("Dialog", "Delete Data User"))
        self.btn_view.setText(_translate("Dialog", "Lihat Data User"))
        
        self.btn_riwayat.setText(_translate("Dialog", "Riwayat Penjualan\n(Cek Omset & Export Excel)"))
        self.btn_logout.setText(_translate("Dialog", "LOGOUT"))

class DashboardAdminForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.btn_insert.clicked.connect(self.buka_insert)
        self.ui.btn_update.clicked.connect(self.buka_update)
        self.ui.btn_delete.clicked.connect(self.buka_delete)
        self.ui.btn_view.clicked.connect(self.buka_view)
        self.ui.btn_riwayat.clicked.connect(self.buka_riwayat)
        self.ui.btn_logout.clicked.connect(self.aksi_logout)

    def buka_insert(self):
        try:
            self.form = InsertUserForm()
            self.form.exec_()
        except NameError: self.show_error("InsertUserForm")

    def buka_update(self):
        try:
            self.form = EditUserForm()
            self.form.exec_()
        except NameError: self.show_error("EditUserForm")

    def buka_delete(self):
        try:
            self.form = DeleteUserForm()
            self.form.exec_()
        except NameError: self.show_error("DeleteUserForm")

    def buka_view(self):
        try:
            self.form = ViewUserForm()
            self.form.exec_()
        except NameError: self.show_error("ViewUserForm")

    def buka_riwayat(self):
        try:
            self.window_riwayat = RiwayatPenjualan()
            self.window_riwayat.show() 
        except NameError: 
            self.show_error("RiwayatPenjualan")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuka riwayat: {e}")

    def aksi_logout(self):
        tanya = QMessageBox.question(
            self, "Konfirmasi", "Yakin ingin keluar dari sistem?",
            QMessageBox.Yes | QMessageBox.No
        )
        if tanya == QMessageBox.Yes:
            self.close()

    def show_error(self, form_name):
        QMessageBox.critical(self, "Error", f"File/Class '{form_name}' tidak ditemukan.\nPastikan file sudah dibuat dan diimport.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardAdminForm()
    window.show()
    sys.exit(app.exec_())