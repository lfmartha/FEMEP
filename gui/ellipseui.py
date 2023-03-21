from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_ellipse(object):
    def setupUi(self, ellipseui):
        ellipseui.setObjectName("ellipseui")
        ellipseui.resize(200, 800)
        ellipseui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.EllipseMainTitle = QtWidgets.QLabel(ellipseui)
        self.EllipseMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EllipseMainTitle.setFont(font)
        self.EllipseMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.EllipseMainTitle.setObjectName("EllipseMainTitle")

        # Center
        self.CenterTitle = QtWidgets.QLabel(ellipseui)
        self.CenterTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.CenterTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterTitle.setObjectName("CenterTitle")

        self.CenterXTitle = QtWidgets.QLabel(ellipseui)
        self.CenterXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        self.CenterXTitle.setFont(font)
        self.CenterXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterXTitle.setObjectName("CenterXTitle")

        self.CenterXlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.CenterXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.CenterXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterXlineEdit.setObjectName("CenterXlineEdit")

        self.CenterYTitle = QtWidgets.QLabel(ellipseui)
        self.CenterYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.CenterYTitle.setFont(font)
        self.CenterYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterYTitle.setObjectName("CenterYTitle")

        self.CenterYlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.CenterYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.CenterYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterYlineEdit.setObjectName("CenterYlineEdit")

        self.setCenterpushButton = QtWidgets.QPushButton(ellipseui)
        self.setCenterpushButton.setAutoDefault(True)
        self.setCenterpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
        self.setCenterpushButton.setObjectName("setCenterpushButton")

        # First axis
        self.FirstAxisTitle = QtWidgets.QLabel(ellipseui)
        self.FirstAxisTitle.setGeometry(QtCore.QRect(50, 145, 100, 20))
        self.FirstAxisTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisTitle.setObjectName("FirstAxisTitle")

        self.FirstAxiscomboBox = QtWidgets.QComboBox(ellipseui)
        self.FirstAxiscomboBox.setGeometry(QtCore.QRect(25, 165, 150, 25))
        self.FirstAxiscomboBox.setObjectName("FirstAxiscomboBox")
        self.FirstAxiscomboBox.addItem("")
        self.FirstAxiscomboBox.addItem("")

        self.FirstAxisXTitle = QtWidgets.QLabel(ellipseui)
        self.FirstAxisXTitle.setGeometry(QtCore.QRect(15, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstAxisXTitle.setFont(font)
        self.FirstAxisXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstAxisXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisXTitle.setObjectName("FirstAxisXTitle")

        self.FirstAxisXlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.FirstAxisXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstAxisXlineEdit.setGeometry(QtCore.QRect(15, 210, 70, 20))
        self.FirstAxisXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstAxisXlineEdit.setObjectName("FirstAxisXlineEdit")

        self.FirstAxisYTitle = QtWidgets.QLabel(ellipseui)
        self.FirstAxisYTitle.setGeometry(QtCore.QRect(115, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstAxisYTitle.setFont(font)
        self.FirstAxisYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstAxisYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisYTitle.setObjectName("FirstAxisYTitle")

        self.FirstAxisYlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.FirstAxisYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstAxisYlineEdit.setGeometry(QtCore.QRect(115, 210, 70, 20))
        self.FirstAxisYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstAxisYlineEdit.setObjectName("FirstAxisYlineEdit")

        self.setFirstAxispushButton = QtWidgets.QPushButton(ellipseui)
        self.setFirstAxispushButton.setAutoDefault(True)
        self.setFirstAxispushButton.setGeometry(QtCore.QRect(70, 235, 60, 25))
        self.setFirstAxispushButton.setObjectName("setFirstAxispushButton")

        # Second axis
        self.SecondAxisTitle = QtWidgets.QLabel(ellipseui)
        self.SecondAxisTitle.setGeometry(QtCore.QRect(50, 280, 100, 20))
        self.SecondAxisTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisTitle.setObjectName("SecondAxisTitle")

        self.SecondAxiscomboBox = QtWidgets.QComboBox(ellipseui)
        self.SecondAxiscomboBox.setGeometry(QtCore.QRect(25, 300, 150, 25))
        self.SecondAxiscomboBox.setObjectName("FirstAxiscomboBox")
        self.SecondAxiscomboBox.addItem("")
        self.SecondAxiscomboBox.addItem("")

        self.SecondAxisXTitle = QtWidgets.QLabel(ellipseui)
        self.SecondAxisXTitle.setGeometry(QtCore.QRect(15, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondAxisXTitle.setFont(font)
        self.SecondAxisXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondAxisXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisXTitle.setObjectName("SecondAxisXTitle")

        self.SecondAxisXlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.SecondAxisXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondAxisXlineEdit.setGeometry(QtCore.QRect(15, 345, 70, 20))
        self.SecondAxisXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondAxisXlineEdit.setObjectName("SecondAxisXlineEdit")

        self.SecondAxisYTitle = QtWidgets.QLabel(ellipseui)
        self.SecondAxisYTitle.setGeometry(QtCore.QRect(115, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondAxisYTitle.setFont(font)
        self.SecondAxisYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondAxisYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisYTitle.setObjectName("SecondAxisYTitle")

        self.SecondAxisYlineEdit = QtWidgets.QLineEdit(ellipseui)
        self.SecondAxisYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondAxisYlineEdit.setGeometry(QtCore.QRect(115, 345, 70, 20))
        self.SecondAxisYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondAxisYlineEdit.setObjectName("SecondAxisYlineEdit")

        # Add Button
        self.addEllipsepushButton = QtWidgets.QPushButton(ellipseui)
        self.addEllipsepushButton.setAutoDefault(True)
        self.addEllipsepushButton.setGeometry(QtCore.QRect(60, 370, 80, 25))
        self.addEllipsepushButton.setObjectName("addEllipsepushButton")

        self.retranslateUi(ellipseui)
        QtCore.QMetaObject.connectSlotsByName(ellipseui)

    def retranslateUi(self, ellipseui):
        _translate = QtCore.QCoreApplication.translate
        self.EllipseMainTitle.setText(_translate("MainWindow", "Ellipse"))

        self.CenterTitle.setText(_translate("MainWindow", "Set Center:"))
        self.CenterXTitle.setText(_translate("MainWindow", "X:"))
        self.CenterYTitle.setText(_translate("MainWindow", "Y:"))
        self.setCenterpushButton.setText(_translate("MainWindow", "Set"))

        self.FirstAxisTitle.setText(_translate("MainWindow", "Set First Axis:"))
        self.FirstAxiscomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.FirstAxiscomboBox.setItemText(1, _translate("MainWindow", "Length and Angle"))
        self.FirstAxisXTitle.setText(_translate("MainWindow", "X:"))
        self.FirstAxisYTitle.setText(_translate("MainWindow", "Y:"))
        self.setFirstAxispushButton.setText(_translate("MainWindow", "Set"))
        
        self.SecondAxisTitle.setText(_translate("MainWindow", "Set Second Axis:"))
        self.SecondAxiscomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.SecondAxiscomboBox.setItemText(1, _translate("MainWindow", "Length and Angle"))
        self.SecondAxisXTitle.setText(_translate("MainWindow", "X:"))
        self.SecondAxisYTitle.setText(_translate("MainWindow", "Y:"))
        self.addEllipsepushButton.setText(_translate("MainWindow", "Add Ellipse"))

class EllipseDisplay(QMainWindow, Ui_ellipse):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
