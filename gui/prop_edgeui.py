from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_prop_edge(object):

    def setupUi(self, prop_edge):
        prop_edge.setObjectName("prop_edge")
        prop_edge.resize(200, 800)
        prop_edge.setMaximumSize(QtCore.QSize(200, 16777215))

        # Tabs
        self.propertiesFrame = QtWidgets.QTabWidget(prop_edge)
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
        self.scrollAreaDS.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
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
        self.degreeChange = QtWidgets.QPushButton(prop_edge)
        self.degreeChange.setAutoDefault(True)
        self.degreeChange.setGeometry(QtCore.QRect(45, 330, 110, 25))
        self.degreeChange.setObjectName("degreeChange")

        self.rescuepushbutton = QtWidgets.QPushButton(prop_edge)
        self.rescuepushbutton.setAutoDefault(True)
        self.rescuepushbutton.setGeometry(QtCore.QRect(155, 330, 25, 25))
        self.rescuepushbutton.setObjectName("rescuepushbutton")
        self.rescuepushbutton.setIcon(QtGui.QIcon("icons/undo-icon.png"))

        self.reversepushbutton = QtWidgets.QPushButton(prop_edge)
        self.reversepushbutton.setAutoDefault(True)
        self.reversepushbutton.setGeometry(QtCore.QRect(70, 360, 60, 25))
        self.reversepushbutton.setObjectName("swappushbutton")

        self.swappushbutton = QtWidgets.QPushButton(prop_edge)
        self.swappushbutton.setAutoDefault(True)
        self.swappushbutton.setGeometry(QtCore.QRect(70, 390, 60, 25))
        self.swappushbutton.setObjectName("swappushbutton")

        # Add control polygon checkbox
        self.ctrlPolygonCheckBox = QtWidgets.QCheckBox(prop_edge)
        self.ctrlPolygonCheckBox.setEnabled(True)
        self.ctrlPolygonCheckBox.setGeometry(QtCore.QRect(10, 377, 70, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ctrlPolygonCheckBox.sizePolicy().hasHeightForWidth())
        self.ctrlPolygonCheckBox.setSizePolicy(sizePolicy)
        self.ctrlPolygonCheckBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.ctrlPolygonCheckBox.setAcceptDrops(False)
        self.ctrlPolygonCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ctrlPolygonCheckBox.setAutoFillBackground(False)
        self.ctrlPolygonCheckBox.setStyleSheet("image: url(icons/ctrlpoly.png);")
        self.ctrlPolygonCheckBox.setText("")
        self.ctrlPolygonCheckBox.setObjectName("ctrlPolygonCheckBox")
        self.retranslateUi(prop_edge)

        QtCore.QMetaObject.connectSlotsByName(prop_edge)

    def retranslateUi(self, prop_edge):
        _translate = QtCore.QCoreApplication.translate
        self.degreeChange.setText(_translate("MainWindow", "Elevate Degree"))
        self.rescuepushbutton.setToolTip(_translate("MainWindow", "Rescue Curve"))
        self.reversepushbutton.setText(_translate("MainWindow", "Reverse"))
        self.swappushbutton.setText(_translate("MainWindow", "Swap"))


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
        self.ctrlPolygonCheckBox.setChecked(_edge.segment.CtrlPolyView)
        
        # get control points and knot vector
        nurbs = _edge.segment.getNurbs()
        Degree = nurbs.degree
        CtrlPts = nurbs.ctrlpts
        KnotVector = nurbs.knotvector
        Weights = nurbs.weights

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

        if (_edge.segment.getType() == 'LINE' or
            _edge.segment.getType() == 'POLYLINE' or
            _edge.segment.getType() == 'CUBICSPLINE'):
            dsLabel_length = QtWidgets.QLabel(contentDS)
            dsLabel_length.setGeometry(QtCore.QRect(0, 40, 200, 20))
            dsLabel_length.setMinimumSize(QtCore.QSize(200, 20))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            dsLabel_length.setFont(font)
            dsLabel_length.setStyleSheet("")
            dsLabel_length.setObjectName("dsLabel_length")
            length = round(_edge.segment.length(), 3)
            dsLabel_length.setText(f"Length: {length}")
            index = 60

        elif _edge.segment.getType() == 'CIRCLEARC':
            dsLabel_radius = QtWidgets.QLabel(contentDS)
            dsLabel_radius.setGeometry(QtCore.QRect(0, 40, 200, 20))
            dsLabel_radius.setMinimumSize(QtCore.QSize(200, 20))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            dsLabel_radius.setFont(font)
            dsLabel_radius.setStyleSheet("")
            dsLabel_radius.setObjectName("dsLabel_radius")
            radius = round(_edge.segment.curve.radius, 3)
            dsLabel_radius.setText(f"Radius: {radius}")

            dsLabel_firstangle = QtWidgets.QLabel(contentDS)
            dsLabel_firstangle.setGeometry(QtCore.QRect(0, 60, 200, 20))
            dsLabel_firstangle.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_firstangle.setFont(font)
            dsLabel_firstangle.setStyleSheet("")
            dsLabel_firstangle.setObjectName("dsLabel_firstangle")
            firstangle = round(_edge.segment.curve.ang1 * 180.0 / 3.14159, 3)
            dsLabel_firstangle.setText(f"Initial angle: {firstangle}")

            dsLabel_secondangle = QtWidgets.QLabel(contentDS)
            dsLabel_secondangle.setGeometry(QtCore.QRect(0, 80, 200, 20))
            dsLabel_secondangle.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_secondangle.setFont(font)
            dsLabel_secondangle.setStyleSheet("")
            dsLabel_secondangle.setObjectName("dsLabel_secondangle")
            secondangle = round(_edge.segment.curve.ang2 * 180.0 / 3.14159, 3)
            dsLabel_secondangle.setText(f"End angle: {secondangle}")
            index = 100

        if _edge.segment.getType() == 'ELLIPSEARC':
            dsLabel_firstaxis = QtWidgets.QLabel(contentDS)
            dsLabel_firstaxis.setGeometry(QtCore.QRect(0, 40, 200, 20))
            dsLabel_firstaxis.setMinimumSize(QtCore.QSize(200, 20))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            dsLabel_firstaxis.setFont(font)
            dsLabel_firstaxis.setStyleSheet("")
            dsLabel_firstaxis.setObjectName("dsLabel_firstaxis")
            firstaxis = round(_edge.segment.curve.axis1, 3)
            dsLabel_firstaxis.setText(f"First axis length: {firstaxis}")

            dsLabel_secondaxis = QtWidgets.QLabel(contentDS)
            dsLabel_secondaxis.setGeometry(QtCore.QRect(0, 60, 200, 20))
            dsLabel_secondaxis.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_secondaxis.setFont(font)
            dsLabel_secondaxis.setStyleSheet("")
            dsLabel_secondaxis.setObjectName("dsLabel_secondaxis")
            secondaxis = round(_edge.segment.curve.axis2, 3)
            dsLabel_secondaxis.setText(f"Second axis length: {secondaxis}")

            dsLabel_angle = QtWidgets.QLabel(contentDS)
            dsLabel_angle.setGeometry(QtCore.QRect(0, 80, 200, 20))
            dsLabel_angle.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_angle.setFont(font)
            dsLabel_angle.setStyleSheet("")
            dsLabel_angle.setObjectName("dsLabel_angle")
            angle = round(_edge.segment.curve.ang * 180.0 / 3.14159, 3)
            dsLabel_angle.setText(f"Inclination: {angle}")

            dsLabel_firstangle = QtWidgets.QLabel(contentDS)
            dsLabel_firstangle.setGeometry(QtCore.QRect(0, 100, 200, 20))
            dsLabel_firstangle.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_firstangle.setFont(font)
            dsLabel_firstangle.setStyleSheet("")
            dsLabel_firstangle.setObjectName("dsLabel_firstangle")
            firstangle = round(_edge.segment.curve.ang1 * 180.0 / 3.14159, 3)
            dsLabel_firstangle.setText(f"Initial angle: {firstangle}")

            dsLabel_secondangle = QtWidgets.QLabel(contentDS)
            dsLabel_secondangle.setGeometry(QtCore.QRect(0, 120, 200, 20))
            dsLabel_secondangle.setMinimumSize(QtCore.QSize(200, 20))
            dsLabel_secondangle.setFont(font)
            dsLabel_secondangle.setStyleSheet("")
            dsLabel_secondangle.setObjectName("dsLabel_secondangle")
            secondangle = round(_edge.segment.curve.ang2 * 180.0 / 3.14159, 3)
            dsLabel_secondangle.setText(f"End angle: {secondangle}")
            index = 140

        index += 20
        dsLabel_title_nurbs = QtWidgets.QLabel(contentDS)
        dsLabel_title_nurbs.setGeometry(QtCore.QRect(0, index, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        dsLabel_title_nurbs.setFont(font)
        dsLabel_title_nurbs.setAlignment(QtCore.Qt.AlignCenter)
        dsLabel_title_nurbs.setObjectName("dsLabel_title_nurbs")
        dsLabel_title_nurbs.setText("NURBS Properties")
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

        dsLabel_controlpoints = QtWidgets.QLabel(contentDS)
        dsLabel_controlpoints.setGeometry(QtCore.QRect(0, index, 200, 20))
        dsLabel_controlpoints.setMinimumSize(QtCore.QSize(200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        dsLabel_controlpoints.setFont(font)
        dsLabel_controlpoints.setStyleSheet("")
        dsLabel_controlpoints.setObjectName("dsLabel_controlpoints")
        dsLabel_controlpoints.setText("Control Points:")
        index += 20

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
        dsLabel_knotvector.setFont(font)
        dsLabel_knotvector.setStyleSheet("")
        dsLabel_knotvector.setObjectName("dsLabel_knotvector")
        dsLabel_knotvector.setText("Knot Vector:")
        index += 20

        for knot in KnotVector:
            LabelKnot = QtWidgets.QLabel(contentDS)
            LabelKnot.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            LabelKnot.setGeometry(QtCore.QRect(0, index, 200, 20))
            LabelKnot.setFont(font)
            knot = round(knot, 3)
            LabelKnot.setText(f"{knot}")
            index += 20

        dsLabel_weights = QtWidgets.QLabel(contentDS)
        dsLabel_weights.setGeometry(QtCore.QRect(0, index, 200, 20))
        dsLabel_weights.setMinimumSize(QtCore.QSize(200, 20))
        dsLabel_weights.setFont(font)
        dsLabel_weights.setStyleSheet("")
        dsLabel_weights.setObjectName("dsLabel_weights")
        dsLabel_weights.setText("Weights:")
        index += 20

        for w in Weights:
            LabelW = QtWidgets.QLabel(contentDS)
            LabelW.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            LabelW.setGeometry(QtCore.QRect(0, index, 200, 20))
            LabelW.setFont(font)
            w = round(w, 3)
            LabelW.setText(f"{w}")
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
