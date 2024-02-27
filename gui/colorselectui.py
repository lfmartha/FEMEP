from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_ColorSelect(object):
    def setupUi(self, ColorSelect):
        ColorSelect.setObjectName("ColorSelect")
        ColorSelect.resize(400, 180)
        ColorSelect.setMinimumSize(QtCore.QSize(390, 180))
        ColorSelect.setMaximumSize(QtCore.QSize(390, 180))
        self.redlabel = QtWidgets.QLabel(ColorSelect)
        self.redlabel.setGeometry(QtCore.QRect(10, 10, 40, 20))
        self.redlabel.setObjectName("redlabel")
        self.greenlabel = QtWidgets.QLabel(ColorSelect)
        self.greenlabel.setGeometry(QtCore.QRect(10, 50, 40, 20))
        self.greenlabel.setObjectName("greenlabel")
        self.bluelabel = QtWidgets.QLabel(ColorSelect)
        self.bluelabel.setGeometry(QtCore.QRect(10, 90, 40, 20))
        self.bluelabel.setObjectName("bluelabel")
        self.redhorizontalSlider = QtWidgets.QSlider(ColorSelect)
        self.redhorizontalSlider.setGeometry(QtCore.QRect(60, 10, 160, 20))
        self.redhorizontalSlider.setAutoFillBackground(True)
        self.redhorizontalSlider.setStyleSheet("")
        self.redhorizontalSlider.setMaximum(255)
        self.redhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.redhorizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.redhorizontalSlider.setObjectName("redhorizontalSlider")
        self.greenhorizontalSlider = QtWidgets.QSlider(ColorSelect)
        self.greenhorizontalSlider.setGeometry(QtCore.QRect(60, 50, 160, 22))
        self.greenhorizontalSlider.setMaximum(255)
        self.greenhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.greenhorizontalSlider.setObjectName("greenhorizontalSlider")
        self.bluehorizontalSlider = QtWidgets.QSlider(ColorSelect)
        self.bluehorizontalSlider.setGeometry(QtCore.QRect(60, 90, 160, 22))
        self.bluehorizontalSlider.setMaximum(255)
        self.bluehorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.bluehorizontalSlider.setObjectName("bluehorizontalSlider")
        self.colorwidget = QtWidgets.QWidget(ColorSelect)
        self.colorwidget.setGeometry(QtCore.QRect(290, 10, 90, 100))
        self.colorwidget.setAutoFillBackground(True)
        self.colorwidget.setObjectName("colorwidget")
        self.redspinBox = QtWidgets.QSpinBox(ColorSelect)
        self.redspinBox.setGeometry(QtCore.QRect(230, 10, 40, 20))
        self.redspinBox.setMaximum(255)
        self.redspinBox.setObjectName("redspinBox")
        self.greenspinBox = QtWidgets.QSpinBox(ColorSelect)
        self.greenspinBox.setGeometry(QtCore.QRect(230, 50, 40, 20))
        self.greenspinBox.setMaximum(255)
        self.greenspinBox.setObjectName("greenspinBox")
        self.bluespinBox = QtWidgets.QSpinBox(ColorSelect)
        self.bluespinBox.setGeometry(QtCore.QRect(230, 90, 40, 20))
        self.bluespinBox.setMaximum(255)
        self.bluespinBox.setObjectName("bluespinBox")
        self.pushButton = QtWidgets.QPushButton(ColorSelect)
        self.pushButton.setGeometry(QtCore.QRect(160, 140, 80, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(ColorSelect)
        QtCore.QMetaObject.connectSlotsByName(ColorSelect)

        self.onColorChanged()

    def retranslateUi(self, ColorSelect):
        _translate = QtCore.QCoreApplication.translate
        ColorSelect.setWindowTitle(_translate("ColorSelect", "Color Select"))
        self.redlabel.setText(_translate("ColorSelect", "Red"))
        self.greenlabel.setText(_translate("ColorSelect", "Green"))
        self.bluelabel.setText(_translate("ColorSelect", "Blue"))
        self.pushButton.setText(_translate("ColorSelect", "OK"))


class ColorSelectDisplay(QMainWindow, Ui_ColorSelect):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.lineEdit = None

        # buttons
        self.pushButton.clicked.connect(self.setColor)
        self.redhorizontalSlider.valueChanged['int'].connect(
            self.redSlider)
        self.greenhorizontalSlider.valueChanged['int'].connect(
            self.greenSlider)
        self.bluehorizontalSlider.valueChanged['int'].connect(
            self.blueSlider)
        self.redspinBox.valueChanged['int'].connect(
            self.redSpin)
        self.greenspinBox.valueChanged['int'].connect(
            self.greenSpin)
        self.bluespinBox.valueChanged['int'].connect(
            self.blueSpin)

    def Display(self):
        self.show()
        txt = self.lineEdit.text()
        txt = txt.replace("[", "")
        txt = txt.replace("]", "")
        txt = txt.split(",")
        rgbColor = []
        for item in txt:
            rgbColor.append(int(item))
        self.redspinBox.setValue(rgbColor[0])
        self.greenspinBox.setValue(rgbColor[1])
        self.bluespinBox.setValue(rgbColor[2])

    def setColor(self):
        r = self.redspinBox.value()
        g = self.greenspinBox.value()
        b = self.bluespinBox.value()
        self.lineEdit.setText(f"[{r},{g},{b}]")
        self.close()

    def redSpin(self, _int):
        self.redhorizontalSlider.setValue(_int)
        self.onColorChanged()

    def greenSpin(self, _int):
        self.greenhorizontalSlider.setValue(_int)
        self.onColorChanged()

    def blueSpin(self, _int):
        self.bluehorizontalSlider.setValue(_int)
        self.onColorChanged()

    def redSlider(self, _int):
        self.redspinBox.setValue(_int)
        self.onColorChanged()

    def greenSlider(self, _int):
        self.greenspinBox.setValue(_int)
        self.onColorChanged()

    def blueSlider(self, _int):
        self.bluespinBox.setValue(_int)
        self.onColorChanged()

    def onColorChanged(self):
        self.colorwidget.setStyleSheet(
            f"background-color: rgb{self.redspinBox.value(),self.greenhorizontalSlider.value(),self.bluespinBox.value()}")
