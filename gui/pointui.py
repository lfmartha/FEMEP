from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_point(object):
    def setupUi(self, pointui):
        pointui.setObjectName("pointui")
        pointui.resize(200, 800)
        pointui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.PointMainTitle = QtWidgets.QLabel(pointui)
        self.PointMainTitle.setGeometry(QtCore.QRect(35, 10, 130, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PointMainTitle.setFont(font)
        self.PointMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PointMainTitle.setObjectName("PointMainTitle")

        # Point
        self.PointTitle = QtWidgets.QLabel(pointui)
        self.PointTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.PointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PointTitle.setObjectName("PointTitle")

        self.PointXTitle = QtWidgets.QLabel(pointui)
        self.PointXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.PointXTitle.setFont(font)
        self.PointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.PointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PointXTitle.setObjectName("PointXTitle")

        self.PointXlineEdit = QtWidgets.QLineEdit(pointui)
        self.PointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.PointXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.PointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.PointXlineEdit.setObjectName("PointXlineEdit")

        self.PointYTitle = QtWidgets.QLabel(pointui)
        self.PointYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.PointYTitle.setFont(font)
        self.PointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.PointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PointYTitle.setObjectName("PointYTitle")

        self.PointYlineEdit = QtWidgets.QLineEdit(pointui)
        self.PointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.PointYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.PointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.PointYlineEdit.setObjectName("PointYlineEdit")

        # Add Button
        self.addPointpushButton = QtWidgets.QPushButton(pointui)
        self.addPointpushButton.setAutoDefault(True)
        self.addPointpushButton.setGeometry(QtCore.QRect(65, 100, 70, 25))
        self.addPointpushButton.setObjectName("addPointpushButton")

        self.retranslateUi(pointui)
        QtCore.QMetaObject.connectSlotsByName(pointui)

    def retranslateUi(self, pointui):
        _translate = QtCore.QCoreApplication.translate
        self.PointMainTitle.setText(_translate("MainWindow", "Point"))

        self.PointTitle.setText(_translate("MainWindow", "Set Point:"))
        self.PointXTitle.setText(_translate("MainWindow", "X:"))
        self.PointYTitle.setText(_translate("MainWindow", "Y:"))
        self.addPointpushButton.setText(_translate("MainWindow", "Add Point"))

class PointDisplay(QMainWindow, Ui_point):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
