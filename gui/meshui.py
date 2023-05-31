from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_mesh(object):
    def setupUi(self, meshui):
        meshui.setObjectName("pointui")
        meshui.resize(200, 800)
        meshui.setMaximumSize(QtCore.QSize(200, 16777215))

        # Main Title
        self.mainTitlelabel = QtWidgets.QLabel(meshui)
        self.mainTitlelabel.setGeometry(QtCore.QRect(0, 10, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mainTitlelabel.setFont(font)
        self.mainTitlelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainTitlelabel.setObjectName("mainTitlelabel")

        # Mesh Type
        self.meshTypesLabel = QtWidgets.QLabel(meshui)
        self.meshTypesLabel.setGeometry(QtCore.QRect(0, 40, 200, 20))
        self.meshTypesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.meshTypesLabel.setObjectName("meshTypesLabel")

        self.meshcomboBox = QtWidgets.QComboBox(meshui)
        self.meshcomboBox.setGeometry(QtCore.QRect(25, 60, 150, 25))
        self.meshcomboBox.setObjectName("meshcomboBox")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")
        self.meshcomboBox.addItem("")

        # Element Type
        self.elemTypesLAbel = QtWidgets.QLabel(meshui)
        self.elemTypesLAbel.setGeometry(QtCore.QRect(0, 105, 200, 20))
        self.elemTypesLAbel.setAlignment(QtCore.Qt.AlignCenter)
        self.elemTypesLAbel.setObjectName("elemTypesLAbel")

        self.shapecomboBox = QtWidgets.QComboBox(meshui)
        self.shapecomboBox.setGeometry(QtCore.QRect(25, 125, 150, 25))
        self.shapecomboBox.setObjectName("shapecomboBox")
        self.shapecomboBox.addItem("")
        self.shapecomboBox.addItem("")

        self.elemcomboBox = QtWidgets.QComboBox(meshui)
        self.elemcomboBox.setGeometry(QtCore.QRect(25, 155, 150, 25))
        self.elemcomboBox.setObjectName("elemcomboBox")
        self.elemcomboBox.addItem("")
        self.elemcomboBox.addItem("")

        # Diagonal Type
        self.diagTypesLabel = QtWidgets.QLabel(meshui)
        self.diagTypesLabel.setGeometry(QtCore.QRect(0, 200, 200, 20))
        self.diagTypesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.diagTypesLabel.setObjectName("diagTypesLabel")

        self.diagcomboBox = QtWidgets.QComboBox(meshui)
        self.diagcomboBox.setGeometry(QtCore.QRect(25, 220, 150, 25))
        self.diagcomboBox.setObjectName("diagcomboBox")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")
        self.diagcomboBox.addItem("")

        # Flag based on
        self.flagLabel = QtWidgets.QLabel(meshui)
        self.flagLabel.setGeometry(QtCore.QRect(0, 265, 200, 20))
        self.flagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.flagLabel.setObjectName("flagLabel")

        self.flagcomboBox = QtWidgets.QComboBox(meshui)
        self.flagcomboBox.setGeometry(QtCore.QRect(25, 285, 150, 25))
        self.flagcomboBox.setObjectName("flagcomboBox")
        self.flagcomboBox.addItem("")
        self.flagcomboBox.addItem("")
        self.flagcomboBox.addItem("")

        self.genMeshpushButton = QtWidgets.QPushButton(meshui)
        self.genMeshpushButton.setAutoDefault(True)
        self.genMeshpushButton.setGeometry(QtCore.QRect(50, 330, 100, 25))
        self.genMeshpushButton.setObjectName("genMeshpushButton")

        self.delMeshpushButton = QtWidgets.QPushButton(meshui)
        self.delMeshpushButton.setAutoDefault(True)
        self.delMeshpushButton.setGeometry(QtCore.QRect(50, 360, 100, 25))
        self.delMeshpushButton.setObjectName("genMeshpushButton")

        self.retranslateUi(meshui)
        QtCore.QMetaObject.connectSlotsByName(meshui)

    def retranslateUi(self, meshui):
        _translate = QtCore.QCoreApplication.translate
        self.mainTitlelabel.setText(_translate("MainWindow", "Mesh Manager"))

        self.meshTypesLabel.setText(_translate("MainWindow", "Mesh Types:"))
        self.meshcomboBox.setCurrentText(_translate("MainWindow", "Bilinear Transfinite"))
        self.meshcomboBox.setItemText(0, _translate("MainWindow", "Bilinear Transfinite"))
        self.meshcomboBox.setItemText(1, _translate("MainWindow", "Trilinear Transfinite"))
        self.meshcomboBox.setItemText(2, _translate("MainWindow", "Triangular Boundary Contraction"))
        self.meshcomboBox.setItemText(3, _translate("MainWindow", "Quadrilateral Seam"))
        self.meshcomboBox.setItemText(4, _translate("MainWindow", "Quadrilateral Template"))
        self.meshcomboBox.setItemText(5, _translate("MainWindow", "Isogeometric"))
        self.meshcomboBox.setItemText(6, _translate("MainWindow", "Isogeometric Template"))

        self.elemTypesLAbel.setText(_translate("MainWindow", "Element Types:"))
        self.shapecomboBox.setItemText(0, _translate("MainWindow", "Triangular"))
        self.shapecomboBox.setItemText(1, _translate("MainWindow", "Quadrilateral"))
        self.elemcomboBox.setItemText(0, _translate("MainWindow", "Linear"))
        self.elemcomboBox.setItemText(1, _translate("MainWindow", "Quadratic"))

        self.diagTypesLabel.setText(_translate("MainWindow", "Diagonal Types:"))
        self.diagcomboBox.setItemText(0, _translate("MainWindow", "Right"))
        self.diagcomboBox.setItemText(1, _translate("MainWindow", "Left"))
        self.diagcomboBox.setItemText(2, _translate("MainWindow", "Union Jack"))
        self.diagcomboBox.setItemText(3, _translate("MainWindow", "Optimal"))

        self.flagLabel.setText(_translate("MainWindow", "Based on:"))
        self.flagcomboBox.setItemText(0, _translate("MainWindow", "Optimal"))
        self.flagcomboBox.setItemText(1, _translate("MainWindow", "Quadtree"))
        self.flagcomboBox.setItemText(2, _translate("MainWindow", "Regular Grid"))

        self.genMeshpushButton.setText(_translate("MainWindow", "Generate Mesh"))
        self.delMeshpushButton.setText(_translate("MainWindow", "Delete Mesh"))


class MeshDisplay(QMainWindow, Ui_mesh):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)