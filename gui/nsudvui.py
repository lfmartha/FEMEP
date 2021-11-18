from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_nsudv(object):
    def setupUi(self, nsudvui):
        nsudvui.setObjectName("nsudvui")
        nsudvui.resize(200, 300)
        nsudvui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.nsudvMainTitle = QtWidgets.QLabel(nsudvui)
        self.nsudvMainTitle.setGeometry(QtCore.QRect(0, 10, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nsudvMainTitle.setFont(font)
        self.nsudvMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.nsudvMainTitle.setObjectName("nsudvMainTitle")
        self.valueTitle = QtWidgets.QLabel(nsudvui)
        self.valueTitle.setGeometry(QtCore.QRect(80, 40, 100, 20))
        self.valueTitle.setObjectName("valueTitle")
        self.valuelineEdit = QtWidgets.QLineEdit(nsudvui)
        self.valuelineEdit.setGeometry(QtCore.QRect(60, 70, 80, 20))
        self.valuelineEdit.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.valuelineEdit.setObjectName("valuelineEdit")
        self.valuelineEdit.setValidator(QtGui.QIntValidator())

        self.ratioTitle = QtWidgets.QLabel(nsudvui)
        self.ratioTitle.setGeometry(QtCore.QRect(80, 100, 100, 20))
        self.ratioTitle.setObjectName("ratioTitle")
        self.ratiolineEdit = QtWidgets.QLineEdit(nsudvui)
        self.ratiolineEdit.setGeometry(QtCore.QRect(60, 130, 80, 20))
        self.ratiolineEdit.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.ratiolineEdit.setObjectName("ratiolineEdit")
        self.ratiolineEdit.setValidator(QtGui.QDoubleValidator())

        self.nsudvpushButton = QtWidgets.QPushButton(nsudvui)
        self.nsudvpushButton.setAutoDefault(True)
        self.nsudvpushButton.setGeometry(QtCore.QRect(60, 170, 80, 23))
        self.nsudvpushButton.setObjectName("addlinepushButton")

        self.retranslateUi(nsudvui)
        QtCore.QMetaObject.connectSlotsByName(nsudvui)

    def retranslateUi(self, nsudvui):
        _translate = QtCore.QCoreApplication.translate
        self.nsudvMainTitle.setText(_translate(
            "MainWindow", "Number of Subdivisions"))
        self.valueTitle.setText(
            _translate("MainWindow", "Value :"))
        self.ratioTitle.setText(
            _translate("MainWindow", "Ratio :"))
        self.nsudvpushButton.setText(_translate("MainWindow", "OK"))


class NsudvDisplay(QMainWindow, Ui_nsudv):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
