from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_point(object):
    def setupUi(self, pointui):
        pointui.setObjectName("pointui")
        pointui.resize(200, 300)
        pointui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.pointMainTitle = QtWidgets.QLabel(pointui)
        self.pointMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pointMainTitle.setFont(font)
        self.pointMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.pointMainTitle.setObjectName("pointMainTitle")
        self.coordinatesTitle = QtWidgets.QLabel(pointui)
        self.coordinatesTitle.setGeometry(QtCore.QRect(70, 40, 70, 20))
        self.coordinatesTitle.setObjectName("coordinatesTitle")
        self.xlineEdit = QtWidgets.QLineEdit(pointui)
        self.xlineEdit.setGeometry(QtCore.QRect(15, 80, 70, 20))
        self.xlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.xlineEdit.setObjectName("xlineEdit")
        self.xlineEdit.setValidator(QtGui.QDoubleValidator())
        self.ylineEdit = QtWidgets.QLineEdit(pointui)
        self.ylineEdit.setGeometry(QtCore.QRect(115, 80, 70, 20))
        self.ylineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ylineEdit.setObjectName("ylineEdit")
        self.ylineEdit.setValidator(QtGui.QDoubleValidator())
        self.yTitle = QtWidgets.QLabel(pointui)
        self.yTitle.setGeometry(QtCore.QRect(120, 60, 70, 20))
        self.yTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.yTitle.setObjectName("yTitle")
        self.xTitle = QtWidgets.QLabel(pointui)
        self.xTitle.setGeometry(QtCore.QRect(20, 60, 70, 20))
        self.xTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.xTitle.setObjectName("xTitle")

        self.addpointpushButton = QtWidgets.QPushButton(pointui)
        self.addpointpushButton.setAutoDefault(True)
        self.addpointpushButton.setGeometry(QtCore.QRect(60, 120, 80, 23))
        self.addpointpushButton.setObjectName("addlinepushButton")

        self.retranslateUi(pointui)
        QtCore.QMetaObject.connectSlotsByName(pointui)

    def retranslateUi(self, pointui):
        _translate = QtCore.QCoreApplication.translate
        self.pointMainTitle.setText(_translate("MainWindow", "Point"))
        self.coordinatesTitle.setText(
            _translate("MainWindow", "Coordinates :"))
        self.yTitle.setText(_translate("MainWindow", "Y :"))
        self.xTitle.setText(_translate("MainWindow", "X : "))
        self.addpointpushButton.setText(_translate("MainWindow", "Add Point"))


class PointDisplay(QMainWindow, Ui_point):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
