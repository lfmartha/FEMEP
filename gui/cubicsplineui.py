from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_cubicspline(object):
    def setupUi(self, cubicsplineui):
        cubicsplineui.setObjectName("cubicsplineUi")
        cubicsplineui.resize(200, 800)
        cubicsplineui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.CubicSplineMainTitle = QtWidgets.QLabel(cubicsplineui)
        self.CubicSplineMainTitle.setGeometry(QtCore.QRect(35, 10, 130, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CubicSplineMainTitle.setFont(font)
        self.CubicSplineMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CubicSplineMainTitle.setObjectName("CubicSplineMainTitle")

        # Initial Point
        self.InitialPointTitle = QtWidgets.QLabel(cubicsplineui)
        self.InitialPointTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.InitialPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.InitialPointTitle.setObjectName("InitialPointTitle")

        self.InitialPointXTitle = QtWidgets.QLabel(cubicsplineui)
        self.InitialPointXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        self.InitialPointXTitle.setFont(font)
        self.InitialPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.InitialPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.InitialPointXTitle.setObjectName("InitialPointXTitle")

        self.InitialPointXlineEdit = QtWidgets.QLineEdit(cubicsplineui)
        self.InitialPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.InitialPointXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.InitialPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.InitialPointXlineEdit.setObjectName("InitialPointXlineEdit")

        self.InitialPointYTitle = QtWidgets.QLabel(cubicsplineui)
        self.InitialPointYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.InitialPointYTitle.setFont(font)
        self.InitialPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.InitialPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.InitialPointYTitle.setObjectName("InitialPointYTitle")

        self.InitialPointYlineEdit = QtWidgets.QLineEdit(cubicsplineui)
        self.InitialPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.InitialPointYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.InitialPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.InitialPointYlineEdit.setObjectName("InitialPointYlineEdit")

        self.InitialPointpushButton = QtWidgets.QPushButton(cubicsplineui)
        self.InitialPointpushButton.setAutoDefault(True)
        self.InitialPointpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
        self.InitialPointpushButton.setObjectName("InitialPointpushButton")

        # End Point
        self.EndPointTitle = QtWidgets.QLabel(cubicsplineui)
        self.EndPointTitle.setGeometry(QtCore.QRect(50, 145, 100, 20))
        self.EndPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.EndPointTitle.setObjectName("EndPointTitle")

        self.EndPointXTitle = QtWidgets.QLabel(cubicsplineui)
        self.EndPointXTitle.setGeometry(QtCore.QRect(15, 160, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.EndPointXTitle.setFont(font)
        self.EndPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.EndPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.EndPointXTitle.setObjectName("EndPointXTitle")

        self.EndPointXlineEdit = QtWidgets.QLineEdit(cubicsplineui)
        self.EndPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.EndPointXlineEdit.setGeometry(QtCore.QRect(15, 180, 70, 20))
        self.EndPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.EndPointXlineEdit.setObjectName("EndPointXlineEdit")

        self.EndPointYTitle = QtWidgets.QLabel(cubicsplineui)
        self.EndPointYTitle.setGeometry(QtCore.QRect(115, 160, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.EndPointYTitle.setFont(font)
        self.EndPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.EndPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.EndPointYTitle.setObjectName("EndPointYTitle")

        self.EndPointYlineEdit = QtWidgets.QLineEdit(cubicsplineui)
        self.EndPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.EndPointYlineEdit.setGeometry(QtCore.QRect(115, 180, 70, 20))
        self.EndPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.EndPointYlineEdit.setObjectName("EndPointYlineEdit")

        # Add Button
        self.addCubicSplinepushButton = QtWidgets.QPushButton(cubicsplineui)
        self.addCubicSplinepushButton.setAutoDefault(True)
        self.addCubicSplinepushButton.setGeometry(QtCore.QRect(15, 205, 80, 25))
        self.addCubicSplinepushButton.setObjectName("addCubicSplinepushButton")

        # End Button
        self.endCubicSplinepushButton = QtWidgets.QPushButton(cubicsplineui)
        self.endCubicSplinepushButton.setAutoDefault(True)
        self.endCubicSplinepushButton.setGeometry(QtCore.QRect(105, 205, 80, 25))
        self.endCubicSplinepushButton.setObjectName("endCubicSplinepushButton")

        self.retranslateUi(cubicsplineui)
        QtCore.QMetaObject.connectSlotsByName(cubicsplineui)

    def retranslateUi(self, cubicsplineui):
        _translate = QtCore.QCoreApplication.translate
        self.CubicSplineMainTitle.setText(_translate("MainWindow", "Cubic B-Spline"))

        self.InitialPointTitle.setText(_translate("MainWindow", "Set Initial Point:"))
        self.InitialPointXTitle.setText(_translate("MainWindow", "X:"))
        self.InitialPointYTitle.setText(_translate("MainWindow", "Y:"))
        self.InitialPointpushButton.setText(_translate("MainWindow", "Set"))

        self.EndPointTitle.setText(_translate("MainWindow", "Set Next Point:"))
        self.EndPointXTitle.setText(_translate("MainWindow", "X:"))
        self.EndPointYTitle.setText(_translate("MainWindow", "Y:"))
        self.addCubicSplinepushButton.setText(_translate("MainWindow", "Add"))
        self.endCubicSplinepushButton.setText(_translate("MainWindow", "End"))

class CubicSplineDisplay(QMainWindow, Ui_cubicspline):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
