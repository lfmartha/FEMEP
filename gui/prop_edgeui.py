from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_prop_edge(object):

    def setupUi(self, prop_edge):
        prop_edge.setObjectName("prop_edge_ui")
        prop_edge.setMinimumSize(QtCore.QSize(200, 369))

        self.frame = QtWidgets.QFrame(prop_edge)
        self.frame.setMinimumSize(QtCore.QSize(200, 369))
        self.frame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.propertiesFrame = QtWidgets.QTabWidget(self.frame)
        self.propertiesFrame.setMinimumSize(QtCore.QSize(200, 335))
        self.propertiesFrame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.propertiesFrame.setStyleSheet("")
        self.propertiesFrame.setTabPosition(QtWidgets.QTabWidget.North)
        self.propertiesFrame.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.propertiesFrame.setIconSize(QtCore.QSize(16, 16))
        self.propertiesFrame.setElideMode(QtCore.Qt.ElideNone)
        self.propertiesFrame.setDocumentMode(True)
        self.propertiesFrame.setTabsClosable(False)
        self.propertiesFrame.setMovable(True)
        self.propertiesFrame.setTabBarAutoHide(False)
        self.propertiesFrame.setObjectName("propertiesFrame")
        self.verticalLayout.addWidget(self.propertiesFrame)
        self.closepushbutton = QtWidgets.QPushButton(self.frame)
        self.closepushbutton.setMaximumSize(QtCore.QSize(80, 23))
        self.closepushbutton.setAutoDefault(True)
        self.closegridLayout = QtWidgets.QGridLayout()
        self.closegridLayout.setContentsMargins(-1, 10, -1, 10)
        self.closegridLayout.setObjectName("closegridLayout")
        self.closegridLayout.addWidget(self.closepushbutton, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.closegridLayout)
        self.dataStructure = QtWidgets.QWidget()
        self.dataStructure.setObjectName("dataStructure")
        self.dsLabel_type_1 = QtWidgets.QLabel(self.dataStructure)
        self.dsLabel_type_1.setGeometry(QtCore.QRect(0, 20, 200, 20))
        self.dsLabel_type_1.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.dsLabel_type_1.setFont(font)
        self.dsLabel_type_1.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.dsLabel_type_1.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.dsLabel_type_1.setObjectName("dsLabel_type_1")
        self.dsLabel_firstpoint = QtWidgets.QLabel(self.dataStructure)
        self.dsLabel_firstpoint.setGeometry(QtCore.QRect(0, 40, 200, 20))
        self.dsLabel_firstpoint.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dsLabel_firstpoint.setFont(font)
        self.dsLabel_firstpoint.setStyleSheet("")
        self.dsLabel_firstpoint.setObjectName("dsLabel_firstpoint")
        self.dsLabel_endpoint = QtWidgets.QLabel(self.dataStructure)
        self.dsLabel_endpoint.setGeometry(QtCore.QRect(0, 60, 200, 20))
        self.dsLabel_endpoint.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dsLabel_endpoint.setFont(font)
        self.dsLabel_endpoint.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.dsLabel_endpoint.setObjectName("dsLabel_endpoint")
        self.dsLabel_title_1 = QtWidgets.QLabel(self.dataStructure)
        self.dsLabel_title_1.setGeometry(QtCore.QRect(0, 0, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.dsLabel_title_1.setFont(font)
        self.dsLabel_title_1.setAlignment(QtCore.Qt.AlignCenter)
        self.dsLabel_title_1.setObjectName("dsLabel_title_1")
        self.dsLabel_length = QtWidgets.QLabel(self.dataStructure)
        self.dsLabel_length.setGeometry(QtCore.QRect(0, 80, 200, 20))
        self.dsLabel_length.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dsLabel_length.setFont(font)
        self.dsLabel_length.setStyleSheet("")
        self.dsLabel_length.setObjectName("dsLabel_xcoord_2")
        self.propertiesFrame.addTab(self.dataStructure, "")
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setGeometry(QtCore.QRect(0, 240, 200, 80))
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
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.propertiesFrame.addTab(self.scrollArea, "Attributes")
        prop_edge.setCentralWidget(self.frame)

        self.retranslateUi(prop_edge)
        QtCore.QMetaObject.connectSlotsByName(prop_edge)

    def retranslateUi(self, prop_edge):
        _translate = QtCore.QCoreApplication.translate
        self.dsLabel_type_1.setText(_translate("MainWindow", "Type :"))
        self.dsLabel_firstpoint.setText(
            _translate("MainWindow", "First Point :"))
        self.dsLabel_endpoint.setText(_translate("MainWindow", "End Point:"))
        self.dsLabel_title_1.setText(_translate("MainWindow", "Geometry"))
        self.closepushbutton.setText(_translate("MainWindow", "Swap/Close"))
        self.propertiesFrame.setTabText(self.propertiesFrame.indexOf(
            self.dataStructure), _translate("MainWindow", "Data Structure"))


class Prop_EdgeDisplay(QMainWindow, Ui_prop_edge):
    def __init__(self, parent=None, frame=None):
        super().__init__(parent)
        super().setupUi(self)
        self.frame = frame

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.frame is not None:
            self.resize(self.frame.size())
        return super().resizeEvent(a0)

    def set_edge_prop(self, _edge):

        first_point = (round(_edge.segment.getXinit(), 3),
                       round(_edge.segment.getYinit(), 3))
        end_point = (round(_edge.segment.getXend(), 3),
                     round(_edge.segment.getYend(), 3))
        length = round(_edge.segment.length(0, 1), 3)

        if _edge.segment.getType() == 'LINE':
            self.dsLabel_type_1.setText("Type : Line")
        elif _edge.segment.getType() == 'POLYLINE':
            self.dsLabel_type_1.setText("Type : Polyline")

        self.dsLabel_firstpoint.setText(
            f"First Point : {first_point}")
        self.dsLabel_endpoint.setText(
            f"End Point : {end_point}")
        self.dsLabel_length.setText(f"Length : {length}")

        # get attributes
        attributes = _edge.segment.attributes

        # creates Qwidget
        scrollAreaContent = QtWidgets.QWidget()
        Layout = QtWidgets.QVBoxLayout(scrollAreaContent)

        # set widget in scrollArea
        self.scrollArea.setWidget(scrollAreaContent)

        # creates QFrame
        content = QtWidgets.QFrame(scrollAreaContent)

        Layout.setContentsMargins(0, 0, 0, 0)
        Layout.setSpacing(0)
        Layout.addWidget(content)

        index = 0
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font1 = QtGui.QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setWeight(75)
        for att in attributes:
            Label = QtWidgets.QLabel(content)
            Label.setAlignment(
                QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            Label.setGeometry(QtCore.QRect(0, index*20, 200, 20))
            Label.setFont(font)
            Label.setText(att['type'])
            properties = att['properties']

            if index % 2 == 0:
                Label.setStyleSheet("")
            else:
                Label.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")
            index += 1

            nameLabel = QtWidgets.QLabel(content)
            nameLabel.setGeometry(QtCore.QRect(0, index*20, 200, 20))
            nameLabel.setFont(font1)
            nameLabel.setText(f"Name : {att['name']}")

            if index % 2 == 0:
                nameLabel.setStyleSheet("")
            else:
                nameLabel.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")
            index += 1

            for key in properties:

                value = properties[key]
                if type(value) == list:
                    if len(value) == 3:
                        continue
                    else:
                        value = properties[key][0][properties[key][1]]

                propLabel = QtWidgets.QLabel(content)
                propLabel.setGeometry(QtCore.QRect(0, index*20, 200, 20))
                propLabel.setFont(font1)
                propLabel.setText(f"{key} : {value}")

                if index % 2 == 0:
                    propLabel.setStyleSheet("")
                else:
                    propLabel.setStyleSheet(
                        "background-color: rgb(255, 255, 255);")
                index += 1

        content.setMinimumSize(QtCore.QSize(200, 20*index))
