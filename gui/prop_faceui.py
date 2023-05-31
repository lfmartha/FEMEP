from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_prop_face(object):

    def setupUi(self, prop_face):
        prop_face.setObjectName("prop_face")
        prop_face.resize(200, 800)
        prop_face.setMaximumSize(QtCore.QSize(200, 16777215))

        # Tabs
        self.propertiesFrame = QtWidgets.QTabWidget(prop_face)
        self.propertiesFrame.setMinimumSize(QtCore.QSize(200, 325))
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

        # Tab Data Structure
        self.tabDS = QtWidgets.QWidget()
        self.tabDS.setObjectName("tabDS")

        self.scrollAreaDS = QtWidgets.QScrollArea(self.tabDS)
        self.scrollAreaDS.setGeometry(QtCore.QRect(0, 0, 200, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaDS.sizePolicy().hasHeightForWidth())
        self.scrollAreaDS.setSizePolicy(sizePolicy)
        self.scrollAreaDS.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollAreaDS.setLineWidth(0)
        self.scrollAreaDS.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaDS.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaDS.setWidgetResizable(True)
        self.scrollAreaDS.setObjectName("scrollAreaDS")

        self.propertiesFrame.addTab(self.tabDS, "Data Structure")

        # Tab Attributes
        self.tabAtt = QtWidgets.QWidget()
        self.tabAtt.setObjectName("tabDS")

        self.scrollAreaAtt = QtWidgets.QScrollArea(self.tabAtt)
        self.scrollAreaAtt.setGeometry(QtCore.QRect(0, 0, 200, 300))
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

        self.propertiesFrame.addTab(self.tabAtt, "Attributes")

        # Add buttons
        self.closepushbutton = QtWidgets.QPushButton(prop_face)
        self.closepushbutton.setAutoDefault(True)
        self.closepushbutton.setGeometry(QtCore.QRect(70, 390, 60, 25))
        self.closepushbutton.setObjectName("closepushbutton")

        # Add control net checkbox
        self.ctrlNetCheckBox = QtWidgets.QCheckBox(prop_face)
        self.ctrlNetCheckBox.setEnabled(True)
        self.ctrlNetCheckBox.setGeometry(QtCore.QRect(10, 377, 70, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ctrlNetCheckBox.sizePolicy().hasHeightForWidth())
        self.ctrlNetCheckBox.setSizePolicy(sizePolicy)
        self.ctrlNetCheckBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.ctrlNetCheckBox.setAcceptDrops(False)
        self.ctrlNetCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ctrlNetCheckBox.setAutoFillBackground(False)
        self.ctrlNetCheckBox.setStyleSheet("image: url(icons/ctrlnet.png);")
        self.ctrlNetCheckBox.setText("")
        self.ctrlNetCheckBox.setObjectName("ctrlNetCheckBox")
        self.retranslateUi(prop_face)

        QtCore.QMetaObject.connectSlotsByName(prop_face)

    def retranslateUi(self, prop_face):
        _translate = QtCore.QCoreApplication.translate
        self.closepushbutton.setText(_translate("MainWindow", "Close"))


class Prop_FaceDisplay(QMainWindow, Ui_prop_face):
    def __init__(self, parent=None, frame=None):
        super().__init__(parent)
        super().setupUi(self)
        self.frame = frame

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.frame is not None:
            self.resize(self.frame.size())
            dy = self.frame.height() - self.frame.minimumHeight()
            self.propertiesFrame.setMinimumSize(QtCore.QSize(200, 325 + dy))
            self.scrollAreaDS.setGeometry(QtCore.QRect(0, 0, 200, 300 + dy))
            self.scrollAreaAtt.setGeometry(QtCore.QRect(0, 0, 200, 300 + dy))
            self.closepushbutton.setGeometry(QtCore.QRect(70, 390 + dy, 60, 25))
            self.ctrlNetCheckBox.setGeometry(QtCore.QRect(10, 377 + dy, 70, 20))
        return super().resizeEvent(a0)

    def set_face_prop(self, _face):
        self.ctrlNetCheckBox.hide()

        # get nurbs surface
        nurbs = _face.patch.getNurbs()
        if nurbs != []:
            self.ctrlNetCheckBox.show()
            self.ctrlNetCheckBox.setChecked(_face.patch.CtrlNetView)
            Degree_U = nurbs.degree_u
            Degree_V = nurbs.degree_v
            CtrlNet_Size_U = nurbs.ctrlpts_size_u
            CtrlNet_Size_V = nurbs.ctrlpts_size_v
            CtrlPts = nurbs.ctrlpts
            Weights = nurbs.weights
            KnotVector_U = nurbs.knotvector_u
            KnotVector_V = nurbs.knotvector_v

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
        dsLabel_type_1.setText("Type: Surface")

        # boundary points, boundary segments, holes and area
        bp_list = _face.patch.getPoints()
        uniqueList = []
        for item in bp_list:
            if item not in uniqueList:
                uniqueList.append(item)
        bp = len(uniqueList)

        bs_list = _face.patch.getSegments()
        uniqueList = []
        for item in bs_list:
            if item not in uniqueList:
                uniqueList.append(item)
        bs = len(uniqueList)

        holes = len(_face.patch.holes)
        Area = round(_face.patch.Area(), 3)

        # Labels
        dsLabel_bp = QtWidgets.QLabel(contentDS)
        dsLabel_bp.setGeometry(QtCore.QRect(0, 40, 200, 20))
        dsLabel_bp.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_bp.setFont(font)
        dsLabel_bp.setStyleSheet("")
        dsLabel_bp.setObjectName("dsLabel_bp")
        dsLabel_bp.setText(f"Boundary points: {bp}")

        dsLabel_bs = QtWidgets.QLabel(contentDS)
        dsLabel_bs.setGeometry(QtCore.QRect(0, 60, 200, 20))
        dsLabel_bs.setMinimumSize(QtCore.QSize(200, 20))
        dsLabel_bs.setFont(font)
        dsLabel_bs.setStyleSheet("")
        dsLabel_bs.setObjectName("dsLabel_bs")
        dsLabel_bs.setText(f"Boundary segments: {bs}")

        dsLabel_holes = QtWidgets.QLabel(contentDS)
        dsLabel_holes.setGeometry(QtCore.QRect(0, 80, 200, 20))
        dsLabel_holes.setMinimumSize(QtCore.QSize(200, 20))
        dsLabel_holes.setFont(font)
        dsLabel_holes.setStyleSheet("")
        dsLabel_holes.setObjectName("dsLabel_holes")
        dsLabel_holes.setText(f"Holes: {holes}")

        dsLabel_area = QtWidgets.QLabel(contentDS)
        dsLabel_area.setGeometry(QtCore.QRect(0, 100, 200, 20))
        dsLabel_area.setMinimumSize(QtCore.QSize(200, 20))
        dsLabel_area.setFont(font)
        dsLabel_area.setStyleSheet("")
        dsLabel_area.setObjectName("dsLabel_area")
        dsLabel_area.setText(f"Area: {Area}")
        index_X = 200
        index_Y = 120

        if nurbs != []:
            dsLabel_title_nurbs = QtWidgets.QLabel(contentDS)
            dsLabel_title_nurbs.setGeometry(QtCore.QRect(0, 140, 200, 20))
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(True)
            font.setWeight(75)
            dsLabel_title_nurbs.setFont(font)
            dsLabel_title_nurbs.setAlignment(QtCore.Qt.AlignCenter)
            dsLabel_title_nurbs.setObjectName("dsLabel_title_nurbs")
            dsLabel_title_nurbs.setText("NURBS Properties")

            dsLabel_Degree_U = QtWidgets.QLabel(contentDS)
            dsLabel_Degree_U.setGeometry(QtCore.QRect(0, 160, 200, 20))
            dsLabel_Degree_U.setMinimumSize(QtCore.QSize(200, 20))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            dsLabel_Degree_U.setFont(font)
            dsLabel_Degree_U.setStyleSheet("")
            dsLabel_Degree_U.setObjectName("dsLabel_Degree_U")
            dsLabel_Degree_U.setText(f"Degree U: {Degree_U}")

            dsLabel_Degree_V = QtWidgets.QLabel(contentDS)
            dsLabel_Degree_V.setGeometry(QtCore.QRect(0, 180, 200, 20))
            dsLabel_Degree_V.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_Degree_V.setFont(font)
            dsLabel_Degree_V.setStyleSheet("")
            dsLabel_Degree_V.setObjectName("dsLabel_Degree_V")
            dsLabel_Degree_V.setText(f"Degree V: {Degree_V}")

            dsLabel_controlpoints = QtWidgets.QLabel(contentDS)
            dsLabel_controlpoints.setGeometry(QtCore.QRect(0, 220, 200, 20))
            dsLabel_controlpoints.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_controlpoints.setFont(font)
            dsLabel_controlpoints.setStyleSheet("")
            dsLabel_controlpoints.setObjectName("dsLabel_controlpoints")
            dsLabel_controlpoints.setText("Control Net:")

            count = 0
            index_X = 0
            for i in range(CtrlNet_Size_U):
                index_Y = 240
                for j in range(CtrlNet_Size_V):
                    LabelCtrlPt = QtWidgets.QLabel(contentDS)
                    LabelCtrlPt.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    LabelCtrlPt.setGeometry(QtCore.QRect(index_X, index_Y, 100, 20))
                    LabelCtrlPt.setFont(font)
                    pt = (round(CtrlPts[count][0], 3), round(CtrlPts[count][1], 3))
                    LabelCtrlPt.setText(f"{pt}")
                    count += 1
                    index_Y += 20
                index_X += 100
            index_X += 10

            index_Y += 20
            dsLabel_knotvector_U = QtWidgets.QLabel(contentDS)
            dsLabel_knotvector_U.setGeometry(QtCore.QRect(0, index_Y, 200, 20))
            dsLabel_knotvector_U.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_knotvector_U.setFont(font)
            dsLabel_knotvector_U.setStyleSheet("")
            dsLabel_knotvector_U.setObjectName("dsLabel_knotvector_U")
            dsLabel_knotvector_U.setText("Knot Vectors U and V:")

            index_Y += 20
            index_knot = int(index_Y) # copy
            for knot in KnotVector_U:
                LabelKnot = QtWidgets.QLabel(contentDS)
                LabelKnot.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                LabelKnot.setGeometry(QtCore.QRect(0, index_knot, 100, 20))
                LabelKnot.setFont(font)
                knot = round(knot, 3)
                LabelKnot.setText(f"{knot}")
                index_knot += 20

            for knot in KnotVector_V:
                LabelKnot = QtWidgets.QLabel(contentDS)
                LabelKnot.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                LabelKnot.setGeometry(QtCore.QRect(100, index_Y, 100, 20))
                LabelKnot.setFont(font)
                knot = round(knot, 3)
                LabelKnot.setText(f"{knot}")
                index_Y += 20

            index_Y += 20
            dsLabel_weights = QtWidgets.QLabel(contentDS)
            dsLabel_weights.setGeometry(QtCore.QRect(0, index_Y, 200, 20))
            dsLabel_weights.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_weights.setFont(font)
            dsLabel_weights.setStyleSheet("")
            dsLabel_weights.setObjectName("dsLabel_weights")
            dsLabel_weights.setText("Weights:")

            count = 0
            index_X = 0
            index_Y += 20
            for i in range(CtrlNet_Size_U):
                index_Y_weight = int(index_Y) # copy
                for j in range(CtrlNet_Size_V):
                    LabelWeight = QtWidgets.QLabel(contentDS)
                    LabelWeight.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    LabelWeight.setGeometry(QtCore.QRect(index_X, index_Y_weight, 100, 20))
                    LabelWeight.setFont(font)
                    w = round(Weights[count], 3)
                    LabelWeight.setText(f"{w}")
                    count += 1
                    index_Y_weight += 20
                index_X += 100
            index_X += 10
            index_Y = int(index_Y_weight) # copy

        contentDS.setMinimumSize(QtCore.QSize(index_X, index_Y))

        # get attributes
        attributes = _face.patch.attributes

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
                    propLabel.setStyleSheet(
                        "background-color: rgb(255, 255, 255);")
                index += 1

        contentAtt.setMinimumSize(QtCore.QSize(200, 20*index))
