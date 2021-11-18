from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_mesh(object):
    def setupUi(self, meshui):
        meshui.setObjectName("pointui")
        meshui.resize(200, 369)
        meshui.setMaximumSize(QtCore.QSize(200, 16777215))

        self.mainTitlelabel = QtWidgets.QLabel(meshui)
        self.mainTitlelabel.setGeometry(QtCore.QRect(0, 10, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mainTitlelabel.setFont(font)
        self.mainTitlelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainTitlelabel.setObjectName("mainTitlelabel")
        self.meshcomboBox = QtWidgets.QComboBox(meshui)
        self.meshcomboBox.setGeometry(QtCore.QRect(10, 70, 180, 20))
        self.meshcomboBox.setObjectName("meshcomboBox")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshTypesLabel = QtWidgets.QLabel(meshui)
        self.meshTypesLabel.setGeometry(QtCore.QRect(0, 40, 200, 20))
        self.meshTypesLabel.setObjectName("meshTypesLabel")
        self.elemTypesLAbel = QtWidgets.QLabel(meshui)
        self.elemTypesLAbel.setGeometry(QtCore.QRect(0, 100, 200, 20))
        self.elemTypesLAbel.setObjectName("elemTypesLAbel")
        self.shapecomboBox = QtWidgets.QComboBox(meshui)
        self.shapecomboBox.setGeometry(QtCore.QRect(25, 130, 150, 20))
        self.shapecomboBox.setObjectName("shapecomboBox")
        self.shapecomboBox.addItem("")
        self.shapecomboBox.addItem("")
        self.elemcomboBox = QtWidgets.QComboBox(meshui)
        self.elemcomboBox.setGeometry(QtCore.QRect(25, 160, 150, 20))
        self.elemcomboBox.setObjectName("elemcomboBox")
        self.elemcomboBox.addItem("")
        self.elemcomboBox.addItem("")
        self.diagTypesLabel = QtWidgets.QLabel(meshui)
        self.diagTypesLabel.setGeometry(QtCore.QRect(0, 190, 200, 20))
        self.diagTypesLabel.setObjectName("diagTypesLabel")
        self.flagLabel = QtWidgets.QLabel(meshui)
        self.flagLabel.setGeometry(QtCore.QRect(0, 160, 200, 20))
        self.flagLabel.setObjectName("flagLabel")
        self.diagcomboBox = QtWidgets.QComboBox(meshui)
        self.diagcomboBox.setGeometry(QtCore.QRect(25, 220, 150, 20))
        self.diagcomboBox.setObjectName("diagcomboBox")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")
        self.flagcomboBox = QtWidgets.QComboBox(meshui)
        self.flagcomboBox.setGeometry(QtCore.QRect(25, 190, 150, 20))
        self.flagcomboBox.setObjectName("flagcomboBox")
        self.flagcomboBox.addItem("")
        self.flagcomboBox.addItem("")
        self.flagcomboBox.addItem("")
        self.genMeshpushButton = QtWidgets.QPushButton(meshui)
        self.genMeshpushButton.setGeometry(QtCore.QRect(55, 230, 90, 23))
        self.genMeshpushButton.setObjectName("genMeshpushButton")
        self.delMeshpushButton = QtWidgets.QPushButton(meshui)
        self.delMeshpushButton.setGeometry(QtCore.QRect(55, 260, 90, 23))
        self.delMeshpushButton.setObjectName("genMeshpushButton")

        self.retranslateUi(meshui)
        QtCore.QMetaObject.connectSlotsByName(meshui)

    def retranslateUi(self, meshui):
        _translate = QtCore.QCoreApplication.translate
        self.mainTitlelabel.setText(_translate("MainWindow", "Mesh Manager"))
        self.meshcomboBox.setCurrentText(
            _translate("MainWindow", "Bilinear Transfinite "))
        self.meshcomboBox.setItemText(0, _translate(
            "MainWindow", "Bilinear Transfinite"))
        self.meshcomboBox.setItemText(1, _translate(
            "MainWindow", "Trilinear Transfinite"))
        self.meshcomboBox.setItemText(2, _translate(
            "MainWindow", "Triangular Boundary Contraction"))
        self.meshcomboBox.setItemText(
            3, _translate("MainWindow", "Quadrilateral Seam"))
        self.meshcomboBox.setItemText(
            4, _translate("MainWindow", "Quadrilateral Template"))
        self.meshTypesLabel.setText(_translate("MainWindow", " Mesh Types :"))
        self.elemTypesLAbel.setText(
            _translate("MainWindow", "Element Types :"))
        self.diagTypesLabel.setText(
            _translate("MainWindow", "Diagonal Types :"))
        self.flagLabel.setText(
            _translate("MainWindow", "Based on:"))
        self.shapecomboBox.setItemText(
            0, _translate("MainWindow", "Triangular"))
        self.shapecomboBox.setItemText(
            1, _translate("MainWindow", "Quadrilateral"))
        self.elemcomboBox.setItemText(
            0, _translate("MainWindow", "Linear"))
        self.elemcomboBox.setItemText(
            1, _translate("MainWindow", "Quadratic"))
        self.diagcomboBox.setItemText(0, _translate("MainWindow", "Right"))
        self.diagcomboBox.setItemText(1, _translate("MainWindow", "Left"))
        self.diagcomboBox.setItemText(
            2, _translate("MainWindow", "Union Jack"))
        self.diagcomboBox.setItemText(3, _translate("MainWindow", "Optimal"))
        self.flagcomboBox.setItemText(0, _translate("MainWindow", "Optimal"))
        self.flagcomboBox.setItemText(1, _translate("MainWindow", "Quadtree"))
        self.flagcomboBox.setItemText(
            2, _translate("MainWindow", "Regular Grid"))
        self.genMeshpushButton.setText(
            _translate("MainWindow", "Generate Mesh"))
        self.delMeshpushButton.setText(
            _translate("MainWindow", "Delete Mesh"))


class MeshDisplay(QMainWindow, Ui_mesh):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
