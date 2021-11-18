from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_line(object):
    def setupUi(self, lineui):
        lineui.setObjectName("lineui")
        lineui.resize(200, 300)
        lineui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.firstpointXlineEdit = QtWidgets.QLineEdit(lineui)
        self.firstpointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.firstpointXlineEdit.setGeometry(QtCore.QRect(15, 80, 70, 20))
        self.firstpointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "")
        self.firstpointXlineEdit.setObjectName("firstpointXlineEdit")
        self.firstpointYlineEdit = QtWidgets.QLineEdit(lineui)
        self.firstpointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.firstpointYlineEdit.setGeometry(QtCore.QRect(115, 80, 70, 20))
        self.firstpointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "")
        self.firstpointYlineEdit.setObjectName("firstYlineEdit")
        self.firstpointXTitle = QtWidgets.QLabel(lineui)
        self.firstpointXTitle.setGeometry(QtCore.QRect(20, 60, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.firstpointXTitle.setFont(font)
        self.firstpointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                            "")
        self.firstpointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointXTitle.setObjectName("firstpointXTitle")
        self.firstpointYTitle = QtWidgets.QLabel(lineui)
        self.firstpointYTitle.setGeometry(QtCore.QRect(120, 60, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.firstpointYTitle.setFont(font)
        self.firstpointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                            "")
        self.firstpointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointYTitle.setObjectName("firstpointYTitle")
        self.lineMainTitle = QtWidgets.QLabel(lineui)
        self.lineMainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineMainTitle.setFont(font)
        self.lineMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lineMainTitle.setObjectName("lineMainTitle")
        self.endpointYTitle = QtWidgets.QLabel(lineui)
        self.endpointYTitle.setGeometry(QtCore.QRect(120, 140, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.endpointYTitle.setFont(font)
        self.endpointYTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                          "")
        self.endpointYTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointYTitle.setObjectName("endpointYTitle")
        self.endpointXTitle = QtWidgets.QLabel(lineui)
        self.endpointXTitle.setGeometry(QtCore.QRect(20, 140, 70, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.endpointXTitle.setFont(font)
        self.endpointXTitle.setStyleSheet("color: rgb(0, 0, 0);\n"
                                          "")
        self.endpointXTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointXTitle.setObjectName("endpointXTitle")
        self.endpointXlineEdit = QtWidgets.QLineEdit(lineui)
        self.endpointXlineEdit.setValidator(QtGui.QDoubleValidator())
        self.endpointXlineEdit.setGeometry(QtCore.QRect(15, 160, 70, 20))
        self.endpointXlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "")
        self.endpointXlineEdit.setObjectName("endpointXlineEdit")
        self.endpointYlineEdit = QtWidgets.QLineEdit(lineui)
        self.endpointYlineEdit.setValidator(QtGui.QDoubleValidator())
        self.endpointYlineEdit.setGeometry(QtCore.QRect(115, 160, 70, 20))
        self.endpointYlineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "")
        self.endpointYlineEdit.setObjectName("endpointYlineEdit")
        self.addlinepushButton = QtWidgets.QPushButton(lineui)
        self.addlinepushButton.setAutoDefault(True)
        self.addlinepushButton.setGeometry(QtCore.QRect(60, 200, 80, 23))
        self.addlinepushButton.setObjectName("addpointpushButton")
        self.firstpointTitle = QtWidgets.QLabel(lineui)
        self.firstpointTitle.setGeometry(QtCore.QRect(70, 40, 70, 13))
        self.firstpointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.firstpointTitle.setObjectName("firstpointTitle")
        self.endpointTitle = QtWidgets.QLabel(lineui)
        self.endpointTitle.setGeometry(QtCore.QRect(70, 120, 70, 13))
        self.endpointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.endpointTitle.setObjectName("endpointTitle")
        self.retranslateUi(lineui)
        QtCore.QMetaObject.connectSlotsByName(lineui)

    def retranslateUi(self, lineui):
        _translate = QtCore.QCoreApplication.translate
        self.firstpointXTitle.setText(_translate("MainWindow", "X :"))
        self.firstpointYTitle.setText(_translate("MainWindow", "Y: "))
        self.lineMainTitle.setText(_translate("MainWindow", "Line"))
        self.endpointYTitle.setText(_translate("MainWindow", "Y :"))
        self.endpointXTitle.setText(_translate("MainWindow", "X :"))
        self.addlinepushButton.setText(_translate("MainWindow", "Add Line"))
        self.firstpointTitle.setText(_translate("MainWindow", "First Point :"))
        self.endpointTitle.setText(_translate("MainWindow", "End Point:"))


class LineDisplay(QMainWindow, Ui_line):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
