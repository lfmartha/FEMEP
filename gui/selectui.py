from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_select(object):
    def setupUi(self, selectui):
        selectui.setObjectName("selectui")
        selectui.resize(200, 300)
        selectui.setMaximumSize(QtCore.QSize(200, 16777215))
        selectui.setMinimumSize(QtCore.QSize(200, 300))

        self.SelectMainTitle = QtWidgets.QLabel(selectui)
        self.SelectMainTitle.setGeometry(QtCore.QRect(0, 10, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SelectMainTitle.setFont(font)
        self.SelectMainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.SelectMainTitle.setObjectName("SelectMainTitle")
        self.SelectMainTitle.setMinimumSize(QtCore.QSize(200, 20))

        self.pointcheckBox = QtWidgets.QCheckBox(selectui)
        self.pointcheckBox.setGeometry(QtCore.QRect(80, 50, 70, 17))
        self.pointcheckBox.setObjectName("pointcheckBox")
        self.pointcheckBox.setChecked(True)
        self.pointcheckBox.setStyleSheet("image: url(icons/point-icon.png);")

        self.segmentcheckBox = QtWidgets.QCheckBox(selectui)
        self.segmentcheckBox.setGeometry(QtCore.QRect(80, 80, 70, 17))
        self.segmentcheckBox.setObjectName("segmentcheckBox")
        self.segmentcheckBox.setChecked(True)
        self.segmentcheckBox.setStyleSheet("image: url(icons/polyline.png);")

        self.patchcheckBox = QtWidgets.QCheckBox(selectui)
        self.patchcheckBox.setGeometry(QtCore.QRect(80, 110, 70, 17))
        self.patchcheckBox.setObjectName("patchcheckBox")
        self.patchcheckBox.setStyleSheet("image: url(icons/patch.png);")
        self.patchcheckBox.setChecked(True)

        self.propertiespushButton = QtWidgets.QPushButton(selectui)
        self.propertiespushButton.setAutoDefault(True)
        self.propertiespushButton.setGeometry(QtCore.QRect(60, 150, 80, 23))
        self.propertiespushButton.setObjectName("propertiespushButton")

        self.retranslateUi(selectui)
        QtCore.QMetaObject.connectSlotsByName(selectui)

    def retranslateUi(self, selectui):
        _translate = QtCore.QCoreApplication.translate
        self.SelectMainTitle.setText(_translate("MainWindow", "Select Options"))
        self.propertiespushButton.setText(_translate("MainWindow", "Properties"))


class SelectDisplay(QMainWindow, Ui_select):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
