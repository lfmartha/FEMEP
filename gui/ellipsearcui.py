from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_ellipsearc(object):
    def setupUi(self, ellipsearcui):
        ellipsearcui.setObjectName("ellipsearcui")
        ellipsearcui.resize(200, 800)
        ellipsearcui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.EllipseArcMainTitle = QtWidgets.QLabel(ellipsearcui)
        self.EllipseArcMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EllipseArcMainTitle.setFont(font)
        self.EllipseArcMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.EllipseArcMainTitle.setObjectName("EllipseArcMainTitle")

        # Center
        self.CenterTitle = QtWidgets.QLabel(ellipsearcui)
        self.CenterTitle.setGeometry(QtCore.QRect(50, 40, 100, 20))
        self.CenterTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterTitle.setObjectName("CenterTitle")

        self.CenterXTitle = QtWidgets.QLabel(ellipsearcui)
        self.CenterXTitle.setGeometry(QtCore.QRect(15, 55, 70, 20))
        font = QtGui.QFont()
        self.CenterXTitle.setFont(font)
        self.CenterXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterXTitle.setObjectName("CenterXTitle")

        self.CenterXlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.CenterXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterXlineEdit.setGeometry(QtCore.QRect(15, 75, 70, 20))
        self.CenterXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterXlineEdit.setObjectName("CenterXlineEdit")

        self.CenterYTitle = QtWidgets.QLabel(ellipsearcui)
        self.CenterYTitle.setGeometry(QtCore.QRect(115, 55, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.CenterYTitle.setFont(font)
        self.CenterYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.CenterYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.CenterYTitle.setObjectName("CenterYTitle")

        self.CenterYlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.CenterYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.CenterYlineEdit.setGeometry(QtCore.QRect(115, 75, 70, 20))
        self.CenterYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.CenterYlineEdit.setObjectName("CenterYlineEdit")

        self.setCenterpushButton = QtWidgets.QPushButton(ellipsearcui)
        self.setCenterpushButton.setAutoDefault(True)
        self.setCenterpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
        self.setCenterpushButton.setObjectName("setCenterpushButton")

        # First axis
        self.FirstAxisTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstAxisTitle.setGeometry(QtCore.QRect(50, 145, 100, 20))
        self.FirstAxisTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisTitle.setObjectName("FirstAxisTitle")

        self.FirstAxiscomboBox = QtWidgets.QComboBox(ellipsearcui)
        self.FirstAxiscomboBox.setGeometry(QtCore.QRect(25, 165, 150, 25))
        self.FirstAxiscomboBox.setObjectName("FirstAxiscomboBox")
        self.FirstAxiscomboBox.addItem("")
        self.FirstAxiscomboBox.addItem("")

        self.FirstAxisXTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstAxisXTitle.setGeometry(QtCore.QRect(15, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstAxisXTitle.setFont(font)
        self.FirstAxisXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstAxisXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisXTitle.setObjectName("FirstAxisXTitle")

        self.FirstAxisXlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.FirstAxisXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstAxisXlineEdit.setGeometry(QtCore.QRect(15, 210, 70, 20))
        self.FirstAxisXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstAxisXlineEdit.setObjectName("FirstAxisXlineEdit")

        self.FirstAxisYTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstAxisYTitle.setGeometry(QtCore.QRect(115, 190, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstAxisYTitle.setFont(font)
        self.FirstAxisYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstAxisYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstAxisYTitle.setObjectName("FirstAxisYTitle")

        self.FirstAxisYlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.FirstAxisYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstAxisYlineEdit.setGeometry(QtCore.QRect(115, 210, 70, 20))
        self.FirstAxisYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstAxisYlineEdit.setObjectName("FirstAxisYlineEdit")

        self.setFirstAxispushButton = QtWidgets.QPushButton(ellipsearcui)
        self.setFirstAxispushButton.setAutoDefault(True)
        self.setFirstAxispushButton.setGeometry(QtCore.QRect(70, 235, 60, 25))
        self.setFirstAxispushButton.setObjectName("setFirstAxispushButton")

        # Second axis
        self.SecondAxisTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondAxisTitle.setGeometry(QtCore.QRect(50, 280, 100, 20))
        self.SecondAxisTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisTitle.setObjectName("SecondAxisTitle")

        self.SecondAxiscomboBox = QtWidgets.QComboBox(ellipsearcui)
        self.SecondAxiscomboBox.setGeometry(QtCore.QRect(25, 300, 150, 25))
        self.SecondAxiscomboBox.setObjectName("FirstAxiscomboBox")
        self.SecondAxiscomboBox.addItem("")
        self.SecondAxiscomboBox.addItem("")

        self.SecondAxisXTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondAxisXTitle.setGeometry(QtCore.QRect(15, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondAxisXTitle.setFont(font)
        self.SecondAxisXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondAxisXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisXTitle.setObjectName("SecondAxisXTitle")

        self.SecondAxisXlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.SecondAxisXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondAxisXlineEdit.setGeometry(QtCore.QRect(15, 345, 70, 20))
        self.SecondAxisXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondAxisXlineEdit.setObjectName("SecondAxisXlineEdit")

        self.SecondAxisYTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondAxisYTitle.setGeometry(QtCore.QRect(115, 325, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondAxisYTitle.setFont(font)
        self.SecondAxisYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondAxisYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondAxisYTitle.setObjectName("SecondAxisYTitle")

        self.SecondAxisYlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.SecondAxisYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondAxisYlineEdit.setGeometry(QtCore.QRect(115, 345, 70, 20))
        self.SecondAxisYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondAxisYlineEdit.setObjectName("SecondAxisYlineEdit")

        self.setSecondAxispushButton = QtWidgets.QPushButton(ellipsearcui)
        self.setSecondAxispushButton.setAutoDefault(True)
        self.setSecondAxispushButton.setGeometry(QtCore.QRect(70, 370, 60, 25))
        self.setSecondAxispushButton.setObjectName("setSecondAxispushButton")

        # First Arc Point
        self.FirstArcPointTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstArcPointTitle.setGeometry(QtCore.QRect(40, 415, 120, 20))
        self.FirstArcPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointTitle.setObjectName("FirstArcPointTitle")

        self.FirstArcPointcomboBox = QtWidgets.QComboBox(ellipsearcui)
        self.FirstArcPointcomboBox.setGeometry(QtCore.QRect(25, 435, 150, 25))
        self.FirstArcPointcomboBox.setObjectName("FirstArcPointcomboBox")
        self.FirstArcPointcomboBox.addItem("")
        self.FirstArcPointcomboBox.addItem("")

        self.FirstArcPointXTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstArcPointXTitle.setGeometry(QtCore.QRect(15, 460, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstArcPointXTitle.setFont(font)
        self.FirstArcPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstArcPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointXTitle.setObjectName("FirstArcPointXTitle")

        self.FirstArcPointXlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.FirstArcPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstArcPointXlineEdit.setGeometry(QtCore.QRect(15, 480, 70, 20))
        self.FirstArcPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstArcPointXlineEdit.setObjectName("FirstArcPointXlineEdit")

        self.FirstArcPointYTitle = QtWidgets.QLabel(ellipsearcui)
        self.FirstArcPointYTitle.setGeometry(QtCore.QRect(115, 460, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstArcPointYTitle.setFont(font)
        self.FirstArcPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.FirstArcPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.FirstArcPointYTitle.setObjectName("FirstArcPointYTitle")

        self.FirstArcPointYlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.FirstArcPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.FirstArcPointYlineEdit.setGeometry(QtCore.QRect(115, 480, 70, 20))
        self.FirstArcPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.FirstArcPointYlineEdit.setObjectName("FirstArcPointYlineEdit")

        self.setFirstArcPointpushButton = QtWidgets.QPushButton(ellipsearcui)
        self.setFirstArcPointpushButton.setAutoDefault(True)
        self.setFirstArcPointpushButton.setGeometry(QtCore.QRect(70, 505, 60, 25))
        self.setFirstArcPointpushButton.setObjectName("setFirstArcPointpushButton")

        # Second Arc Point
        self.SecondArcPointTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondArcPointTitle.setGeometry(QtCore.QRect(35, 550, 130, 20))
        self.SecondArcPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointTitle.setObjectName("SecondArcPointTitle")

        self.SecondArcPointcomboBox = QtWidgets.QComboBox(ellipsearcui)
        self.SecondArcPointcomboBox.setGeometry(QtCore.QRect(25, 570, 150, 25))
        self.SecondArcPointcomboBox.setObjectName("SecondArcPointcomboBox")
        self.SecondArcPointcomboBox.addItem("")
        self.SecondArcPointcomboBox.addItem("")

        self.SecondArcPointXTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondArcPointXTitle.setGeometry(QtCore.QRect(15, 595, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondArcPointXTitle.setFont(font)
        self.SecondArcPointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondArcPointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointXTitle.setObjectName("SecondArcPointXTitle")

        self.SecondArcPointXlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.SecondArcPointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondArcPointXlineEdit.setGeometry(QtCore.QRect(15, 615, 70, 20))
        self.SecondArcPointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondArcPointXlineEdit.setObjectName("SecondArcPointXlineEdit")

        self.SecondArcPointYTitle = QtWidgets.QLabel(ellipsearcui)
        self.SecondArcPointYTitle.setGeometry(QtCore.QRect(115, 595, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SecondArcPointYTitle.setFont(font)
        self.SecondArcPointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        self.SecondArcPointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SecondArcPointYTitle.setObjectName("SecondArcPointYTitle")

        self.SecondArcPointYlineEdit = QtWidgets.QLineEdit(ellipsearcui)
        self.SecondArcPointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.SecondArcPointYlineEdit.setGeometry(QtCore.QRect(115, 615, 70, 20))
        self.SecondArcPointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.SecondArcPointYlineEdit.setObjectName("SecondArcPointYlineEdit")

        # Add Button
        self.addEllipseArcpushButton = QtWidgets.QPushButton(ellipsearcui)
        self.addEllipseArcpushButton.setAutoDefault(True)
        self.addEllipseArcpushButton.setGeometry(QtCore.QRect(50, 640, 100, 25))
        self.addEllipseArcpushButton.setObjectName("addEllipseArcpushButton")

        self.retranslateUi(ellipsearcui)
        QtCore.QMetaObject.connectSlotsByName(ellipsearcui)

    def retranslateUi(self, ellipsearcui):
        _translate = QtCore.QCoreApplication.translate
        self.EllipseArcMainTitle.setText(_translate("MainWindow", "Ellipse Arc"))

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
        self.setSecondAxispushButton.setText(_translate("MainWindow", "Set"))

        self.FirstArcPointTitle.setText(_translate("MainWindow", "Set First Arc Point:"))
        self.FirstArcPointcomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.FirstArcPointcomboBox.setItemText(1, _translate("MainWindow", "Length and Angle"))
        self.FirstArcPointXTitle.setText(_translate("MainWindow", "X:"))
        self.FirstArcPointYTitle.setText(_translate("MainWindow", "Y:"))
        self.setFirstArcPointpushButton.setText(_translate("MainWindow", "Set"))

        self.SecondArcPointTitle.setText(_translate("MainWindow", "Set Second Arc Point:"))
        self.SecondArcPointcomboBox.setItemText(0, _translate("MainWindow", "Coordinates"))
        self.SecondArcPointcomboBox.setItemText(1, _translate("MainWindow", "Length and Angle"))
        self.SecondArcPointXTitle.setText(_translate("MainWindow", "X:"))
        self.SecondArcPointYTitle.setText(_translate("MainWindow", "Y:"))

        self.addEllipseArcpushButton.setText(_translate("MainWindow", "Add Ellipse Arc"))

class EllipseArcDisplay(QMainWindow, Ui_ellipsearc):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)