from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_prop_edge(object):

    def setupUi(self, prop_edge):
        prop_edge.setObjectName("prop_edge_ui")
        prop_edge.setMinimumSize(QtCore.QSize(200, 400))

        self.frame = QtWidgets.QFrame(prop_edge)
        self.frame.setMinimumSize(QtCore.QSize(200, 400))
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
        self.closepushbutton.setMaximumSize(QtCore.QSize(80, 25))
        self.closepushbutton.setAutoDefault(True)

        self.degreeChange = QtWidgets.QPushButton(self.frame)
        self.degreeChange.setMaximumSize(QtCore.QSize(100, 25))
        self.degreeChange.setAutoDefault(True)

        self.degreelineEdit = QtWidgets.QLineEdit(self.frame)
        self.degreelineEdit.setValidator(QtGui.QDoubleValidator())
        self.degreelineEdit.setMaximumSize(QtCore.QSize(70, 20))
        # self.degreelineEdit.setGeometry(QtCore.QRect(80, 390, 70, 20))
        self.degreelineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        self.degreelineEdit.setObjectName("degreelineEdit")

        self.closegridLayout = QtWidgets.QGridLayout()
        self.closegridLayout.setContentsMargins(-1, 10, -1, 10)
        self.closegridLayout.setObjectName("closegridLayout")
        self.closegridLayout.addWidget(self.closepushbutton, 0, 0, 1, 1)
        self.closegridLayout.addWidget(self.degreeChange, 0, 20, 1, 1)
        self.closegridLayout.addWidget(self.degreelineEdit, 0, 40, 1, 1)

        self.verticalLayout.addLayout(self.closegridLayout)

        self.scrollAreaDS = QtWidgets.QScrollArea()
        self.scrollAreaDS.setGeometry(QtCore.QRect(0, 240, 200, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaDS.sizePolicy().hasHeightForWidth())
        self.scrollAreaDS.setSizePolicy(sizePolicy)
        self.scrollAreaDS.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollAreaDS.setLineWidth(0)
        self.scrollAreaDS.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaDS.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaDS.setWidgetResizable(True)
        self.scrollAreaDS.setObjectName("scrollAreaDS")

        self.propertiesFrame.addTab(self.scrollAreaDS, "Data Structure")

        self.scrollAreaAtt = QtWidgets.QScrollArea()
        self.scrollAreaAtt.setGeometry(QtCore.QRect(0, 240, 200, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaAtt.sizePolicy().hasHeightForWidth())
        self.scrollAreaAtt.setSizePolicy(sizePolicy)
        self.scrollAreaAtt.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollAreaAtt.setLineWidth(0)
        self.scrollAreaAtt.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaAtt.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaAtt.setWidgetResizable(True)
        self.scrollAreaAtt.setObjectName("scrollAreaAtt")


        #self.degreeChange = QtWidgets.QPushButton()
        #self.degreelineEdit = QtWidgets.QLineEdit()
        
        # #index += 25
        # self.newDegreeTitle = QtWidgets.QLabel(self.frame)
        # #self.newDegreeTitle.setGeometry(QtCore.QRect(0, index, 75, 20))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.newDegreeTitle.setFont(font)
        # self.newDegreeTitle.setStyleSheet("color: rgb(0, 0, 0);\n""")
        # self.newDegreeTitle.setAlignment(QtCore.Qt.AlignCenter)
        # self.newDegreeTitle.setObjectName("newDegreeTitle")
        # self.newDegreeTitle.setText("New Degree:")

        # self.degreelineEdit = QtWidgets.QLineEdit(self.frame)
        # self.degreelineEdit.setValidator(QtGui.QDoubleValidator())
        # #self.degreelineEdit.setGeometry(QtCore.QRect(80, index, 70, 20))
        # self.degreelineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n""color: rgb(0, 0, 0);\n""")
        # self.degreelineEdit.setObjectName("degreelineEdit")

        # #index += 30
        # self.degreeChange = QtWidgets.QPushButton(self.frame)
        # self.degreeChange.setAutoDefault(True)
        # #self.degreeChange.setGeometry(QtCore.QRect(50, index, 100, 25))
        # self.degreeChange.setText("Change degree")

        self.propertiesFrame.addTab(self.scrollAreaAtt, "Attributes")
        
        prop_edge.setCentralWidget(self.frame)

        self.retranslateUi(prop_edge)
        QtCore.QMetaObject.connectSlotsByName(prop_edge)

    def retranslateUi(self, prop_edge):
        _translate = QtCore.QCoreApplication.translate
        self.closepushbutton.setText(_translate("MainWindow", "Swap/Close"))
        self.degreeChange.setText(_translate("MainWindow", "Change Degree"))


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

        # get control points and knot vector
        nurbs = _edge.segment.getNurbs()
        Degree = nurbs.degree
        CtrlPts = nurbs.ctrlpts
        KnotVector = nurbs.knotvector

        # creates Qwidget
        scrollAreaContentDS = QtWidgets.QWidget()
        LayoutDS = QtWidgets.QVBoxLayout(scrollAreaContentDS)

        # set widget in scrollArea
        self.scrollAreaDS.setWidget(scrollAreaContentDS)

        # creates QFrame
        contentDS = QtWidgets.QFrame(scrollAreaContentDS)

        LayoutDS.setContentsMargins(0, 0, 0, 0)
        LayoutDS.setSpacing(0)
        LayoutDS.addWidget(contentDS)

        dsLabel_title_1 = QtWidgets.QLabel(contentDS)
        dsLabel_title_1.setGeometry(QtCore.QRect(0, 0, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        dsLabel_title_1.setFont(font)
        dsLabel_title_1.setAlignment(QtCore.Qt.AlignCenter)
        dsLabel_title_1.setObjectName("dsLabel_title_1")
        dsLabel_title_1.setText("Geometry")

        dsLabel_type_1 = QtWidgets.QLabel(contentDS)
        dsLabel_type_1.setGeometry(QtCore.QRect(0, 20, 200, 20))
        dsLabel_type_1.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        dsLabel_type_1.setFont(font)
        dsLabel_type_1.setStyleSheet("background-color: rgb(255, 255, 255);")
        dsLabel_type_1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        dsLabel_type_1.setObjectName("dsLabel_type_1")
        if _edge.segment.getType() == 'LINE':
            dsLabel_type_1.setText("Type: Line")
        elif _edge.segment.getType() == 'POLYLINE':
            dsLabel_type_1.setText("Type: Polyline")
        elif _edge.segment.getType() == 'CUBICSPLINE':
            dsLabel_type_1.setText("Type: Cubic Spline")
        elif _edge.segment.getType() == 'CIRCLE':
            dsLabel_type_1.setText("Type: Circle")
        elif _edge.segment.getType() == 'CIRCLEARC':
            dsLabel_type_1.setText("Type: Circle Arc")
        elif _edge.segment.getType() == 'ELLIPSE':
            dsLabel_type_1.setText("Type: Ellipse")
        elif _edge.segment.getType() == 'ELLIPSEARC':
            dsLabel_type_1.setText("Type: Ellipse Arc")

        dsLabel_length = QtWidgets.QLabel(contentDS)
        dsLabel_length.setGeometry(QtCore.QRect(0, 40, 200, 20))
        dsLabel_length.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_length.setFont(font)
        dsLabel_length.setStyleSheet("")
        dsLabel_length.setObjectName("dsLabel_length")
        length = round(_edge.segment.length(0, 1), 3)
        dsLabel_length.setText(f"Length: {length}")

        dsLabel_controlpoints = QtWidgets.QLabel(contentDS)
        dsLabel_controlpoints.setGeometry(QtCore.QRect(0, 60, 200, 20))
        dsLabel_controlpoints.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_controlpoints.setFont(font)
        dsLabel_controlpoints.setStyleSheet("")
        dsLabel_controlpoints.setObjectName("dsLabel_controlpoints")
        dsLabel_controlpoints.setText("Control Points:")

        index = 80
        for pt in CtrlPts:
            LabelCtrlPt = QtWidgets.QLabel(contentDS)
            LabelCtrlPt.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            LabelCtrlPt.setGeometry(QtCore.QRect(0, index, 200, 20))
            LabelCtrlPt.setFont(font)
            pt = (round(pt[0], 3), round(pt[1], 3))
            LabelCtrlPt.setText(f"{pt}")
            index += 20

        dsLabel_knotvector = QtWidgets.QLabel(contentDS)
        dsLabel_knotvector.setGeometry(QtCore.QRect(0, index, 200, 20))
        dsLabel_knotvector.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_knotvector.setFont(font)
        dsLabel_knotvector.setStyleSheet("")
        dsLabel_knotvector.setObjectName("dsLabel_knotvector")
        dsLabel_knotvector.setText("Knot Vector:")

        index = index + 20
        for knot in KnotVector:
            LabelKnot = QtWidgets.QLabel(contentDS)
            LabelKnot.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            LabelKnot.setGeometry(QtCore.QRect(0, index, 200, 20))
            LabelKnot.setFont(font)
            knot = round(knot, 3)
            LabelKnot.setText(f"{knot}")
            index += 20

        dsLabel_degree = QtWidgets.QLabel(contentDS)
        dsLabel_degree.setGeometry(QtCore.QRect(0, index, 200, 20))
        dsLabel_degree.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_degree.setFont(font)
        dsLabel_degree.setStyleSheet("")
        dsLabel_degree.setObjectName("dsLabel_degree")
        dsLabel_degree.setText(f"Degree: {Degree}")

        index += 20
        contentDS.setMinimumSize(QtCore.QSize(200, index))

        # get attributes
        attributes = _edge.segment.attributes

        # creates Qwidget
        scrollAreaContentAtt = QtWidgets.QWidget()
        LayoutAtt = QtWidgets.QVBoxLayout(scrollAreaContentAtt)

        # set widget in scrollArea
        self.scrollAreaAtt.setWidget(scrollAreaContentAtt)

        # creates QFrame
        contentAtt = QtWidgets.QFrame(scrollAreaContentAtt)

        LayoutAtt.setContentsMargins(0, 0, 0, 0)
        LayoutAtt.setSpacing(0)
        LayoutAtt.addWidget(contentAtt)

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
            Label = QtWidgets.QLabel(contentAtt)
            Label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            Label.setGeometry(QtCore.QRect(0, index*20, 200, 20))
            Label.setFont(font)
            Label.setText(att['type'])
            properties = att['properties']

            if index % 2 == 0:
                Label.setStyleSheet("")
            else:
                Label.setStyleSheet("background-color: rgb(255, 255, 255);")
            index += 1

            nameLabel = QtWidgets.QLabel(contentAtt)
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

                propLabel = QtWidgets.QLabel(contentAtt)
                propLabel.setGeometry(QtCore.QRect(0, index*20, 200, 20))
                propLabel.setFont(font1)
                propLabel.setText(f"{key} : {value}")

                if index % 2 == 0:
                    propLabel.setStyleSheet("")
                else:
                    propLabel.setStyleSheet("background-color: rgb(255, 255, 255);")
                index += 1

        contentAtt.setMinimumSize(QtCore.QSize(200, 20*index))
