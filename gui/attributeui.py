from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from gui.colorselectui import ColorSelectDisplay


class Ui_attribute(object):

    def setupUi(self, attributeui):
        attributeui.setObjectName("attributeui")
        attributeui.setMinimumSize(QtCore.QSize(200, 369))

        self.AttribFrame = QtWidgets.QFrame(attributeui)
        self.AttribFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.AttribFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AttribFrame.setObjectName("AttribFrame")
        self.AttribFrame.setMinimumSize(QtCore.QSize(200, 369))
        self.AttribFrame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.AttribFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.attTitleframe = QtWidgets.QFrame(attributeui)
        self.attTitleframe.setMinimumSize(QtCore.QSize(200, 30))
        self.attTitleframe.setMaximumSize(QtCore.QSize(200, 30))
        self.attTitleframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.attTitleframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.attTitleframe.setObjectName("attTitleframe")
        self.attTitle = QtWidgets.QLabel(self.attTitleframe)
        self.attTitle.setGeometry(QtCore.QRect(0, 10, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.attTitle.setFont(font)
        self.attTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.attTitle.setObjectName("attTitle")
        self.verticalLayout.addWidget(self.attTitleframe)
        self.typesTitleframe = QtWidgets.QFrame(self.AttribFrame)
        self.typesTitleframe.setMinimumSize(QtCore.QSize(200, 30))
        self.typesTitleframe.setMaximumSize(QtCore.QSize(200, 30))
        self.typesTitleframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.typesTitleframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.typesTitleframe.setObjectName("typesTitleframe")
        self.typesTitle = QtWidgets.QLabel(self.typesTitleframe)
        self.typesTitle.setGeometry(QtCore.QRect(0, 0, 200, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.typesTitle.setFont(font)
        self.typesTitle.setObjectName("typesTitle")
        self.verticalLayout.addWidget(self.typesTitleframe)
        self.typesgridLayout = QtWidgets.QGridLayout()
        self.typesgridLayout.setContentsMargins(-1, -1, -1, 10)
        self.typesgridLayout.setObjectName("typesgridLayout")
        self.typescomboBox = QtWidgets.QComboBox(self.AttribFrame)
        self.typescomboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.typescomboBox.setMaximumSize(QtCore.QSize(150, 20))
        self.typescomboBox.setObjectName("typescomboBox")
        self.typesgridLayout.addWidget(self.typescomboBox, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.typesgridLayout)
        self.namegridLayout = QtWidgets.QGridLayout()
        self.namegridLayout.setContentsMargins(0, -1, 0, -1)
        self.namegridLayout.setHorizontalSpacing(0)
        self.namegridLayout.setVerticalSpacing(10)
        self.namegridLayout.setObjectName("namegridLayout")
        self.nameFrame = QtWidgets.QFrame(self.AttribFrame)
        self.nameFrame.setMinimumSize(QtCore.QSize(200, 30))
        self.nameFrame.setMaximumSize(QtCore.QSize(200, 30))
        self.nameFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nameFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nameFrame.setObjectName("nameFrame")
        self.nameTitle = QtWidgets.QLabel(self.nameFrame)
        self.nameTitle.setGeometry(QtCore.QRect(0, 0, 200, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.nameTitle.setFont(font)
        self.nameTitle.setObjectName("nameTitle")
        self.namelineEdit = QtWidgets.QLineEdit(self.nameFrame)
        self.namelineEdit.setGeometry(QtCore.QRect(40, 0, 155, 20))
        self.namelineEdit.setMaximumSize(QtCore.QSize(155, 20))
        self.namelineEdit.setObjectName("namelineEdit")
        self.namegridLayout.addWidget(self.nameFrame, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.namegridLayout)
        self.addgridLayout = QtWidgets.QGridLayout()
        self.addgridLayout.setContentsMargins(-1, -1, -1, 10)
        self.addgridLayout.setObjectName("addgridLayout")
        self.addpushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.addpushButton.setMaximumSize(QtCore.QSize(80, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.addpushButton.setFont(font)
        self.addpushButton.setObjectName("addpushButton")
        self.addpushButton.setAutoDefault(True)
        self.addgridLayout.addWidget(self.addpushButton, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.addgridLayout)
        self.attsTitle = QtWidgets.QLabel(self.AttribFrame)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.attsTitle.setFont(font)
        self.attsTitle.setObjectName("attsTitle")
        self.verticalLayout.addWidget(self.attsTitle)
        self.attgridLayout = QtWidgets.QGridLayout()
        self.attgridLayout.setContentsMargins(-1, 10, -1, 10)
        self.attgridLayout.setObjectName("attgridLayout")
        self.attcomboBox = QtWidgets.QComboBox(self.AttribFrame)
        self.attcomboBox.setMaximumSize(QtCore.QSize(150, 20))
        self.attcomboBox.setObjectName("attcomboBox")
        self.attgridLayout.addWidget(self.attcomboBox, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.attgridLayout)
        self.toolbargridLayout = QtWidgets.QGridLayout()
        self.toolbargridLayout.setContentsMargins(5, 10, 5, 20)
        self.toolbargridLayout.setSpacing(5)
        self.toolbargridLayout.setObjectName("toolbargridLayout")
        self.setAttpushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.setAttpushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.setAttpushButton.setObjectName("setAttpushButton")
        self.setAttpushButton.setAutoDefault(True)
        self.toolbargridLayout.addWidget(self.setAttpushButton, 0, 0, 1, 1)
        self.unsetpushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.unsetpushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.unsetpushButton.setObjectName("renamepushButton")
        self.unsetpushButton.setAutoDefault(True)
        self.toolbargridLayout.addWidget(self.unsetpushButton, 0, 1, 1, 1)
        self.saveAttpushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.saveAttpushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.saveAttpushButton.setObjectName("saveAttpushButton")
        self.saveAttpushButton.setAutoDefault(True)
        self.toolbargridLayout.addWidget(self.saveAttpushButton, 0, 2, 1, 1)
        self.delpushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.delpushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.delpushButton.setObjectName("delpushButton")
        self.delpushButton.setAutoDefault(True)
        self.toolbargridLayout.addWidget(self.delpushButton, 1, 0, 1, 1)
        self.renamepushButton = QtWidgets.QPushButton(self.AttribFrame)
        self.renamepushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.renamepushButton.setObjectName("renamepushButton")
        self.renamepushButton.setAutoDefault(True)
        self.toolbargridLayout.addWidget(self.renamepushButton, 1, 1, 1, 1)
        self.renamelineEdit = QtWidgets.QLineEdit(self.AttribFrame)
        self.renamelineEdit.setObjectName("renamelineEdit")
        self.toolbargridLayout.addWidget(self.renamelineEdit, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.toolbargridLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.AttribFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.verticalLayout.addWidget(self.scrollArea)
        attributeui.setCentralWidget(self.AttribFrame)

        self.retranslateUi(attributeui)
        QtCore.QMetaObject.connectSlotsByName(attributeui)

    def retranslateUi(self, attributeui):
        _translate = QtCore.QCoreApplication.translate
        self.attTitle.setText(_translate("MainWindow", "Attribute Manager"))
        self.typesTitle.setText(_translate("MainWindow", "Types:"))
        self.addpushButton.setText(_translate("MainWindow", "Add"))
        self.nameTitle.setText(_translate("MainWindow", "Name :"))
        self.attsTitle.setText(_translate("MainWindow", "Atrributes :"))
        self.saveAttpushButton.setText(_translate("MainWindow", "Save"))
        self.delpushButton.setText(_translate("MainWindow", "Del"))
        self.setAttpushButton.setText(_translate("MainWindow", "Set"))
        self.renamepushButton.setText(_translate("MainWindow", "Rename"))
        self.unsetpushButton.setText(_translate("MainWindow", "Unset"))


class AttributeDisplay(QMainWindow, Ui_attribute):
    def __init__(self, parent=None, frame=None):
        super().__init__(parent)
        super().setupUi(self)
        self.frame = frame

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.frame is not None:
            self.resize(self.frame.size())
        return super().resizeEvent(a0)

    def setAttPropertiesDisplay(self, _attribute):

        # creates Qwidget
        scrollAreaContent = QtWidgets.QWidget()
        Layout = QtWidgets.QVBoxLayout(scrollAreaContent)

        # set widget in scrollArea
        self.scrollArea.setWidget(scrollAreaContent)

        if _attribute is None:
            return

        attValues = _attribute['properties']
        attValues_type = _attribute['properties_type']

        # creates QFrame
        content = QtWidgets.QFrame(scrollAreaContent)
        content.setMinimumSize(QtCore.QSize(200, 20*len(attValues)))
        Layout.setContentsMargins(0, 0, 0, 0)
        Layout.setSpacing(0)
        Layout.addWidget(content)

        # creates labels and sets labels texts
        index = 0
        attpropertiesItems = []
        for key in attValues:
            valueLabel = QtWidgets.QLabel(content)
            valueLabel.setGeometry(QtCore.QRect(0, index*20, 200, 20))
            valueLabel.setText(key)

            if index % 2 == 0:
                valueLabel.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")
            else:
                valueLabel.setStyleSheet("")

            if attValues_type[index] == "float":
                lineEdit = QtWidgets.QLineEdit(content)
                lineEdit.setGeometry(QtCore.QRect(80, index*20, 100, 20))
                lineEdit.setStyleSheet("background-color: transparent;")
                lineEdit.setFrame(False)
                lineEdit.setValidator(QtGui.QDoubleValidator())
                lineEdit.setText(f"{attValues[key]}")
                attpropertiesItems.append(lineEdit)
            elif attValues_type[index] == "int":
                lineEdit = QtWidgets.QLineEdit(content)
                lineEdit.setGeometry(QtCore.QRect(80, index*20, 100, 20))
                lineEdit.setStyleSheet("background-color: transparent;")
                lineEdit.setFrame(False)
                lineEdit.setValidator(QtGui.QIntValidator())
                lineEdit.setText(f"{attValues[key]}")
                attpropertiesItems.append(lineEdit)
            elif attValues_type[index] == "string":
                lineEdit = QtWidgets.QLineEdit(content)
                lineEdit.setGeometry(QtCore.QRect(80, index*20, 100, 20))
                lineEdit.setStyleSheet("background-color: transparent;")
                lineEdit.setFrame(False)
                lineEdit.setText(f"{attValues[key]}")
                attpropertiesItems.append(lineEdit)
            elif attValues_type[index] == "bool":
                contentRB = QtWidgets.QFrame(content)
                contentRB.setGeometry(QtCore.QRect(80, index*20, 100, 20))
                trueradioButton = QtWidgets.QRadioButton(contentRB)
                trueradioButton.setGeometry(QtCore.QRect(0, 0, 50, 20))
                trueradioButton.setText("True")
                falseradioButton = QtWidgets.QRadioButton(contentRB)
                falseradioButton.setGeometry(
                    QtCore.QRect(50, 0, 50, 20))
                falseradioButton.setText("False")
                attpropertiesItems.append(trueradioButton)

                if attValues[key]:
                    trueradioButton.setChecked(True)
                else:
                    falseradioButton.setChecked(True)
            elif attValues_type[index] == "color":
                lineEdit = QtWidgets.QLineEdit(content)
                lineEdit.setGeometry(QtCore.QRect(80, index*20, 80, 20))
                lineEdit.setStyleSheet("background-color: transparent;")
                lineEdit.setFrame(False)
                lineEdit.setText(f"{attValues[key]}")
                toolButton = QtWidgets.QToolButton(content)
                toolButton.setText("...")
                toolButton.setGeometry(160, index*20, 20, 20)
                colorDisp = ColorSelectDisplay(self)
                colorDisp.lineEdit = lineEdit
                toolButton.clicked.connect(colorDisp.Display)
                attpropertiesItems.append(lineEdit)
            elif attValues_type[index] == "options":
                comboBox = QtWidgets.QComboBox(content)
                comboBox.setGeometry(QtCore.QRect(80, index*20, 100, 20))
                options = attValues[key]["list"]
                for item in options:
                    comboBox.addItem(f"{item}")
                comboBox.setCurrentIndex(attValues[key]["index"])
                attpropertiesItems.append(comboBox)

            index += 1

        return attpropertiesItems
