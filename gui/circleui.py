from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_circle(object):
    def setupUi(self, circleui):
        circleui.setObjectName("circleui")
        circleui.resize(200, 800)
        circleui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.CircleMainTitle = QtWidgets.QLabel(circleui)
        self.CircleMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CircleMainTitle.setFont(font)
        self.CircleMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CircleMainTitle.setObjectName("CircleMainTitle")

        # Center
        self.CenterTitle = QtWidgets.QLabel(circleui)
        self.CenterTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.CenterTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterTitle.setObjectName("CenterTitle")

        self.CenterXTitle = QtWidgets.QLabel(circleui)
        self.CenterXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        self.CenterXTitle.setFont(font)
        self.CenterXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterXTitle.setObjectName("CenterXTitle")

        self.CenterXlineEdit = QtWidgets.QLineEdit(circleui)
        self.CenterXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.CenterXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterXlineEdit.setObjectName("CenterXlineEdit")

        self.CenterYTitle = QtWidgets.QLabel(circleui)
        self.CenterYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.CenterYTitle.setFont(font)
        self.CenterYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterYTitle.setObjectName("CenterYTitle")

        self.CenterYlineEdit = QtWidgets.QLineEdit(circleui)
        self.CenterYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.CenterYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterYlineEdit.setObjectName("CenterYlineEdit")

        self.setCenterpushButton = QtWidgets.QPushButton(circleui)
        self.setCenterpushButton.setAutoDefault(True)
        self.setCenterpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
        self.setCenterpushButton.setObjectName("setCenterpushButton")

        # Radius
        self.RadiusTitle = QtWidgets.QLabel(circleui)
        self.RadiusTitle.setGeometry(QtCore.QRect(50, 145, 100, 20))
        self.RadiusTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.RadiusTitle.setObjectName("RadiusTitle")

        self.RadiuscomboBox = QtWidgets.QComboBox(circleui)
        self.RadiuscomboBox.setGeometry(QtCore.QRect(25, 165, 150, 25))
        self.RadiuscomboBox.setObjectName("RadiuscomboBox")
        self.RadiuscomboBox.addItem("")
        self.RadiuscomboBox.addItem("")

        self.RadiusXTitle = QtWidgets.QLabel(circleui)
        self.RadiusXTitle.setGeometry(QtCore.QRect(15, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RadiusXTitle.setFont(font)
        self.RadiusXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.RadiusXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.RadiusXTitle.setObjectName("RadiusXTitle")

        self.RadiusXlineEdit = QtWidgets.QLineEdit(circleui)
        self.RadiusXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.RadiusXlineEdit.setGeometry(QtCore.QRect(15, 210, 70, 20))
        self.RadiusXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.RadiusXlineEdit.setObjectName("RadiusXlineEdit")

        self.RadiusYTitle = QtWidgets.QLabel(circleui)
        self.RadiusYTitle.setGeometry(QtCore.QRect(115, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RadiusYTitle.setFont(font)
        self.RadiusYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.RadiusYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.RadiusYTitle.setObjectName("RadiusYTitle")

        self.RadiusYlineEdit = QtWidgets.QLineEdit(circleui)
        self.RadiusYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.RadiusYlineEdit.setGeometry(QtCore.QRect(115, 210, 70, 20))
        self.RadiusYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.RadiusYlineEdit.setObjectName("RadiusYlineEdit")

        # Add Button
        self.addCirclepushButton = QtWidgets.QPushButton(circleui)
        self.addCirclepushButton.setAutoDefault(True)
        self.addCirclepushButton.setGeometry(QtCore.QRect(60, 235, 80, 25))
        self.addCirclepushButton.setObjectName("addCirclepushButton")

        self.retranslateUi(circleui)
        QtCore.QMetaObject.connectSlotsByName(circleui)

    def retranslateUi(self, circleui):
        _translate = QtCore.QCoreApplication.translate
        self.CircleMainTitle.setText(_translate("MainWindow", "Circle"))

        self.CenterTitle.setText(_translate("MainWindow", "Set Center:"))
        self.CenterXTitle.setText(_translate("MainWindow", "X:"))
        self.CenterYTitle.setText(_translate("MainWindow", "Y:"))
        self.setCenterpushButton.setText(_translate("MainWindow", "Set"))

        self.RadiusTitle.setText(_translate("MainWindow", "Set Radius:"))
        self.RadiuscomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.RadiuscomboBox.setItemText(1, _translate("MainWindow", "Radius and Angle"))
        self.RadiusXTitle.setText(_translate("MainWindow", "X:"))
        self.RadiusYTitle.setText(_translate("MainWindow", "Y:"))
        self.addCirclepushButton.setText(_translate("MainWindow", "Add Circle"))

class CircleDisplay(QMainWindow, Ui_circle):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)