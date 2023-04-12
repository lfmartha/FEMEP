from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_nsudv(object):
    def setupUi(self, nsudvui):
        nsudvui.setObjectName("nsudvui")
        nsudvui.resize(200, 300)
        nsudvui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.nsudvMainTitle1 = QtWidgets.QLabel(nsudvui)
        self.nsudvMainTitle1.setGeometry(QtCore.QRect(0, 10, 200, 20))
        self.nsudvMainTitle2 = QtWidgets.QLabel(nsudvui)
        self.nsudvMainTitle2.setGeometry(QtCore.QRect(0, 30, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nsudvMainTitle1.setFont(font)
        self.nsudvMainTitle1.setAlignment(QtCore.Qt.AlignCenter)
        self.nsudvMainTitle1.setObjectName("nsudvMainTitle1")
        self.nsudvMainTitle2.setFont(font)
        self.nsudvMainTitle2.setAlignment(QtCore.Qt.AlignCenter)
        self.nsudvMainTitle2.setObjectName("nsudvMainTitle2")

        # ComboBox
        self.nsudvcomboBox = QtWidgets.QComboBox(nsudvui)
        self.nsudvcomboBox.setGeometry(QtCore.QRect(25, 65, 150, 25))
        self.nsudvcomboBox.setObjectName("nsudvcomboBox")
        self.nsudvcomboBox.addItem("")
        self.nsudvcomboBox.addItem("")

        # Value
        self.valueTitle = QtWidgets.QLabel(nsudvui)
        self.valueTitle.setGeometry(QtCore.QRect(15, 95, 70, 20))
        self.valueTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.valueTitle.setObjectName("valueTitle")

        self.valuelineEdit = QtWidgets.QLineEdit(nsudvui)
        self.valuelineEdit.setGeometry(QtCore.QRect(15, 115, 70, 20))
        self.valuelineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.valuelineEdit.setObjectName("valuelineEdit")
        self.valuelineEdit.setValidator(QtGui.QIntValidator())

        # Ratio
        self.ratioTitle = QtWidgets.QLabel(nsudvui)
        self.ratioTitle.setGeometry(QtCore.QRect(115, 95, 70, 20))
        self.ratioTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.ratioTitle.setObjectName("ratioTitle")

        self.ratiolineEdit = QtWidgets.QLineEdit(nsudvui)
        self.ratiolineEdit.setGeometry(QtCore.QRect(115, 115, 70, 20))
        self.ratiolineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ratiolineEdit.setObjectName("ratiolineEdit")
        self.ratiolineEdit.setValidator(QtGui.QDoubleValidator())

        # Push Button
        self.nsudvpushButton = QtWidgets.QPushButton(nsudvui)
        self.nsudvpushButton.setAutoDefault(True)
        self.nsudvpushButton.setGeometry(QtCore.QRect(70, 140, 60, 25))
        self.nsudvpushButton.setObjectName("addlinepushButton")

        # Knot Refinement
        self.knotrefinementTitle = QtWidgets.QLabel(nsudvui)
        self.knotrefinementTitle.setGeometry(QtCore.QRect(50, 145, 100, 20))
        self.knotrefinementTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.knotrefinementTitle.setObjectName("knotrefinementTitle")

        self.knotrefinementpushButton = QtWidgets.QPushButton(nsudvui)
        self.knotrefinementpushButton.setAutoDefault(True)
        self.knotrefinementpushButton.setGeometry(QtCore.QRect(50, 170, 100, 25))
        self.knotrefinementpushButton.setObjectName("knotrefinementpushButton")

        self.rescuepushButton = QtWidgets.QPushButton(nsudvui)
        self.rescuepushButton.setAutoDefault(True)
        self.rescuepushButton.setGeometry(QtCore.QRect(150, 170, 25, 25))
        self.rescuepushButton.setObjectName("rescuepushButton")
        self.rescuepushButton.setIcon(QtGui.QIcon("icons/undo-icon.png"))

        # Knot Comform
        self.knotconformTitle = QtWidgets.QLabel(nsudvui)
        self.knotconformTitle.setGeometry(QtCore.QRect(50, 210, 100, 20))
        self.knotconformTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.knotconformTitle.setObjectName("knotconformTitle")

        self.knotconformpushButton = QtWidgets.QPushButton(nsudvui)
        self.knotconformpushButton.setAutoDefault(True)
        self.knotconformpushButton.setGeometry(QtCore.QRect(50, 235, 100, 25))
        self.knotconformpushButton.setObjectName("knotconformpushButton")

        self.retranslateUi(nsudvui)
        QtCore.QMetaObject.connectSlotsByName(nsudvui)

    def retranslateUi(self, nsudvui):
        _translate = QtCore.QCoreApplication.translate
        self.nsudvMainTitle1.setText(_translate("MainWindow", "Number of"))
        self.nsudvMainTitle2.setText(_translate("MainWindow", "Subdivisions"))
        self.nsudvcomboBox.setItemText(0, _translate("MainWindow", "Set Subdivisions"))
        self.nsudvcomboBox.setItemText(1, _translate("MainWindow", "Get from Knot Vector"))
        self.valueTitle.setText(_translate("MainWindow", "Value:"))
        self.ratioTitle.setText(_translate("MainWindow", "Ratio:"))
        self.nsudvpushButton.setText(_translate("MainWindow", "Set"))
        self.knotrefinementTitle.setText(_translate("MainWindow", "Knot Refinement"))
        self.knotrefinementTitle.hide()
        self.knotrefinementpushButton.setText(_translate("MainWindow", "Refine Curve"))
        self.knotrefinementpushButton.hide()
        self.rescuepushButton.setToolTip(_translate("MainWindow", "Rescue Curve"))
        self.rescuepushButton.hide()
        self.knotconformTitle.setText(_translate("MainWindow", "Knot Conform"))
        self.knotconformTitle.hide()
        self.knotconformpushButton.setText(_translate("MainWindow", "Conform Curves"))
        self.knotconformpushButton.hide()

class NsudvDisplay(QMainWindow, Ui_nsudv):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
