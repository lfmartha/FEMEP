from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_polyline(object):
    def setupUi(self, polylineui):
        polylineui.setObjectName("polylineUi")
        polylineui.resize(200, 300)
        polylineui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.firstpointXlineEdit = QtWidgets.QLineEdit(polylineui)
        self.firstpointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.firstpointXlineEdit.setGeometry(QtCore.QRect(15, 80, 70, 20))
        self.firstpointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "")
        self.firstpointXlineEdit.setObjectName("firstpointXlineEdit")
        self.firstpointYlineEdit = QtWidgets.QLineEdit(polylineui)
        self.firstpointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.firstpointYlineEdit.setGeometry(QtCore.QRect(115, 80, 70, 20))
        self.firstpointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "")
        self.firstpointYlineEdit.setObjectName("firstYlineEdit")
        self.firstpointXTitle = QtWidgets.QLabel(polylineui)
        self.firstpointXTitle.setGeometry(QtCore.QRect(20, 60, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.firstpointXTitle.setFont(font)
        self.firstpointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                            "")
        self.firstpointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointXTitle.setObjectName("firstpointXTitle")
        self.firstpointYTitle = QtWidgets.QLabel(polylineui)
        self.firstpointYTitle.setGeometry(QtCore.QRect(120, 60, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.firstpointYTitle.setFont(font)
        self.firstpointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                            "")
        self.firstpointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointYTitle.setObjectName("firstpointYTitle")
        self.PolylineMainTitle = QtWidgets.QLabel(polylineui)
        self.PolylineMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PolylineMainTitle.setFont(font)
        self.PolylineMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.PolylineMainTitle.setObjectName("PolylineMainTitle")
        self.endpointYTitle = QtWidgets.QLabel(polylineui)
        self.endpointYTitle.setGeometry(QtCore.QRect(120, 140, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.endpointYTitle.setFont(font)
        self.endpointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                          "")
        self.endpointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointYTitle.setObjectName("endpointYTitle")
        self.endpointXTitle = QtWidgets.QLabel(polylineui)
        self.endpointXTitle.setGeometry(QtCore.QRect(20, 140, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.endpointXTitle.setFont(font)
        self.endpointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                          "")
        self.endpointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointXTitle.setObjectName("endpointXTitle")
        self.endpointXlineEdit = QtWidgets.QLineEdit(polylineui)
        self.endpointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.endpointXlineEdit.setGeometry(QtCore.QRect(15, 160, 70, 20))
        self.endpointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "")
        self.endpointXlineEdit.setObjectName("endpointXlineEdit")
        self.endpointYlineEdit = QtWidgets.QLineEdit(polylineui)
        self.endpointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.endpointYlineEdit.setGeometry(QtCore.QRect(115, 160, 70, 20))
        self.endpointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "")
        self.endpointYlineEdit.setObjectName("endpointYlineEdit")
        self.addlinepushButton = QtWidgets.QPushButton(polylineui)
        self.addlinepushButton.setAutoDefault(True)
        self.addlinepushButton.setGeometry(QtCore.QRect(15, 200, 80, 23))
        self.addlinepushButton.setObjectName("addlinepushButton")
        self.firstpointTitle = QtWidgets.QLabel(polylineui)
        self.firstpointTitle.setGeometry(QtCore.QRect(70, 40, 70, 13))
        self.firstpointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointTitle.setObjectName("firstpointTitle")
        self.endpointTitle = QtWidgets.QLabel(polylineui)
        self.endpointTitle.setGeometry(QtCore.QRect(70, 120, 70, 13))
        self.endpointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointTitle.setObjectName("endpointTitle")
        self.endsegmenttpushButton = QtWidgets.QPushButton(polylineui)
        self.endsegmenttpushButton.setAutoDefault(True)
        self.endsegmenttpushButton.setGeometry(QtCore.QRect(105, 200, 80, 23))
        self.endsegmenttpushButton.setObjectName("endsegmenttpushButton")

        self.retranslateUi(polylineui)
        QtCore.QMetaObject.connectSlotsByName(polylineui)

    def retranslateUi(self, polylineui):
        _translate = QtCore.QCoreApplication.translate
        self.firstpointXTitle.setText(_translate("MainWindow", "X :"))
        self.firstpointYTitle.setText(_translate("MainWindow", "Y: "))
        self.PolylineMainTitle.setText(
            _translate("MainWindow", "Polyline"))
        self.endpointYTitle.setText(_translate("MainWindow", "Y :"))
        self.endpointXTitle.setText(_translate("MainWindow", "X :"))
        self.addlinepushButton.setText(
            _translate("MainWindow", "Add Line"))
        self.firstpointTitle.setText(
            _translate("MainWindow", "First Point :"))
        self.endpointTitle.setText(_translate("MainWindow", "End Point:"))
        self.endsegmenttpushButton.setText(
            _translate("MainWindow", "End"))


class PolylineDisplay(QMainWindow, Ui_polyline):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
