from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_exportFile(object):
    def setupUi(self, exportFileui):
        exportFileui.setObjectName("exportFileui")
        exportFileui.resize(200, 369)
        exportFileui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.MainTitle = QtWidgets.QLabel(exportFileui)
        self.MainTitle.setGeometry(QtCore.QRect(50, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MainTitle.setFont(font)
        self.MainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.MainTitle.setObjectName("MainTitle")

        self.optionsLabel = QtWidgets.QLabel(exportFileui)
        self.optionsLabel.setGeometry(QtCore.QRect(0, 40, 200, 20))
        self.optionsLabel.setObjectName("optionsLabel")

        self.optionscomboBox = QtWidgets.QComboBox(exportFileui)
        self.optionscomboBox.setGeometry(QtCore.QRect(10, 70, 180, 20))
        self.optionscomboBox.setObjectName("meshcomboBox")
        self.optionscomboBox.addItem("")

        self.alLabel = QtWidgets.QLabel(exportFileui)
        self.alLabel.setGeometry(QtCore.QRect(0, 100, 200, 20))
        self.alLabel.setObjectName("alLabel")

        self.aloptionscomboBox = QtWidgets.QComboBox(exportFileui)
        self.aloptionscomboBox.setGeometry(QtCore.QRect(10, 130, 180, 20))
        self.aloptionscomboBox.setObjectName("aloptionscomboBox")
        self.aloptionscomboBox.addItem("")
        self.aloptionscomboBox.addItem("")

        self.gpLabel = QtWidgets.QLabel(exportFileui)
        self.gpLabel.setGeometry(QtCore.QRect(0, 160, 200, 20))
        self.gpLabel.setObjectName("gpLabel")

        self.T3Label = QtWidgets.QLabel(exportFileui)
        self.T3Label.setGeometry(QtCore.QRect(0, 190, 200, 20))
        self.T3Label.setObjectName("T3Label")
        self.T3comboBox = QtWidgets.QComboBox(exportFileui)
        self.T3comboBox.setGeometry(QtCore.QRect(40, 190, 50, 20))
        self.T3comboBox.setObjectName("T3comboBox")
        self.T3comboBox.addItem("1")
        self.T3comboBox.addItem("3")

        self.T6Label = QtWidgets.QLabel(exportFileui)
        self.T6Label.setGeometry(QtCore.QRect(0, 220, 200, 20))
        self.T6Label.setObjectName("T6Label")
        self.T6comboBox = QtWidgets.QComboBox(exportFileui)
        self.T6comboBox.setGeometry(QtCore.QRect(40, 220, 50, 20))
        self.T6comboBox.setObjectName("T6comboBox")
        self.T6comboBox.addItem("3")

        self.Q4Label = QtWidgets.QLabel(exportFileui)
        self.Q4Label.setGeometry(QtCore.QRect(0, 250, 200, 20))
        self.Q4Label.setObjectName("Q4Label")
        self.Q4comboBox = QtWidgets.QComboBox(exportFileui)
        self.Q4comboBox.setGeometry(QtCore.QRect(40, 250, 50, 20))
        self.Q4comboBox.setObjectName("Q4comboBox")
        self.Q4comboBox.addItem("1x1")
        self.Q4comboBox.addItem("2x2")
        self.Q4comboBox.addItem("3x3")

        self.Q8Label = QtWidgets.QLabel(exportFileui)
        self.Q8Label.setGeometry(QtCore.QRect(0, 280, 200, 20))
        self.Q8Label.setObjectName("Q8Label")
        self.Q8comboBox = QtWidgets.QComboBox(exportFileui)
        self.Q8comboBox.setGeometry(QtCore.QRect(40, 280, 50, 20))
        self.Q8comboBox.setObjectName("Q8comboBox")
        self.Q8comboBox.addItem("2x2")

        self.exportpushButton = QtWidgets.QPushButton(exportFileui)
        self.exportpushButton.setAutoDefault(True)
        self.exportpushButton.setGeometry(QtCore.QRect(60, 320, 80, 23))
        self.exportpushButton.setObjectName("exportpushButton")

        self.retranslateUi(exportFileui)
        QtCore.QMetaObject.connectSlotsByName(exportFileui)

    def retranslateUi(self, exportFileui):
        _translate = QtCore.QCoreApplication.translate
        self.MainTitle.setText(_translate("MainWindow", "Export File"))
        self.optionsLabel.setText(_translate("MainWindow", "Export to :"))
        self.alLabel.setText(_translate("MainWindow", "Analysis Type :"))
        self.gpLabel.setText(_translate("MainWindow", "Gauss Points :"))
        self.T3Label.setText(_translate("MainWindow", "T3 :"))
        self.T6Label.setText(_translate("MainWindow", "T6 :"))
        self.Q4Label.setText(_translate("MainWindow", "Q4 :"))
        self.Q8Label.setText(_translate("MainWindow", "Q8 :"))
        self.optionscomboBox.setItemText(0, _translate(
            "MainWindow", "Femoolab"))
        self.aloptionscomboBox.setItemText(0, _translate(
            "MainWindow", "Plane Stress"))
        self.aloptionscomboBox.setItemText(1, _translate(
            "MainWindow", "Plane Conduction"))
        self.exportpushButton.setText(_translate("MainWindow", "Export"))


class ExportFileDisplay(QMainWindow, Ui_exportFile):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
