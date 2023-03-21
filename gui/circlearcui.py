from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_circlearc(object):
    def setupUi(self, circlearcui):
        circlearcui.setObjectName("circlearcui")
        circlearcui.resize(200, 800)
        circlearcui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.CircleArcMainTitle = QtWidgets.QLabel(circlearcui)
        self.CircleArcMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CircleArcMainTitle.setFont(font)
        self.CircleArcMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CircleArcMainTitle.setObjectName("CircleArcMainTitle")

        # Center
        self.CenterTitle = QtWidgets.QLabel(circlearcui)
        self.CenterTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.CenterTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterTitle.setObjectName("CenterTitle")

        self.CenterXTitle = QtWidgets.QLabel(circlearcui)
        self.CenterXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        self.CenterXTitle.setFont(font)
        self.CenterXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterXTitle.setObjectName("CenterXTitle")

        self.CenterXlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.CenterXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.CenterXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterXlineEdit.setObjectName("CenterXlineEdit")

        self.CenterYTitle = QtWidgets.QLabel(circlearcui)
        self.CenterYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.CenterYTitle.setFont(font)
        self.CenterYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterYTitle.setObjectName("CenterYTitle")

        self.CenterYlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.CenterYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.CenterYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterYlineEdit.setObjectName("CenterYlineEdit")

        self.setCenterpushButton = QtWidgets.QPushButton(circlearcui)
        self.setCenterpushButton.setAutoDefault(True)
        self.setCenterpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
        self.setCenterpushButton.setObjectName("setCenterpushButton")

        # First Arc Point
        self.FirstArcPointTitle = QtWidgets.QLabel(circlearcui)
        self.FirstArcPointTitle.setGeometry(QtCore.QRect(35, 145, 130, 20))
        self.FirstArcPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointTitle.setObjectName("FirstArcPointTitle")

        self.FirstArcPointcomboBox = QtWidgets.QComboBox(circlearcui)
        self.FirstArcPointcomboBox.setGeometry(QtCore.QRect(25, 165, 150, 25))
        self.FirstArcPointcomboBox.setObjectName("FirstArcPointcomboBox")
        self.FirstArcPointcomboBox.addItem("")
        self.FirstArcPointcomboBox.addItem("")

        self.FirstArcPointXTitle = QtWidgets.QLabel(circlearcui)
        self.FirstArcPointXTitle.setGeometry(QtCore.QRect(15, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstArcPointXTitle.setFont(font)
        self.FirstArcPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstArcPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointXTitle.setObjectName("FirstArcPointXTitle")

        self.FirstArcPointXlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.FirstArcPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstArcPointXlineEdit.setGeometry(QtCore.QRect(15, 210, 70, 20))
        self.FirstArcPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstArcPointXlineEdit.setObjectName("FirstArcPointXlineEdit")

        self.FirstArcPointYTitle = QtWidgets.QLabel(circlearcui)
        self.FirstArcPointYTitle.setGeometry(QtCore.QRect(115, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstArcPointYTitle.setFont(font)
        self.FirstArcPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstArcPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointYTitle.setObjectName("FirstArcPointYTitle")

        self.FirstArcPointYlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.FirstArcPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstArcPointYlineEdit.setGeometry(QtCore.QRect(115, 210, 70, 20))
        self.FirstArcPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstArcPointYlineEdit.setObjectName("FirstArcPointYlineEdit")

        self.setFirstArcPointpushButton = QtWidgets.QPushButton(circlearcui)
        self.setFirstArcPointpushButton.setAutoDefault(True)
        self.setFirstArcPointpushButton.setGeometry(QtCore.QRect(70, 235, 60, 25))
        self.setFirstArcPointpushButton.setObjectName("FirstArcPointpushButton")

        # Second Arc Point
        self.SecondArcPointTitle = QtWidgets.QLabel(circlearcui)
        self.SecondArcPointTitle.setGeometry(QtCore.QRect(35, 280, 130, 20))
        self.SecondArcPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointTitle.setObjectName("SecondArcPointTitle")

        self.SecondArcPointcomboBox = QtWidgets.QComboBox(circlearcui)
        self.SecondArcPointcomboBox.setGeometry(QtCore.QRect(25, 300, 150, 25))
        self.SecondArcPointcomboBox.setObjectName("SecondArcPointcomboBox")
        self.SecondArcPointcomboBox.addItem("")
        self.SecondArcPointcomboBox.addItem("")

        self.SecondArcPointXTitle = QtWidgets.QLabel(circlearcui)
        self.SecondArcPointXTitle.setGeometry(QtCore.QRect(15, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondArcPointXTitle.setFont(font)
        self.SecondArcPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondArcPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointXTitle.setObjectName("SecondArcPointXTitle")

        self.SecondArcPointXlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.SecondArcPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondArcPointXlineEdit.setGeometry(QtCore.QRect(15, 345, 70, 20))
        self.SecondArcPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondArcPointXlineEdit.setObjectName("SecondArcPointXlineEdit")

        self.SecondArcPointYTitle = QtWidgets.QLabel(circlearcui)
        self.SecondArcPointYTitle.setGeometry(QtCore.QRect(115, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondArcPointYTitle.setFont(font)
        self.SecondArcPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondArcPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointYTitle.setObjectName("SecondArcPointYTitle")

        self.SecondArcPointYlineEdit = QtWidgets.QLineEdit(circlearcui)
        self.SecondArcPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondArcPointYlineEdit.setGeometry(QtCore.QRect(115, 345, 70, 20))
        self.SecondArcPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondArcPointYlineEdit.setObjectName("SecondArcPointYlineEdit")

        # Add Button
        self.addCircleArcpushButton = QtWidgets.QPushButton(circlearcui)
        self.addCircleArcpushButton.setAutoDefault(True)
        self.addCircleArcpushButton.setGeometry(QtCore.QRect(50, 370, 100, 25))
        self.addCircleArcpushButton.setObjectName("addCircleArcpushButton")

        self.retranslateUi(circlearcui)
        QtCore.QMetaObject.connectSlotsByName(circlearcui)

    def retranslateUi(self, circlearcui):
        _translate = QtCore.QCoreApplication.translate
        self.CircleArcMainTitle.setText(_translate("MainWindow", "Circle Arc"))

        self.CenterTitle.setText(_translate("MainWindow", "Set Center:"))
        self.CenterXTitle.setText(_translate("MainWindow", "X:"))
        self.CenterYTitle.setText(_translate("MainWindow", "Y:"))
        self.setCenterpushButton.setText(_translate("MainWindow", "Set"))

        self.FirstArcPointTitle.setText(_translate("MainWindow", "Set First Arc Point:"))
        self.FirstArcPointcomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.FirstArcPointcomboBox.setItemText(1, _translate("MainWindow", "Radius and Angle"))
        self.FirstArcPointXTitle.setText(_translate("MainWindow", "X:"))
        self.FirstArcPointYTitle.setText(_translate("MainWindow", "Y:"))
        self.setFirstArcPointpushButton.setText(_translate("MainWindow", "Set"))
        
        self.SecondArcPointTitle.setText(_translate("MainWindow", "Set Second Arc Point:"))
        self.SecondArcPointcomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.SecondArcPointcomboBox.setItemText(1, _translate("MainWindow", "Radius and Angle"))
        self.SecondArcPointXTitle.setText(_translate("MainWindow", "X:"))
        self.SecondArcPointYTitle.setText(_translate("MainWindow", "Y:"))
        self.addCircleArcpushButton.setText(_translate("MainWindow", "Add Circle Arc"))

class CircleArcDisplay(QMainWindow, Ui_circlearc):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
