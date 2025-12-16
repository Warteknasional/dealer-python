import sys
from form_insert_barang import InsertBarangForm
from form_edit_barang import EditBarangForm
from form_delete_barang import DeleteBarangForm
from form_view_barang import ViewBarangForm
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 550)
        Dialog.setStyleSheet("background-color: #f8f9fa;") 
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 30, 850, 50))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: #333;") 
        
        self.groupBarang = QtWidgets.QGroupBox(Dialog)
        self.groupBarang.setGeometry(QtCore.QRect(50, 100, 380, 400))
        self.groupBarang.setTitle("Manajemen Stok Barang")
        self.groupBarang.setStyleSheet("""
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
            }
            QPushButton:hover { 
                background-color: #e9ecef; 
                border: 1px solid #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """

        # Tombol 1: Insert
        self.btn_insert = QtWidgets.QPushButton(self.groupBarang)
        self.btn_insert.setGeometry(QtCore.QRect(40, 50, 300, 55))
        self.btn_insert.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_insert.setObjectName("btn_insert")
        self.btn_insert.setStyleSheet(style_default)
        # Tombol 2: Update
        self.btn_update = QtWidgets.QPushButton(self.groupBarang)
        self.btn_update.setGeometry(QtCore.QRect(40, 120, 300, 55))
        self.btn_update.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_update.setObjectName("btn_update")
        self.btn_update.setStyleSheet(style_default)
        # Tombol 3: Delete
        self.btn_delete = QtWidgets.QPushButton(self.groupBarang)
        self.btn_delete.setGeometry(QtCore.QRect(40, 190, 300, 55))
        self.btn_delete.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setStyleSheet(style_default)
        # Tombol 4: View
        self.btn_view = QtWidgets.QPushButton(self.groupBarang)
        self.btn_view.setGeometry(QtCore.QRect(40, 260, 300, 55))
        self.btn_view.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_view.setObjectName("btn_view")
        self.btn_view.setStyleSheet(style_default)
        # --- GROUP KANAN: SISTEM / INFO ---
        self.groupSystem = QtWidgets.QGroupBox(Dialog)
        self.groupSystem.setGeometry(QtCore.QRect(480, 100, 320, 180))
        self.groupSystem.setTitle("Sistem Gudang")
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

        self.btn_logout = QtWidgets.QPushButton(self.groupSystem)
        self.btn_logout.setGeometry(QtCore.QRect(35, 50, 250, 80))
        self.btn_logout.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_logout.setObjectName("btn_logout")
        self.btn_logout.setStyleSheet(style_logout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dashboard Gudang"))
        self.label.setText(_translate("Dialog", "DASHBOARD GUDANG"))
        
        self.btn_insert.setText(_translate("Dialog", "Insert Barang Baru"))
        self.btn_update.setText(_translate("Dialog", "Update Stok / Harga"))
        self.btn_delete.setText(_translate("Dialog", "Hapus Data Barang"))
        self.btn_view.setText(_translate("Dialog", "Lihat Semua Barang"))
        
        self.btn_logout.setText(_translate("Dialog", "Log Out"))

class DashboardGudangForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.btn_insert.clicked.connect(self.buka_insert)
        self.ui.btn_update.clicked.connect(self.buka_update)
        self.ui.btn_delete.clicked.connect(self.buka_delete)
        self.ui.btn_view.clicked.connect(self.buka_view)
        self.ui.btn_logout.clicked.connect(self.aksi_logout)

    def buka_insert(self):
        try:
            self.form = InsertBarangForm()
            self.form.exec_()
        except NameError: self.show_error("InsertBarangForm")

    def buka_update(self):
        try:
            self.form = EditBarangForm()
            self.form.exec_()
        except NameError: self.show_error("EditBarangForm")

    def buka_delete(self):
        try:
            self.form = DeleteBarangForm()
            self.form.exec_()
        except NameError: self.show_error("DeleteBarangForm")

    def buka_view(self):
        try:
            self.form = ViewBarangForm()
            self.form.exec_()
        except NameError: self.show_error("ViewBarangForm")

    def aksi_logout(self):
        tanya = QMessageBox.question(
            self, "Konfirmasi", "Yakin ingin keluar?",
            QMessageBox.Yes | QMessageBox.No
        )
        if tanya == QMessageBox.Yes:
            self.close()
            
    def show_error(self, form_name):
        QMessageBox.critical(self, "Error", f"Class '{form_name}' tidak ditemukan.\nPastikan file import sudah benar.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardGudangForm()
    window.show()
    sys.exit(app.exec_())