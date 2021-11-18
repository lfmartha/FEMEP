from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_grid(object):
    def setupUi(self, gridui):
        gridui.setObjectName("gridUi")
        gridui.resize(200, 300)
        gridui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.central_grid = QtWidgets.QWidget(gridui)
        self.gridXlineEdit = QtWidgets.QLineEdit(gridui)
        self.gridXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.gridXlineEdit.setGeometry(QtCore.QRect(50, 70, 100, 20))
        self.gridXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        self.gridXlineEdit.setObjectName("gridXlineEdit")
        self.gridYlineEdit = QtWidgets.QLineEdit(gridui)
        self.gridYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.gridYlineEdit.setGeometry(QtCore.QRect(50, 140, 100, 20))
        self.gridYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        self.gridYlineEdit.setObjectName("gridYlineEdit")
        self.gridXTitle = QtWidgets.QLabel(gridui)
        self.gridXTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.gridXTitle.setFont(font)
        self.gridXTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                      "")
        self.gridXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.gridXTitle.setObjectName("gridXTitle")
        self.gridYTitle = QtWidgets.QLabel(gridui)
        self.gridYTitle.setGeometry(QtCore.QRect(50, 110, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.gridYTitle.setFont(font)
        self.gridYTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                      "")
        self.gridYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.gridYTitle.setObjectName("gridYTitle")
        self.gridOKpushButton = QtWidgets.QPushButton(gridui)
        self.gridOKpushButton.setAutoDefault(True)
        self.gridOKpushButton.setGeometry(QtCore.QRect(60, 190, 80, 23))
        self.gridOKpushButton.setStyleSheet("color: rgb(0, 0, 0);")
        self.gridOKpushButton.setObjectName("gridOKpushButton")
        self.gridMainTitle = QtWidgets.QLabel(gridui)
        self.gridMainTitle.setGeometry(QtCore.QRect(0, 10, 200, 20))
        self.gridMainTitle.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gridMainTitle.setFont(font)
        self.gridMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.gridMainTitle.setObjectName("gridMainTitle")

        self.retranslateUi(gridui)
        QtCore.QMetaObject.connectSlotsByName(gridui)

    def retranslateUi(self, gridui):

        _translate = QtCore.QCoreApplication.translate
        self.gridXTitle.setText(_translate("MainWindow", "X Direction:"))
        self.gridYTitle.setText(_translate("MainWindow", "Y Direction:"))
        self.gridOKpushButton.setText(_translate("MainWindow", "OK"))
        self.gridMainTitle.setText(_translate(
            "MainWindow", "Grid Definition"))


class GridDisplay(QMainWindow, Ui_grid):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
