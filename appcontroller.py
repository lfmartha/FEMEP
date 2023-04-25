import ctypes
from he.heview import HeView
from PyQt5.QtWidgets import *
from glcanvas import Canvas, Point
from he.hemodel import HeModel
from he.hecontroller import HeController
from PyQt5 import QtCore, QtGui
from gui.femepui import Ui_MainWindow
from gui.gridui import GridDisplay
from gui.lineui import LineDisplay
from gui.polylineui import PolylineDisplay
from gui.cubicsplineui import CubicSplineDisplay
from gui.circleui import CircleDisplay
from gui.circlearcui import CircleArcDisplay
from gui.ellipseui import EllipseDisplay
from gui.ellipsearcui import EllipseArcDisplay
from gui.selectui import SelectDisplay
from gui.pointui import PointDisplay
from gui.attributeui import AttributeDisplay
from gui.prop_vertexui import Prop_VertexDisplay
from gui.prop_edgeui import Prop_EdgeDisplay
from gui.prop_faceui import Prop_FaceDisplay
from gui.colorselectui import ColorSelectDisplay
from gui.exportfileui import ExportFileDisplay
from gui.meshui import MeshDisplay
from gui.nsudvui import NsudvDisplay
from mesh.mesh import MeshGeneration


class AppController(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.setMouseTracking(True)

        # set window icon
        self.setWindowIcon(QtGui.QIcon("icons/femepwindow-icon.png"))
        AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            AppUserModelID)

        # setup half-edge data structures
        self.tab_list = []  # list of tabs
        self.canvas_list = []  # list of canvas
        self.hecontrollers_list = []  # list of handles to hecontroller
        self.attpropertiesItems = []  # handle to items of attributes values
        self.num_tab = 0  # number of tabs created
        self.view_grid_display = False  # flag to turn on GridDisplayer
        self.current_canvas = None
        self.current_hecontroller = None

        # setup dynamic displayers
        self.grid_display = GridDisplay()
        self.line_display = LineDisplay()
        self.polyline_display = PolylineDisplay()
        self.cubicspline_display = CubicSplineDisplay()
        self.circle_display = CircleDisplay()
        self.circlearc_display = CircleArcDisplay()
        self.ellipse_display = EllipseDisplay()
        self.ellipsearc_display = EllipseArcDisplay()
        self.select_display = SelectDisplay()
        self.point_display = PointDisplay()
        self.attribute_display = AttributeDisplay(frame=self.leftToolbarFrame)
        self.prop_vertex_display = Prop_VertexDisplay(
            frame=self.leftToolbarFrame)
        self.prop_edge_display = Prop_EdgeDisplay(frame=self.leftToolbarFrame)
        self.prop_face_display = Prop_FaceDisplay(frame=self.leftToolbarFrame)
        self.colorSelect_display = ColorSelectDisplay(self)
        self.nsudv_display = NsudvDisplay()
        self.mesh_display = MeshDisplay()
        self.exportFile_display = ExportFileDisplay()

        MeshGeneration.App = self  # pass handle for msg box

        # create a tab and canvas
        self.on_actionAdd_tab()

        # Set default button checked status and display
        self.actionSelect.setChecked(True)
        self.select_display.setParent(self.leftToolbarFrame)
        self.select_display.show()

        # set default mouse action on canvas
        self.canvas_list[0].setMouseAction('SELECTION')

        # tab buttons
        self.tabWidget.tabCloseRequested.connect(self.closetab)
        self.tabWidget.tabBarClicked.connect(self.tabBarClicked)

        # QActions Toolbar
        self.actionPoint.triggered.connect(self.on_actionPoint)
        self.actionLine.triggered.connect(self.on_actionLine)
        self.actionPolyline.triggered.connect(self.on_actionPolyline)
        self.actionCubicSpline.triggered.connect(self.on_actionCubicSpline)
        self.actionCircle.triggered.connect(self.on_actionCircle)
        self.actionCircleArc.triggered.connect(self.on_actionCircleArc)
        self.actionEllipse.triggered.connect(self.on_actionEllipse)
        self.actionEllipseArc.triggered.connect(self.on_actionEllipseArc)
        self.actionSelect.triggered.connect(self.on_actionSelect)
        self.actionDelete.triggered.connect(self.delSelectedEntities)
        self.actionFit.triggered.connect(self.fitWorldToViewport)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPanRight.triggered.connect(self.PanRight)
        self.actionPanLeft.triggered.connect(self.PanLeft)
        self.actionPanUp.triggered.connect(self.PanUp)
        self.actionPanDown.triggered.connect(self.PanDown)
        self.actionGrid.triggered.connect(self.on_actionGrid)
        self.actionCreatePatch.triggered.connect(self.createPatch)
        self.actionUndo.triggered.connect(self.Undo)
        self.actionRedo.triggered.connect(self.Redo)
        self.actionNew.triggered.connect(self.on_actionAdd_tab)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSaveAs.triggered.connect(self.saveAsFile)
        self.actionExport.triggered.connect(self.exportFile_disp)
        self.actionExit.triggered.connect(self.exit)
        self.actionAttmanager.triggered.connect(self.AttributeManager)
        self.actionNsudv.triggered.connect(self.on_action_nsudv)
        self.actionMesh.triggered.connect(self.on_action_Mesh)

        # ---------------------------------------------------------------------
        # QPushButtons
        # Grid QPushButton
        self.grid_display.gridOKpushButton.clicked.connect(self.setgrid)

        # Point QPushButton
        self.point_display.addPointpushButton.clicked.connect(self.add_point)

        # Line QPushButton
        self.line_display.InitialPointpushButton.clicked.connect(self.add_lineInitialPoint)
        self.line_display.addLinepushButton.clicked.connect(self.add_line)

        # Polyline QPushButton
        self.polyline_display.InitialPointpushButton.clicked.connect(self.add_polylineInitialPoint)
        self.polyline_display.addPolylinepushButton.clicked.connect(self.add_polylineEndPoint)
        self.polyline_display.endPolylinepushButton.clicked.connect(self.end_polyline)

        # Cubic Spline QPushButton
        self.cubicspline_display.InitialPointpushButton.clicked.connect(self.add_cubicsplineInitialPoint)
        self.cubicspline_display.addCubicSplinepushButton.clicked.connect(self.add_cubicsplineEndPoint)
        self.cubicspline_display.endCubicSplinepushButton.clicked.connect(self.end_cubicspline)

        # Circle QPushButton
        self.circle_display.setCenterpushButton.clicked.connect(self.set_circleCenter)
        self.circle_display.addCirclepushButton.clicked.connect(self.add_circle)

        # Circle Arc QPushButton
        self.circlearc_display.setCenterpushButton.clicked.connect(self.set_circlearcCenter)
        self.circlearc_display.setFirstArcPointpushButton.clicked.connect(self.set_circlearcFirstArcPoint)
        self.circlearc_display.addCircleArcpushButton.clicked.connect(self.add_circlearc)

        # Ellipse QPushButton
        self.ellipse_display.setCenterpushButton.clicked.connect(self.set_ellipseCenter)
        self.ellipse_display.setFirstAxispushButton.clicked.connect(self.set_ellipseFirstAxis)
        self.ellipse_display.addEllipsepushButton.clicked.connect(self.add_ellipse)

        # Ellipse Arc QPushButton
        self.ellipsearc_display.setCenterpushButton.clicked.connect(self.set_ellipsearcCenter)
        self.ellipsearc_display.setFirstAxispushButton.clicked.connect(self.set_ellipsearcFirstAxis)
        self.ellipsearc_display.setSecondAxispushButton.clicked.connect(self.set_ellipsearcSecondAxis)
        self.ellipsearc_display.setFirstArcPointpushButton.clicked.connect(self.set_ellipsearcFirstArcPoint)
        self.ellipsearc_display.addEllipseArcpushButton.clicked.connect(self.add_ellipsearc)

        # Select QPushButton
        self.select_display.propertiespushButton.clicked.connect(self.properties)

        # Prop vertex QPushButton
        self.prop_vertex_display.closepushbutton.clicked.connect(self.close_propVertex)

        # Prop edge QPushButton
        self.prop_edge_display.degreeChange.clicked.connect(self.degreeChange)
        self.prop_edge_display.rescuepushbutton.clicked.connect(self.BackToOriginalNurbs)
        self.prop_edge_display.reversepushbutton.clicked.connect(self.ReverseNurbs)
        self.prop_edge_display.swappushbutton.clicked.connect(self.close_propEdge)

        # Prop face QPushButton
        self.prop_face_display.closepushbutton.clicked.connect(self.close_propFace)

        # Subdivisions QPushButton
        self.nsudv_display.nsudvpushButton.clicked.connect(self.setNumberSdv)
        self.nsudv_display.knotrefinementpushButton.clicked.connect(self.refineNumberSdv)
        self.nsudv_display.rescuepushButton.clicked.connect(self.BackToOriginalNurbsRefine)
        self.nsudv_display.knotconformpushButton.clicked.connect(self.conformSegs)

        # Mesh QPushButton
        self.mesh_display.genMeshpushButton.clicked.connect(self.generateMesh)
        self.mesh_display.delMeshpushButton.clicked.connect(self.delMesh)
        self.mesh_display.surfUCurvespushButton.clicked.connect(self.setUCurves)
        self.mesh_display.surfVCurvespushButton.clicked.connect(self.setVCurves)

        # Attributes QPushButton
        self.attribute_display.addpushButton.clicked.connect(self.addAttribute)
        self.attribute_display.saveAttpushButton.clicked.connect(self.saveAttributeValues)
        self.attribute_display.delpushButton.clicked.connect(self.delAttribute)
        self.attribute_display.setAttpushButton.clicked.connect(self.setAttribute)
        self.attribute_display.unsetpushButton.clicked.connect(self.unSetAttribute)
        self.attribute_display.renamepushButton.clicked.connect(self.renameAttribute)

        # Export QPushButton
        self.exportFile_display.exportpushButton.clicked.connect(self.exportFile)

        # ---------------------------------------------------------------------
        # QCheckBoxes
        # Snap QCheckBox
        self.snapcheckBox.clicked.connect(self.change_snapgrid)

        # Select QCheckBox
        self.select_display.pointcheckBox.clicked.connect(self.change_select)
        self.select_display.segmentcheckBox.clicked.connect(self.change_select)
        self.select_display.patchcheckBox.clicked.connect(self.change_select)

        # Prop edge Checkbox
        self.prop_edge_display.ctrlPolygonCheckBox.clicked.connect(self.updateCtrlPolyView)

        # ---------------------------------------------------------------------
        # QComboBoxes
        # Circle QComboBox
        self.circle_display.RadiuscomboBox.activated.connect(self.setCircleRadiusOptions)

        # Circle Arc QComboBox
        self.circlearc_display.FirstArcPointcomboBox.activated.connect(self.setCircleArcFirstArcPointOptions)
        self.circlearc_display.SecondArcPointcomboBox.activated.connect(self.setCircleArcSecondArcPointOptions)
        
        # Ellipse QComboBox
        self.ellipse_display.FirstAxiscomboBox.activated.connect(self.setEllipseFirstAxisOptions)
        self.ellipse_display.SecondAxiscomboBox.activated.connect(self.setEllipseSecondAxisOptions)

        # Ellipse Arc QComboBox
        self.ellipsearc_display.FirstAxiscomboBox.activated.connect(self.setEllipseArcFirstAxisOptions)
        self.ellipsearc_display.SecondAxiscomboBox.activated.connect(self.setEllipseArcSecondAxisOptions)
        self.ellipsearc_display.FirstArcPointcomboBox.activated.connect(self.setEllipseArcFirstArcPointOptions)
        self.ellipsearc_display.SecondArcPointcomboBox.activated.connect(self.setEllipseArcSecondArcPointOptions)

        # Subdivisions QComboBox
        self.nsudv_display.nsudvcomboBox.activated.connect(self.setNumSubdivisionsOptions)

        # Attribute QComboBox
        self.attribute_display.attcomboBox.activated.connect(self.setAttPropertiesDisplay)

        # Mesh QComboBox
        self.mesh_display.meshcomboBox.activated.connect(self.setMeshOptions)
        self.mesh_display.shapecomboBox.activated.connect(self.setDiagOptions)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.attribute_display.resizeEvent(a0)
        self.prop_edge_display.resizeEvent(a0)
        self.prop_face_display.resizeEvent(a0)
        self.prop_vertex_display.resizeEvent(a0)
        return super().resizeEvent(a0)

    def on_actionAdd_tab(self):
        new_tab = QWidget()
        self.tab_list.append(new_tab)
        self.num_tab += 1
        new_tab.setObjectName(f"untitled_{self.num_tab}")
        self.tabWidget.addTab(new_tab, f"untitled_{self.num_tab}")

        horizontalLayout = QVBoxLayout(new_tab)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(0)
        horizontalLayout.setObjectName(f"canvas_Layout_{self.num_tab}")

        # setup half-edge data structures
        model = HeModel()
        hecontroller = HeController(model)
        self.hecontrollers_list.append(hecontroller)

        # setup the canvas
        canvas = Canvas(self, hecontroller)
        self.canvas_list.append(canvas)
        canvas.setParent(new_tab)
        horizontalLayout.addWidget(canvas)

        # passes the view to the canvas
        view = HeView(model)
        canvas.setView(view)

        # change canvas cursor
        canvas.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Get mouse move events even when no buttons are held down
        canvas.setMouseTracking(True)

        # Set the canvas input focus
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)

        # adjust the snap to grid
        if self.snapcheckBox.isChecked():
            canvas.grid.isSnapOn = True

        # adjust select options
        if not self.select_display.pointcheckBox.isChecked():
            hecontroller.select_point = False
        if not self.select_display.segmentcheckBox.isChecked():
            hecontroller.select_segment = False
        if not self.select_display.patchcheckBox.isChecked():
            hecontroller.select_patch = False

        # set the current mouse action on canvas
        if self.actionSelect.isChecked():
            canvas.setMouseAction('SELECTION')
        elif self.actionLine.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('LINE')
        elif self.actionPolyline.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('POLYLINE')
        elif self.actionCubicSpline.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CUBICSPLINE')
        elif self.actionCircle.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CIRCLE')
        elif self.actionCircleArc.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CIRCLEARC')
        elif self.actionEllipse.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('ELLIPSE')
        elif self.actionEllipseArc.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('ELLIPSEARC')
        elif self.actionPoint.isChecked():
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('POINT')

        if len(self.tab_list) == 1:
            self.current_canvas = self.canvas_list[0]
            self.current_hecontroller = self.hecontrollers_list[0]

        if len(self.tab_list) > 0:
            self.tabWidget.setStyleSheet("")
            # set new tab as the current tab
            self.tabBarClicked(len(self.tab_list)-1)

    def tabBarClicked(self, _index):

        # setup interface
        self.current_canvas.collector.endGeoCollection()
        self.clearDispText(self.line_display)
        self.clearDispText(self.polyline_display)
        self.clearDispText(self.cubicspline_display)
        self.clearDispText(self.circle_display)
        self.clearDispText(self.circlearc_display)
        self.clearDispText(self.ellipse_display)
        self.clearDispText(self.ellipsearc_display)

        self.tabWidget.setCurrentIndex(_index)
        tab = self.tabWidget.currentWidget()
        currentIndex = self.getTabIndex(tab)
        self.current_canvas = self.canvas_list[currentIndex]
        self.current_hecontroller = self.hecontrollers_list[currentIndex]

        if self.actionAttmanager.isChecked():
            self.AttributeManager()

        if self.actionSelect.isChecked():
            if self.current_canvas.prop_disp:
                self.properties()
            else:
                self.closeAllDisplayers()
                self.select_display.show()

        self.update()

    def closetab(self, _index):
        for tab in self.tab_list:
            if self.tabWidget.indexOf(tab) == _index:
                currentIndex = self.getTabIndex(tab)
                break

        hecontroller = self.hecontrollers_list[currentIndex]
        if (hecontroller.isChanged and not hecontroller.hemodel.isEmpty()):
            filename = self.tabWidget.tabText(currentIndex)
            qm = QMessageBox
            ans = qm.question(
                self, 'Warning', f"Save current {filename} changes?", qm.Yes | qm.No | qm.Cancel)

            if ans == qm.Yes:
                self.saveFile()
            elif ans == qm.Cancel:
                return False

        # setup interface
        if self.current_canvas == self.canvas_list[currentIndex]:
            self.clearDispText(self.line_display)
            self.clearDispText(self.polyline_display)
            self.clearDispText(self.cubicspline_display)
            self.clearDispText(self.circle_display)
            self.clearDispText(self.circlearc_display)
            self.clearDispText(self.ellipse_display)
            self.clearDispText(self.ellipsearc_display)

        self.tabWidget.removeTab(_index)
        self.canvas_list.pop(currentIndex)
        self.hecontrollers_list.pop(currentIndex)
        self.tab_list.pop(currentIndex)

        if len(self.tab_list) > 0:
            tab = self.tabWidget.currentWidget()
            currentIndex = self.getTabIndex(tab)
            self.current_canvas = self.canvas_list[currentIndex]
            self.current_hecontroller = self.hecontrollers_list[currentIndex]

            if self.actionSelect.isChecked():
                if self.current_canvas.prop_disp:
                    self.properties()
                else:
                    self.closeAllDisplayers()
                    self.select_display.show()
            elif self.actionAttmanager.isChecked():
                self.AttributeManager()

        if len(self.tab_list) == 0:
            self.tabWidget.setStyleSheet(
                "image: url(icons/new-file-bg.png);")
            self.on_actionSelect()

        self.update()

        return True

    def getTabIndex(self, _tab):
        for i in range(0, len(self.tab_list)):
            if _tab == self.tab_list[i]:
                return i

    def on_actionSelect(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionSelect.setChecked(True)

        # close displayers
        self.closeAllDisplayers()
        self.select_display.setParent(self.leftToolbarFrame)
        self.select_display.show()

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('SELECTION')

    def on_actionPoint(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionPoint.setChecked(True)

        # Turn on Line display
        self.closeAllDisplayers()
        self.point_display.setParent(self.leftToolbarFrame)
        self.point_display.show()

        # clear txts
        self.clearDispText(self.point_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('POINT')

    def on_actionLine(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionLine.setChecked(True)

        # Turn on Line display
        self.closeAllDisplayers()
        self.line_display.setParent(self.leftToolbarFrame)
        self.line_display.show()

        # clear txts
        self.clearDispText(self.line_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('LINE')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionPolyline(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionPolyline.setChecked(True)

        # Turn on Polyline display
        self.closeAllDisplayers()
        self.polyline_display.setParent(self.leftToolbarFrame)
        self.polyline_display.show()

        # clear txts
        self.clearDispText(self.polyline_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('POLYLINE')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionCubicSpline(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionCubicSpline.setChecked(True)

        # Turn on CubicSpline display
        self.closeAllDisplayers()
        self.cubicspline_display.setParent(self.leftToolbarFrame)
        self.cubicspline_display.show()

        # clear txts
        self.clearDispText(self.cubicspline_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CUBICSPLINE')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionCircle(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionCircle.setChecked(True)

        # Turn on Circle display
        self.closeAllDisplayers()
        self.circle_display.setParent(self.leftToolbarFrame)
        self.circle_display.show()

        # clear txts
        self.clearDispText(self.circle_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CIRCLE')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionCircleArc(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionCircleArc.setChecked(True)

        # Turn on CircleArc display
        self.closeAllDisplayers()
        self.circlearc_display.setParent(self.leftToolbarFrame)
        self.circlearc_display.show()

        # clear txts
        self.clearDispText(self.circlearc_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('CIRCLEARC')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionEllipse(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionEllipse.setChecked(True)

        # Turn on Ellipse display
        self.closeAllDisplayers()
        self.ellipse_display.setParent(self.leftToolbarFrame)
        self.ellipse_display.show()

        # clear txts
        self.clearDispText(self.ellipse_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('ELLIPSE')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionEllipseArc(self):

        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionEllipseArc.setChecked(True)

        # Turn on EllipseArc display
        self.closeAllDisplayers()
        self.ellipsearc_display.setParent(self.leftToolbarFrame)
        self.ellipsearc_display.show()

        # clear txts
        self.clearDispText(self.ellipsearc_display)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('COLLECTION')
            canvas.setGeoType('ELLIPSEARC')

        # set LineEdits
        self.set_curves_lineEdits()

    def on_actionGrid(self):

        if len(self.canvas_list) == 0:
            return

        # turn off view grid
        if self.current_canvas.viewGrid:
            self.current_canvas.viewGrid = False
            self.current_canvas.update()
            return

        # verifies if the grid button is turned on or off
        if not self.view_grid_display:
            # Turn on grid display
            self.closeAllDisplayers()
            self.grid_display.setParent(self.leftToolbarFrame)
            self.grid_display.show()
            self.view_grid_display = True

            # get data from grid/snap and set in the dialog
            dX = 0
            dY = 0
            _, dX, dY = self.current_canvas.getGridSnapInfo(
                dX, dY)
            self.grid_display.gridXlineEdit.setText(str(dX))
            self.grid_display.gridYlineEdit.setText(str(dY))
        else:
            self.grid_display.close()
            self.view_grid_display = False

            # check if there is other display on
            self.showCurrentdisplay()

    def setgrid(self):

        # get data from grid/snap and set in the dialog
        dX, dY = self.current_canvas.grid.getGridSpace()
        isSnapOn, dX, dY = self.current_canvas.getGridSnapInfo(
            dX, dY)

        # get inputs data
        try:
            dX = float(self.grid_display.gridXlineEdit.text())
            dY = float(self.grid_display.gridYlineEdit.text())
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            self.grid_display.gridXlineEdit.setText(str(dX))
            self.grid_display.gridYlineEdit.setText(str(dY))
            return

        if dX <= 0 or dY <= 0:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These numbers is not acceptable')
            msg.exec()
            self.grid_display.gridXlineEdit.setText('')
            self.grid_display.gridYlineEdit.setText('')
            return

        # opens dialog and get properties from grid and snap
        self.current_canvas.setGridSnapData(True, isSnapOn, dX, dY)
        self.current_canvas.viewGrid = True

        # turn off grid display
        self.grid_display.close()
        self.view_grid_display = False

        # check if there is other display on
        self.showCurrentdisplay()

    def change_select(self):

        if self.select_display.pointcheckBox.isChecked():
            for canvas in self.canvas_list:
                canvas.hecontroller.select_point = True
        else:
            for canvas in self.canvas_list:
                canvas.hecontroller.select_point = False

        if self.select_display.segmentcheckBox.isChecked():
            for canvas in self.canvas_list:
                canvas.hecontroller.select_segment = True
        else:
            for canvas in self.canvas_list:
                canvas.hecontroller.select_segment = False

        if self.select_display.patchcheckBox.isChecked():
            for canvas in self.canvas_list:
                canvas.hecontroller.select_patch = True
        else:
            for canvas in self.canvas_list:
                canvas.hecontroller.select_patch = False

    def change_snapgrid(self):

        if self.snapcheckBox.isChecked():
            for canvas in self.canvas_list:
                canvas.grid.isSnapOn = True
        else:
            for canvas in self.canvas_list:
                canvas.grid.isSnapOn = False

    def add_point(self):
        if len(self.canvas_list) == 0:
            return
        
        # get current canvas
        canvas = self.current_canvas

        # get point from lineEdits
        try:
            x = float(self.point_display.PointXlineEdit.text())
            y = float(self.point_display.PointYlineEdit.text())
        except:
            self.clearDispText(self.point_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        self.current_canvas.hecontroller.insertPoint(Point(x, y), pick_tol)
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

        # clear txts
        self.clearDispText(self.point_display)

    # Line pushButton methods
    def add_lineInitialPoint(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Line initial point lineEdits
        try:
            x = float(self.line_display.InitialPointXlineEdit.text())
            y = float(self.line_display.InitialPointYlineEdit.text())
        except:
            self.clearDispText(self.line_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the initial point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def add_line(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get point from Line end point lineEdits
        try:
            x = float(self.line_display.EndPointXlineEdit.text())
            y = float(self.line_display.EndPointYlineEdit.text())
        except:
            self.clearDispText(self.line_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set the end point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, False, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Polyline pushButton methods
    def add_polylineInitialPoint(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Polyline initial point lineEdits
        try:
            x = float(self.polyline_display.InitialPointXlineEdit.text())
            y = float(self.polyline_display.InitialPointYlineEdit.text())
        except:
            self.clearDispText(self.polyline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the initial point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def add_polylineEndPoint(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Polyline end point lineEdits
        try:
            x = float(self.polyline_display.EndPointXlineEdit.text())
            y = float(self.polyline_display.EndPointYlineEdit.text())
        except:
            self.clearDispText(self.polyline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set the end point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, False, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def end_polyline(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get point from Polyline end point lineEdits
        try:
            x = float(self.polyline_display.EndPointXlineEdit.text())
            y = float(self.polyline_display.EndPointYlineEdit.text())
        except:
            self.clearDispText(self.polyline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set the end point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, False, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Cubicspline pushButton methods
    def add_cubicsplineInitialPoint(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Cubic Spline initial point lineEdits
        try:
            x = float(self.cubicspline_display.InitialPointXlineEdit.text())
            y = float(self.cubicspline_display.InitialPointYlineEdit.text())
        except:
            self.clearDispText(self.cubicspline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the initial point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def add_cubicsplineEndPoint(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Cubic Spline end point lineEdits
        try:
            x = float(self.cubicspline_display.EndPointXlineEdit.text())
            y = float(self.cubicspline_display.EndPointYlineEdit.text())
        except:
            self.clearDispText(self.cubicspline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set the end point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, False, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def end_cubicspline(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get point from Cubic Spline end point lineEdits
        try:
            x = float(self.cubicspline_display.EndPointXlineEdit.text())
            y = float(self.cubicspline_display.EndPointYlineEdit.text())
        except:
            self.clearDispText(self.cubicspline_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # set the end point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, False, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Circle pushButton methods
    def set_circleCenter(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Circle center lineEdits
        try:
            x = float(self.circle_display.CenterXlineEdit.text())
            y = float(self.circle_display.CenterYlineEdit.text())
        except:
            self.clearDispText(self.circle_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the center point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def add_circle(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Circle radius lineEdits
        try:
            x = float(self.circle_display.RadiusXlineEdit.text())
            y = float(self.circle_display.RadiusYlineEdit.text())
        except:
            self.clearDispText(self.circle_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check comboBox
        Radius_option = self.circle_display.RadiuscomboBox.currentText()
        if Radius_option == "Coordinates":
            LenAndAng = False
        elif Radius_option == "Radius and Angle":
            LenAndAng = True

        # set the radius
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Circle Arc pushButton methods
    def set_circlearcCenter(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Circle Arc center lineEdits
        try:
            x = float(self.circlearc_display.CenterXlineEdit.text())
            y = float(self.circlearc_display.CenterYlineEdit.text())
        except:
            self.clearDispText(self.circlearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the center point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def set_circlearcFirstArcPoint(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Circle Arc first arc point lineEdits
        try:
            x = float(self.circlearc_display.FirstArcPointXlineEdit.text())
            y = float(self.circlearc_display.FirstArcPointYlineEdit.text())
        except:
            self.clearDispText(self.circlearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

       # check comboBox
        FirstArcPoint_option = self.circlearc_display.FirstArcPointcomboBox.currentText()
        if FirstArcPoint_option == "Coordinates":
            LenAndAng = False
        elif FirstArcPoint_option == "Radius and Angle":
            LenAndAng = True

        # set the first arc point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

       # check comboBox and set LineEdits text
        SecondArcPoint_option = self.circlearc_display.SecondArcPointcomboBox.currentText()
        if SecondArcPoint_option == "Coordinates":
            pass
        elif SecondArcPoint_option == "Radius and Angle":
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.circlearc_display.SecondArcPointYlineEdit.clear()

    def add_circlearc(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Circle Arc second arc point lineEdits
        try:
            x = float(self.circlearc_display.SecondArcPointXlineEdit.text())
            y = float(self.circlearc_display.SecondArcPointYlineEdit.text())
        except:
            self.clearDispText(self.circlearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check comboBox
        Radius_option = self.circlearc_display.SecondArcPointcomboBox.currentText()
        if Radius_option == "Coordinates":
            LenAndAng = False
        elif Radius_option == "Radius and Angle":
            LenAndAng = True

        # set the radius
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Ellipse pushButton methods
    def set_ellipseCenter(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Ellipse center lineEdits
        try:
            x = float(self.ellipse_display.CenterXlineEdit.text())
            y = float(self.ellipse_display.CenterYlineEdit.text())
        except:
            self.clearDispText(self.ellipse_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the center point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def set_ellipseFirstAxis(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse first axis lineEdits
        try:
            x = float(self.ellipse_display.FirstAxisXlineEdit.text())
            y = float(self.ellipse_display.FirstAxisYlineEdit.text())
        except:
            self.clearDispText(self.ellipse_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

       # check comboBox
        FirstAxis_option = self.ellipse_display.FirstAxiscomboBox.currentText()
        if FirstAxis_option == "Coordinates":
            LenAndAng = False
        elif FirstAxis_option == "Length and Angle":
            LenAndAng = True

        # set the first axis
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

       # check comboBox and set LineEdits text
        SecondAxis_option = self.ellipse_display.SecondAxiscomboBox.currentText()
        if SecondAxis_option == "Coordinates":
            pass
        elif SecondAxis_option == "Length and Angle":
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.ellipse_display.SecondAxisXlineEdit.clear()

    def add_ellipse(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse second axis lineEdits
        try:
            x = float(self.ellipse_display.SecondAxisXlineEdit.text())
            y = float(self.ellipse_display.SecondAxisYlineEdit.text())
        except:
            self.clearDispText(self.ellipse_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check comboBox
        SecondAxis_option = self.ellipse_display.SecondAxiscomboBox.currentText()
        if SecondAxis_option == "Coordinates":
            LenAndAng = False
        elif SecondAxis_option == "Length and Angle":
            LenAndAng = True

        # set the second axis
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    # Ellipse Arc pushButton methods
    def set_ellipsearcCenter(self):
        if len(self.canvas_list) == 0:
             return

        # get current canvas
        canvas = self.current_canvas

        # get point from Ellipse Arc center lineEdits
        try:
            x = float(self.ellipsearc_display.CenterXlineEdit.text())
            y = float(self.ellipsearc_display.CenterYlineEdit.text())
        except:
            self.clearDispText(self.ellipsearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # start collection and set the center point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x, y, False, pick_tol)
        
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def set_ellipsearcFirstAxis(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse Arc first axis lineEdits
        try:
            x = float(self.ellipsearc_display.FirstAxisXlineEdit.text())
            y = float(self.ellipsearc_display.FirstAxisYlineEdit.text())
        except:
            self.clearDispText(self.ellipsearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

       # check comboBox
        FirstAxis_option = self.ellipsearc_display.FirstAxiscomboBox.currentText()
        if FirstAxis_option == "Coordinates":
            LenAndAng = False
        elif FirstAxis_option == "Length and Angle":
            LenAndAng = True

        # set the first axis
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

        # check comboBox and set lineEdits
        SecondAxis_option = self.ellipsearc_display.SecondAxiscomboBox.currentText()
        if SecondAxis_option == "Coordinates":
            pass
        elif SecondAxis_option == "Length and Angle":
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.ellipsearc_display.SecondAxisXlineEdit.clear()

    def set_ellipsearcSecondAxis(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse Arc second axis lineEdits
        try:
            x = float(self.ellipsearc_display.SecondAxisXlineEdit.text())
            y = float(self.ellipsearc_display.SecondAxisYlineEdit.text())
        except:
            self.clearDispText(self.ellipsearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

       # check comboBox
        SecondAxis_option = self.ellipsearc_display.SecondAxiscomboBox.currentText()
        if SecondAxis_option == "Coordinates":
            LenAndAng = False
        elif SecondAxis_option == "Length and Angle":
            LenAndAng = True

        # set the second axis
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def set_ellipsearcFirstArcPoint(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse Arc first point lineEdits
        try:
            y = float(self.ellipsearc_display.FirstArcPointYlineEdit.text())
        except:
            self.clearDispText(self.ellipsearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return
        
       # check comboBox
        FirstArcPoint_option = self.ellipsearc_display.FirstArcPointcomboBox.currentText()
        if FirstArcPoint_option == "Coordinates":
            LenAndAng = False
        elif FirstArcPoint_option == "Length and Angle":
            LenAndAng = True

        try:
            x = float(self.ellipsearc_display.FirstArcPointXlineEdit.text())
        except:
            if LenAndAng:
                # set LineEdit
                x = canvas.collector.geo.LenCenterToPt(y)
                self.ellipsearc_display.FirstArcPointXlineEdit.setText(str(round(x, 3)))
            else:
                self.clearDispText(self.ellipsearc_display)
                msg = QMessageBox(self)
                msg.setWindowTitle('Warning')
                msg.setText('These data fields only accept numbers')
                msg.exec()
                return
            
        # set the first arc point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        canvas.updatedDsp = False
        canvas.update()

        # # set LineEdits
        self.set_curves_lineEdits()

    def add_ellipsearc(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # get values from Ellipse Arc second point lineEdits
        try:
            y = float(self.ellipsearc_display.SecondArcPointYlineEdit.text())
        except:
            self.clearDispText(self.ellipsearc_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check comboBox
        SecondArcPoint_option = self.ellipsearc_display.SecondArcPointcomboBox.currentText()
        if SecondArcPoint_option == "Coordinates":
            LenAndAng = False
        elif SecondArcPoint_option == "Length and Angle":
            LenAndAng = True

        try:
            x = float(self.ellipsearc_display.SecondArcPointXlineEdit.text())
        except:
            if LenAndAng:
                # set LineEdit
                x = canvas.collector.geo.LenCenterToPt(y)
            else:
                self.clearDispText(self.ellipsearc_display)
                msg = QMessageBox(self)
                msg.setWindowTitle('Warning')
                msg.setText('These data fields only accept numbers')
                msg.exec()
                return

        # set the second arc point
        max_size = max(abs(canvas.right-canvas.left),
                        abs(canvas.top-canvas.bottom))
        pick_tol = max_size * canvas.pickTolFac
        canvas.collector.insertPoint(x, y, LenAndAng, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, pick_tol)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # set LineEdits
        self.set_curves_lineEdits()

    def delSelectedEntities(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.delSelectedEntities()

    def fitWorldToViewport(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.fitWorldToViewport()

    def zoomIn(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.zoomIn()

    def zoomOut(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.zoomOut()

    def PanRight(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.PanRight()

    def PanLeft(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.PanLeft()

    def PanUp(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.PanUp()

    def PanDown(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.PanDown()

    def createPatch(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.createPatch()

    def Undo(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.Undo()

        if self.actionSelect.isChecked():
            self.properties()
            self.update()

    def Redo(self):
        if len(self.canvas_list) == 0:
            return

        self.current_canvas.Redo()

        if self.actionSelect.isChecked():
            self.properties()
            self.update()

    def saveFile(self):
        if len(self.canvas_list) == 0:
            return

        if self.current_hecontroller.hemodel.isEmpty():
            return

        file = self.current_hecontroller.file

        if file is None:
            filename, _ = QFileDialog.getSaveFileName(
                self.centralwidget, 'Save File')
        else:
            filename = file

        if filename == '':
            return

        split_name = filename.split('/')
        split_name = split_name[-1].split('.')
        tr = QtCore.QCoreApplication.translate
        tab = self.tabWidget.currentWidget()
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(tab), tr("MainWindow", f"{split_name[0]}"))
        self.current_canvas.saveFile(filename)

    def saveAsFile(self):

        if len(self.canvas_list) == 0:
            return

        if self.current_hecontroller.hemodel.isEmpty():
            return

        filename, _ = QFileDialog.getSaveFileName(
            self.centralwidget, 'Save File')

        if filename == '':
            return

        split_name = filename.split('/')
        split_name = split_name[-1].split('.')

        tr = QtCore.QCoreApplication.translate
        tab = self.tabWidget.currentWidget()
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(tab), tr("MainWindow", f"{split_name[0]}"))
        self.current_canvas.saveFile(filename)

    def openFile(self):
        if len(self.canvas_list) == 0:
            return

        filename, _ = QFileDialog.getOpenFileName(
            self.centralwidget, 'Open File')

        if filename == '':
            return

        # try:
        self.current_canvas.openFile(filename)
        # except:
        #     msg = QMessageBox(self)
        #     msg.setWindowTitle('Error')
        #     msg.setText('It was not possible read the file')
        #     msg.exec()
        #     return

        split_name = filename.split('/')
        split_name = split_name[-1].split('.')
        tr = QtCore.QCoreApplication.translate
        tab = self.tabWidget.currentWidget()
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(tab), tr("MainWindow", f"{split_name[0]}"))

        # set action select
        self.on_actionSelect()

    def exportFile_disp(self):
        # setup checked buttons
        self.setFalseButtonsChecked()

        # close displayers
        self.closeAllDisplayers()
        self.exportFile_display.setParent(self.leftToolbarFrame)
        self.exportFile_display.show()

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('SELECTION')

    def exportFile(self):
        option = self.exportFile_display.optionscomboBox.currentText()
        alType = self.exportFile_display.aloptionscomboBox.currentText()
        gpT3 = self.exportFile_display.T3comboBox.currentText()
        gpT6 = self.exportFile_display.T6comboBox.currentText()
        gpQ4 = self.exportFile_display.Q4comboBox.currentText()
        gpQ8 = self.exportFile_display.Q8comboBox.currentText()

        self.saveFile()
        self.current_hecontroller.exportFile(
            option, alType, gpT3, gpT6, gpQ4, gpQ8)

        """
        try:
            self.saveFile()
            self.current_hecontroller.exportFile(
                option, alType, gpT3, gpT6, gpQ4, gpQ8)
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText('it is not possible to export the model')
            msg.exec()
        """

    def closeEvent(self, event):
        self.exit()
        event.ignore()

    def exit(self):

        qm = QMessageBox
        ans = qm.question(
            self, 'Warning', "Do you really want to exit?", qm.Yes | qm.No)

        if ans == qm.No:
            return

        if len(self.canvas_list) == 0:
            QtCore.QCoreApplication.quit()

        while len(self.canvas_list) > 0:
            check = self.closetab(self.tabWidget.currentIndex())

            if not check:
                return

        QtCore.QCoreApplication.quit()

    def on_action_nsudv(self):

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('SELECTION')

        # setup buttons checked
        self.setFalseButtonsChecked()
        self.actionNsudv.setChecked(True)

        # close displayers
        self.closeAllDisplayers()
        self.nsudv_display.setParent(self.leftToolbarFrame)
        self.nsudv_display.show()

        # clean lineEdits
        self.nsudv_display.valuelineEdit.setText("0")
        self.nsudv_display.ratiolineEdit.setText("1.0")

    def setNumberSdv(self):

        Subdivision_option = self.nsudv_display.nsudvcomboBox.currentText()
        if Subdivision_option == "Set Subdivisions":
            try:
                number = int(self.nsudv_display.valuelineEdit.text())
                ratio = float(self.nsudv_display.ratiolineEdit.text())
            except:
                msg = QMessageBox(self)
                msg.setWindowTitle('Warning')
                msg.setText('These data fields only accept numbers')
                msg.exec()
                return
        
        elif Subdivision_option == "Get from Knot Vector":
            number = None
            ratio = None

        self.current_hecontroller.setNumberSdv(number, ratio)
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def refineNumberSdv(self):

        self.current_hecontroller.refineNumberSdv()
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def BackToOriginalNurbsRefine(self):

        self.current_hecontroller.BackToOriginalNurbsRefine()
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def BackToOriginalNurbs(self):

        check, error_text = self.current_hecontroller.BackToOriginalNurbs()
        if check:
            self.close_propEdge()
        elif not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()
            
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def degreeChange(self):

        check, error_text = self.current_hecontroller.degreeChange()
        if check:
            self.close_propEdge()
        elif not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def ReverseNurbs(self):

        check, error_text = self.current_hecontroller.ReverseNurbs()
        if check:
            self.close_propEdge()
        elif not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def conformSegs(self):

        check, error_text = self.current_hecontroller.conformSegs()
        if not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def updateCtrlPolyView(self):

        if self.prop_edge_display.ctrlPolygonCheckBox.isChecked():
            status = True
        else:
            status = False
        check, error_text = self.current_hecontroller.updateCtrlPolyView(status)
        if check:
            self.close_propEdge()
        elif not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

    def setUCurves(self):
        check, error_text = self.current_hecontroller.setUCurves()
        if not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

    def setVCurves(self):
        check, error_text = self.current_hecontroller.setVCurves()
        if not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(error_text)
            msg.exec()

    def AttributeManager(self):

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('SELECTION')

        # setup buttons checked
        self.setFalseButtonsChecked()
        self.actionAttmanager.setChecked(True)

        # close displayers
        self.closeAllDisplayers()
        self.attribute_display.setParent(self.leftToolbarFrame)
        self.attribute_display.show()

        # get attribute controller
        attManager = self.current_hecontroller.attManager
        prototypes = attManager.getPrototypes()
        attributes = attManager.getAttributes()

        # setup scrool area
        scrollAreaContent = QWidget()
        self.attribute_display.scrollArea.setWidget(scrollAreaContent)

        # set types
        self.attribute_display.typescomboBox.clear()
        for prototype in prototypes:
            self.attribute_display.typescomboBox.addItem(prototype['type'])

        # set attributes
        self.attribute_display.attcomboBox.clear()
        for att in attributes:
            self.attribute_display.attcomboBox.addItem(att['name'])

        # hide buttons
        self.attribute_display.setAttpushButton.hide()
        self.attribute_display.saveAttpushButton.hide()
        self.attribute_display.delpushButton.hide()
        self.attribute_display.renamepushButton.hide()
        self.attribute_display.renamelineEdit.hide()
        self.attribute_display.unsetpushButton.hide()

    def addAttribute(self):

        # get  hecontroller
        hecontroller = self.current_hecontroller

        # get prototype
        prototype = self.attribute_display.typescomboBox.currentText()

        # get name
        name = self.attribute_display.namelineEdit.text()

        if name == '':
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('You must name the attribute')
            msg.exec()
            return

        # add attribute
        check = hecontroller.addAttribute(prototype, name)
        if check:
            self.attribute_display.attcomboBox.addItem(name)
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('An attribute with that name already exists')
            msg.exec()

        self.attribute_display.namelineEdit.clear()
        self.attribute_display.attcomboBox.setCurrentText(name)

        # setup attPropertiesDisplay
        self.setAttPropertiesDisplay()

    def saveAttributeValues(self):

        # get attributeManager
        attManager = self.current_hecontroller.attManager

        # get attribute
        attName = self.attribute_display.attcomboBox.currentText()
        attribute = attManager.getAttributeByName(attName)

        if attribute is None:
            return

        attValues_type = attribute['properties_type']

        # get values
        values = []

        try:
            index = 0
            for propertiesItem in self.attpropertiesItems:
                if attValues_type[index] == "float":
                    values.append(float(propertiesItem.text()))
                elif attValues_type[index] == "int":
                    values.append(int(propertiesItem.text()))
                elif attValues_type[index] == "string":
                    values.append(propertiesItem.text())
                elif attValues_type[index] == "options":
                    options_dict = list(attribute['properties'].values())[
                        index].copy()
                    options_dict["index"] = propertiesItem.currentIndex()
                    values.append(options_dict)
                elif attValues_type[index] == "color":
                    txt = propertiesItem.text()
                    txt = txt.replace("[", "")
                    txt = txt.replace("]", "")
                    txt = txt.split(",")
                    rgbColor = []
                    for item in txt:
                        rgbColor.append(int(item))
                    values.append(rgbColor)
                elif attValues_type[index] == "bool":
                    if propertiesItem.isChecked():
                        values.append(True)
                    else:
                        values.append(False)

                index += 1
        except:
            # reset properties values
            self.setAttPropertiesDisplay()

            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These values are not acceptable')
            msg.exec()
            return

        # get name
        name = self.attribute_display.attcomboBox.currentText()

        # set the new values
        self.current_canvas.saveAtribute(name, values)

    def setAttribute(self):
        # get canvas
        canvas = self.current_canvas

        # get attribute
        name = self.attribute_display.attcomboBox.currentText()

        canvas.setAttribute(name)

    def unSetAttribute(self):
        # get canvas
        canvas = self.current_canvas

        # get attribute
        name = self.attribute_display.attcomboBox.currentText()

        canvas.unSetAttribute(name)

    def renameAttribute(self):
        new_name = self.attribute_display.renamelineEdit.text()
        old_name = self.attribute_display.attcomboBox.currentText()

        qm = QMessageBox
        ans = qm.question(
            self, 'Warning', f"Do you really want to rename {old_name}?", qm.Yes | qm.No)

        if ans == qm.No:
            return

        if new_name == '':
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('You must name the attribute')
            msg.exec()
            return

        # get hecontroller
        hecontroller = self.current_hecontroller

        check = hecontroller.renameAttribute(old_name, new_name)
        self.attribute_display.renamelineEdit.clear()

        if not check:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('An attribute with that name already exists')
            msg.exec()
            return

        # reset
        self.AttributeManager()
        self.attribute_display.attcomboBox.setCurrentText(new_name)
        self.setAttPropertiesDisplay()

    def delAttribute(self):

        # get name
        name = self.attribute_display.attcomboBox.currentText()

        qm = QMessageBox
        ans = qm.question(
            self, 'Warning', f"Do you really want to delete {name}?", qm.Yes | qm.No)

        if ans == qm.No:
            return

        # get canvas
        canvas = self.current_canvas

        # removes attribute
        canvas.delAttribute(name, self.attribute_display.attcomboBox)

        # setup attPropertiesDisplay
        self.setAttPropertiesDisplay()

    def setAttPropertiesDisplay(self, _index=None):
        attManager = self.current_hecontroller.attManager

        attName = self.attribute_display.attcomboBox.currentText()
        attribute = attManager.getAttributeByName(attName)

        # creates items for attribute display
        self.attpropertiesItems = self.attribute_display.setAttPropertiesDisplay(
            attribute)

        # show/hide buttons
        if self.attribute_display.attcomboBox.currentText() == '':
            self.attribute_display.setAttpushButton.hide()
            self.attribute_display.saveAttpushButton.hide()
            self.attribute_display.delpushButton.hide()
            self.attribute_display.renamepushButton.hide()
            self.attribute_display.renamelineEdit.hide()
            self.attribute_display.unsetpushButton.hide()
        else:
            self.attribute_display.setAttpushButton.show()
            self.attribute_display.saveAttpushButton.show()
            self.attribute_display.delpushButton.show()
            self.attribute_display.renamepushButton.show()
            self.attribute_display.renamelineEdit.show()
            self.attribute_display.unsetpushButton.show()

    def properties(self):

        if len(self.canvas_list) == 0:
            return False, None

        hemodel = self.current_hecontroller.hemodel
        selectedEntities = []
        selectedVertices = hemodel.selectedVertices()
        selectedEdges = hemodel.selectedEdges()
        selectedFaces = hemodel.selectedFaces()
        selectedEntities.extend(selectedVertices)
        selectedEntities.extend(selectedEdges)
        selectedEntities.extend(selectedFaces)

        if len(selectedEntities) == 1:

            self.closeAllDisplayers()
            self.current_canvas.prop_disp = True

            if len(selectedVertices) == 1:
                self.prop_vertex_display.setParent(self.leftToolbarFrame)
                self.prop_vertex_display.show()
                self.prop_vertex_display.set_vertex_prop(selectedEntities[0])
            elif len(selectedEdges) == 1:
                self.prop_edge_display.setParent(self.leftToolbarFrame)
                self.prop_edge_display.show()
                self.prop_edge_display.set_edge_prop(selectedEntities[0])
            elif not selectedEntities[0].patch.isDeleted:
                self.prop_face_display.setParent(self.leftToolbarFrame)
                self.prop_face_display.show()
                self.prop_face_display.set_face_prop(selectedEntities[0])
            else:
                self.select_display.show()
                self.current_canvas.prop_disp = False
                return False, None

            return True, selectedEntities[0]

        elif len(selectedEntities) > 1:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('Please select only one entity')
            msg.exec()

        self.closeAllDisplayers()
        self.select_display.show()

        return False, None

    def close_propVertex(self):
        check, _ = self.properties()

        if check:
            return

        self.prop_vertex_display.close()
        self.select_display.show()
        self.current_canvas.prop_disp = False

    def close_propEdge(self):
        check, _ = self.properties()

        if check:
            return

        self.prop_edge_display.close()
        self.select_display.show()
        self.current_canvas.prop_disp = False

    def close_propFace(self):
        check, _ = self.properties()

        if check:
            return

        self.prop_face_display.close()
        self.select_display.show()
        self.current_canvas.prop_disp = False

    def on_action_Mesh(self):
        # setup checked buttons
        self.setFalseButtonsChecked()
        self.actionMesh.setChecked(True)

        # set corresponding mouse action on canvas
        for canvas in self.canvas_list:
            canvas.setMouseAction('SELECTION')

        # close displayers
        self.closeAllDisplayers()
        self.mesh_display.setParent(self.leftToolbarFrame)
        self.mesh_display.show()

        self.setMeshOptions()

    def setMeshOptions(self):

        # setup display
        mesh_type = self.mesh_display.meshcomboBox.currentText()
        self.mesh_display.elemTypesLAbel.hide()
        self.mesh_display.shapecomboBox.hide()
        self.mesh_display.elemcomboBox.hide()
        self.mesh_display.diagTypesLabel.hide()
        self.mesh_display.diagcomboBox.hide()
        self.mesh_display.flagLabel.hide()
        self.mesh_display.flagcomboBox.hide()
        self.mesh_display.surfCurvesLabel.hide()
        self.mesh_display.surfUCurvespushButton.hide()
        self.mesh_display.surfVCurvespushButton.hide()
        
        if mesh_type == "Bilinear Transfinite":
            self.mesh_display.elemTypesLAbel.show()
            self.mesh_display.shapecomboBox.show()
            self.mesh_display.elemcomboBox.show()
            self.setDiagOptions()

            self.mesh_display.shapecomboBox.setGeometry(
                QtCore.QRect(25, 125, 150, 25))
            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 155, 150, 25))

        elif (mesh_type == "Trilinear Transfinite" or
              mesh_type == "Quadrilateral Seam" or
              mesh_type == "Quadrilateral Template"):
            self.mesh_display.elemTypesLAbel.show()
            self.mesh_display.elemcomboBox.show()

            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 125, 150, 25))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(50, 170, 100, 25))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(50, 200, 100, 25))
            
        elif mesh_type == "Triangular Boundary Contraction":
            self.mesh_display.elemTypesLAbel.show()
            self.mesh_display.elemcomboBox.show()
            self.mesh_display.flagLabel.show()
            self.mesh_display.flagcomboBox.show()

            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 125, 150, 25))
            self.mesh_display.flagLabel.setGeometry(
                QtCore.QRect(25, 170, 150, 20))
            self.mesh_display.flagcomboBox.setGeometry(
                QtCore.QRect(25, 190, 150, 25))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(50, 235, 100, 25))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(50, 265, 100, 25))
            
        elif (mesh_type == "Isogeometric" or 
              mesh_type == "Isogeometric Template"):
            self.mesh_display.surfCurvesLabel.show()
            self.mesh_display.surfUCurvespushButton.show()
            self.mesh_display.surfVCurvespushButton.show()
            
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(50, 200, 100, 25))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(50, 230, 100, 25))

    def setDiagOptions(self):
        shape_type = self.mesh_display.shapecomboBox.currentText()

        if shape_type == "Triangular":
            self.mesh_display.diagcomboBox.show()
            self.mesh_display.diagTypesLabel.show()

            self.mesh_display.diagTypesLabel.setGeometry(
                QtCore.QRect(0, 200, 200, 20))
            self.mesh_display.diagcomboBox.setGeometry(
                QtCore.QRect(25, 220, 150, 25))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(50, 265, 100, 25))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(50, 295, 100, 25))
        else:
            self.mesh_display.diagcomboBox.hide()
            self.mesh_display.diagTypesLabel.hide()

            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(50, 200, 100, 25))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(50, 230, 100, 25))

    def generateMesh(self):
        mesh_type = self.mesh_display.meshcomboBox.currentText()
        diag_type = self.mesh_display.diagcomboBox.currentText()
        elem_type = self.mesh_display.elemcomboBox.currentText()
        bc_flag = self.mesh_display.flagcomboBox.currentText()

        if mesh_type == "Trilinear Transfinite":
            shape_type = "Triangular"
        elif mesh_type == "Quadrilateral Template":
            shape_type = "Quadrilateral"
        elif mesh_type == "Quadrilateral Seam":
            shape_type = "Quadrilateral"
        elif mesh_type == "Triangular Boundary Contraction":
            shape_type = "Triangular"
        elif (mesh_type == "Isogeometric" or 
              mesh_type == "Isogeometric Template"):
            shape_type = "Quadrilateral"
        else:
            shape_type = self.mesh_display.shapecomboBox.currentText()

        try:
            self.current_canvas.generateMesh(mesh_type, shape_type, elem_type, diag_type, bc_flag)
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('It was not possible to generate the mesh')
            msg.exec()

    def delMesh(self):
        self.current_canvas.delMesh()

    def setFalseButtonsChecked(self):
        self.actionMesh.setChecked(False)
        self.actionAttmanager.setChecked(False)
        self.actionSelect.setChecked(False)
        self.actionPolyline.setChecked(False)
        self.actionCubicSpline.setChecked(False)
        self.actionCircle.setChecked(False)
        self.actionCircleArc.setChecked(False)
        self.actionEllipse.setChecked(False)
        self.actionEllipseArc.setChecked(False)
        self.actionLine.setChecked(False)
        self.actionPoint.setChecked(False)
        self.actionNsudv.setChecked(False)

    def showCurrentdisplay(self):
        if self.actionLine.isChecked():
            self.line_display.show()
        elif self.actionPolyline.isChecked():
            self.polyline_display.show()
        elif self.actionCubicSpline.isChecked():
            self.cubicspline_display.show()
        elif self.actionCircle.isChecked():
            self.circle_display.show()
        elif self.actionCircleArc.isChecked():
            self.circlearc_display.show()
        elif self.actionEllipse.isChecked():
            self.ellipse_display.show()
        elif self.actionEllipseArc.isChecked():
            self.ellipsearc_display.show()
        elif self.actionSelect.isChecked():
            self.select_display.show()
        elif self.actionPoint.isChecked():
            self.point_display.show()
        elif self.actionAttmanager.isChecked():
            self.attribute_display.show()
        elif self.actionMesh.isChecked():
            self.mesh_display.show()

    def closeAllDisplayers(self):
        self.select_display.close()
        self.point_display.close()
        self.line_display.close()
        self.polyline_display.close()
        self.cubicspline_display.close()
        self.circle_display.close()
        self.circlearc_display.close()
        self.ellipse_display.close()
        self.ellipsearc_display.close()
        self.grid_display.close()
        self.prop_vertex_display.close()
        self.prop_edge_display.close()
        self.prop_face_display.close()
        self.attribute_display.close()
        self.mesh_display.close()
        self.exportFile_display.close()
        self.nsudv_display.close()
        self.view_grid_display = False

        if len(self.tab_list) > 0:
            tab = self.tabWidget.currentWidget()
            currentIndex = self.getTabIndex(tab)
            self.canvas_list[currentIndex].prop_disp = False

    def clearDispText(self, _display):
        if _display == self.point_display:
            _display.PointXlineEdit.clear()
            _display.PointYlineEdit.clear()

        elif _display == self.line_display:
            _display.InitialPointXlineEdit.clear()
            _display.InitialPointYlineEdit.clear()
            _display.EndPointXlineEdit.clear()
            _display.EndPointYlineEdit.clear()

        elif _display == self.polyline_display:
            _display.InitialPointXlineEdit.clear()
            _display.InitialPointYlineEdit.clear()
            _display.EndPointXlineEdit.clear()
            _display.EndPointYlineEdit.clear()

        elif _display == self.cubicspline_display:
            _display.InitialPointXlineEdit.clear()
            _display.InitialPointYlineEdit.clear()
            _display.EndPointXlineEdit.clear()
            _display.EndPointYlineEdit.clear()

        elif _display == self.circle_display:
            _display.CenterXlineEdit.clear()
            _display.CenterYlineEdit.clear()
            _display.RadiusXlineEdit.clear()
            _display.RadiusYlineEdit.clear()

        elif _display == self.circlearc_display:
            _display.CenterXlineEdit.clear()
            _display.CenterYlineEdit.clear()
            _display.FirstArcPointXlineEdit.clear()
            _display.FirstArcPointYlineEdit.clear()
            _display.SecondArcPointXlineEdit.clear()
            _display.SecondArcPointYlineEdit.clear()

        elif _display == self.ellipse_display:
            _display.CenterXlineEdit.clear()
            _display.CenterYlineEdit.clear()
            _display.FirstAxisXlineEdit.clear()
            _display.FirstAxisYlineEdit.clear()
            _display.SecondAxisXlineEdit.clear()
            _display.SecondAxisYlineEdit.clear()

        elif _display == self.ellipsearc_display:
            _display.CenterXlineEdit.clear()
            _display.CenterYlineEdit.clear()
            _display.FirstAxisXlineEdit.clear()
            _display.FirstAxisYlineEdit.clear()
            _display.SecondAxisXlineEdit.clear()
            _display.SecondAxisYlineEdit.clear()
            _display.FirstArcPointXlineEdit.clear()
            _display.FirstArcPointYlineEdit.clear()
            _display.SecondArcPointXlineEdit.clear()
            _display.SecondArcPointYlineEdit.clear()

    # Set Enable in lineEdits, pushButtons and comboBoxes
    def set_curves_lineEdits(self):
        # get current canvas
        canvas = self.current_canvas

        # get curve type
        curve_type = canvas.collector.geoType

        # get current number of control points
        NumCtrlPt = canvas.collector.CurrentNumberOfControlPoints()

        # set lineEdits
        if curve_type == "LINE":
            if NumCtrlPt == 0:
                self.clearDispText(self.line_display)
                self.line_display.InitialPointXlineEdit.setEnabled(True)
                self.line_display.InitialPointYlineEdit.setEnabled(True)
                self.line_display.InitialPointpushButton.setEnabled(True)
                self.line_display.EndPointXlineEdit.setEnabled(False)
                self.line_display.EndPointYlineEdit.setEnabled(False)
                self.line_display.addLinepushButton.setEnabled(False)

            elif NumCtrlPt == 1:
                self.line_display.InitialPointXlineEdit.setEnabled(False)
                self.line_display.InitialPointYlineEdit.setEnabled(False)
                self.line_display.InitialPointpushButton.setEnabled(False)
                self.line_display.EndPointXlineEdit.setEnabled(True)
                self.line_display.EndPointYlineEdit.setEnabled(True)
                self.line_display.addLinepushButton.setEnabled(True)

        elif curve_type == "POLYLINE":
            if NumCtrlPt == 0:
                self.clearDispText(self.polyline_display)
                self.polyline_display.InitialPointXlineEdit.setEnabled(True)
                self.polyline_display.InitialPointYlineEdit.setEnabled(True)
                self.polyline_display.InitialPointpushButton.setEnabled(True)
                self.polyline_display.EndPointXlineEdit.setEnabled(False)
                self.polyline_display.EndPointYlineEdit.setEnabled(False)
                self.polyline_display.addPolylinepushButton.setEnabled(False)
                self.polyline_display.endPolylinepushButton.setEnabled(False)

            else:
                self.polyline_display.InitialPointXlineEdit.setEnabled(False)
                self.polyline_display.InitialPointYlineEdit.setEnabled(False)
                self.polyline_display.InitialPointpushButton.setEnabled(False)
                self.polyline_display.EndPointXlineEdit.setEnabled(True)
                self.polyline_display.EndPointYlineEdit.setEnabled(True)
                self.polyline_display.addPolylinepushButton.setEnabled(True)
                self.polyline_display.endPolylinepushButton.setEnabled(True)

        elif curve_type == "CUBICSPLINE":
            if NumCtrlPt == 0:
                self.clearDispText(self.cubicspline_display)
                self.cubicspline_display.InitialPointXlineEdit.setEnabled(True)
                self.cubicspline_display.InitialPointYlineEdit.setEnabled(True)
                self.cubicspline_display.InitialPointpushButton.setEnabled(True)
                self.cubicspline_display.EndPointXlineEdit.setEnabled(False)
                self.cubicspline_display.EndPointYlineEdit.setEnabled(False)
                self.cubicspline_display.addCubicSplinepushButton.setEnabled(False)
                self.cubicspline_display.endCubicSplinepushButton.setEnabled(False)

            else:
                self.cubicspline_display.InitialPointXlineEdit.setEnabled(False)
                self.cubicspline_display.InitialPointYlineEdit.setEnabled(False)
                self.cubicspline_display.InitialPointpushButton.setEnabled(False)
                self.cubicspline_display.EndPointXlineEdit.setEnabled(True)
                self.cubicspline_display.EndPointYlineEdit.setEnabled(True)
                self.cubicspline_display.addCubicSplinepushButton.setEnabled(True)
                self.cubicspline_display.endCubicSplinepushButton.setEnabled(True)

        elif curve_type == "CIRCLE":
            if NumCtrlPt == 0:
                self.clearDispText(self.circle_display)
                self.circle_display.CenterXlineEdit.setEnabled(True)
                self.circle_display.CenterYlineEdit.setEnabled(True)
                self.circle_display.setCenterpushButton.setEnabled(True)
                self.circle_display.RadiuscomboBox.setEnabled(False)
                self.circle_display.RadiusXlineEdit.setEnabled(False)
                self.circle_display.RadiusYlineEdit.setEnabled(False)
                self.circle_display.addCirclepushButton.setEnabled(False)

            elif NumCtrlPt == 1:
                self.circle_display.CenterXlineEdit.setEnabled(False)
                self.circle_display.CenterYlineEdit.setEnabled(False)
                self.circle_display.setCenterpushButton.setEnabled(False)
                self.circle_display.RadiuscomboBox.setEnabled(True)
                self.circle_display.RadiusXlineEdit.setEnabled(True)
                self.circle_display.RadiusYlineEdit.setEnabled(True)
                self.circle_display.addCirclepushButton.setEnabled(True)

        elif curve_type == "CIRCLEARC":
            if NumCtrlPt == 0:
                self.clearDispText(self.circlearc_display)
                self.circlearc_display.CenterXlineEdit.setEnabled(True)
                self.circlearc_display.CenterYlineEdit.setEnabled(True)
                self.circlearc_display.setCenterpushButton.setEnabled(True)
                self.circlearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.circlearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.circlearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.circlearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.circlearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.circlearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.circlearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.circlearc_display.addCircleArcpushButton.setEnabled(False)

            elif NumCtrlPt == 1:
                self.circlearc_display.CenterXlineEdit.setEnabled(False)
                self.circlearc_display.CenterYlineEdit.setEnabled(False)
                self.circlearc_display.setCenterpushButton.setEnabled(False)
                self.circlearc_display.FirstArcPointcomboBox.setEnabled(True)
                self.circlearc_display.FirstArcPointXlineEdit.setEnabled(True)
                self.circlearc_display.FirstArcPointYlineEdit.setEnabled(True)
                self.circlearc_display.setFirstArcPointpushButton.setEnabled(True)
                self.circlearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.circlearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.circlearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.circlearc_display.addCircleArcpushButton.setEnabled(False)

            elif NumCtrlPt == 2:
                self.circlearc_display.CenterXlineEdit.setEnabled(False)
                self.circlearc_display.CenterYlineEdit.setEnabled(False)
                self.circlearc_display.setCenterpushButton.setEnabled(False)
                self.circlearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.circlearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.circlearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.circlearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.circlearc_display.SecondArcPointcomboBox.setEnabled(True)
                SecondArcPoint_option = self.circlearc_display.SecondArcPointcomboBox.currentText()
                if SecondArcPoint_option == "Coordinates":
                    self.circlearc_display.SecondArcPointXlineEdit.setEnabled(True)
                elif SecondArcPoint_option == "Radius and Angle":
                    self.circlearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.circlearc_display.SecondArcPointYlineEdit.setEnabled(True)
                self.circlearc_display.addCircleArcpushButton.setEnabled(True)

        elif curve_type == "ELLIPSE":
            if NumCtrlPt == 0:
                self.clearDispText(self.ellipse_display)
                self.ellipse_display.CenterXlineEdit.setEnabled(True)
                self.ellipse_display.CenterYlineEdit.setEnabled(True)
                self.ellipse_display.setCenterpushButton.setEnabled(True)
                self.ellipse_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipse_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipse_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipse_display.setFirstAxispushButton.setEnabled(False)
                self.ellipse_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipse_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipse_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipse_display.addEllipsepushButton.setEnabled(False)

            elif NumCtrlPt == 1:
                self.ellipse_display.CenterXlineEdit.setEnabled(False)
                self.ellipse_display.CenterYlineEdit.setEnabled(False)
                self.ellipse_display.setCenterpushButton.setEnabled(False)
                self.ellipse_display.FirstAxiscomboBox.setEnabled(True)
                self.ellipse_display.FirstAxisXlineEdit.setEnabled(True)
                self.ellipse_display.FirstAxisYlineEdit.setEnabled(True)
                self.ellipse_display.setFirstAxispushButton.setEnabled(True)
                self.ellipse_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipse_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipse_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipse_display.addEllipsepushButton.setEnabled(False)

            elif NumCtrlPt == 2:
                self.ellipse_display.CenterXlineEdit.setEnabled(False)
                self.ellipse_display.CenterYlineEdit.setEnabled(False)
                self.ellipse_display.setCenterpushButton.setEnabled(False)
                self.ellipse_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipse_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipse_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipse_display.setFirstAxispushButton.setEnabled(False)
                self.ellipse_display.SecondAxiscomboBox.setEnabled(True)
                self.ellipse_display.SecondAxisXlineEdit.setEnabled(True)
                SecondAxis_option = self.ellipse_display.SecondAxiscomboBox.currentText()
                if SecondAxis_option == "Coordinates":
                    self.ellipse_display.SecondAxisYlineEdit.setEnabled(True)
                elif SecondAxis_option == "Length and Angle":
                    self.ellipse_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipse_display.addEllipsepushButton.setEnabled(True)

        elif curve_type == "ELLIPSEARC":
            if NumCtrlPt == 0:
                self.clearDispText(self.ellipsearc_display)
                self.ellipsearc_display.CenterXlineEdit.setEnabled(True)
                self.ellipsearc_display.CenterYlineEdit.setEnabled(True)
                self.ellipsearc_display.setCenterpushButton.setEnabled(True)
                self.ellipsearc_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstAxispushButton.setEnabled(False)
                self.ellipsearc_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setSecondAxispushButton.setEnabled(False)
                self.ellipsearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.ellipsearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.addEllipseArcpushButton.setEnabled(False)

            elif NumCtrlPt == 1:
                self.ellipsearc_display.CenterXlineEdit.setEnabled(False)
                self.ellipsearc_display.CenterYlineEdit.setEnabled(False)
                self.ellipsearc_display.setCenterpushButton.setEnabled(False)
                self.ellipsearc_display.FirstAxiscomboBox.setEnabled(True)
                self.ellipsearc_display.FirstAxisXlineEdit.setEnabled(True)
                self.ellipsearc_display.FirstAxisYlineEdit.setEnabled(True)
                self.ellipsearc_display.setFirstAxispushButton.setEnabled(True)
                self.ellipsearc_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setSecondAxispushButton.setEnabled(False)
                self.ellipsearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.ellipsearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.addEllipseArcpushButton.setEnabled(False)

            elif NumCtrlPt == 2:
                self.ellipsearc_display.CenterXlineEdit.setEnabled(False)
                self.ellipsearc_display.CenterYlineEdit.setEnabled(False)
                self.ellipsearc_display.setCenterpushButton.setEnabled(False)
                self.ellipsearc_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstAxispushButton.setEnabled(False)
                self.ellipsearc_display.SecondAxiscomboBox.setEnabled(True)
                self.ellipsearc_display.SecondAxisXlineEdit.setEnabled(True)
                SecondAxis_option = self.ellipsearc_display.SecondAxiscomboBox.currentText()
                if SecondAxis_option == "Coordinates":
                    self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(True)
                elif SecondAxis_option == "Length and Angle":
                    self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setSecondAxispushButton.setEnabled(True)
                self.ellipsearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.ellipsearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.addEllipseArcpushButton.setEnabled(False)

            elif NumCtrlPt == 3:
                self.ellipsearc_display.CenterXlineEdit.setEnabled(False)
                self.ellipsearc_display.CenterYlineEdit.setEnabled(False)
                self.ellipsearc_display.setCenterpushButton.setEnabled(False)
                self.ellipsearc_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstAxispushButton.setEnabled(False)
                self.ellipsearc_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setSecondAxispushButton.setEnabled(False)
                self.ellipsearc_display.FirstArcPointcomboBox.setEnabled(True)
                FirstArcPoint_option = self.ellipsearc_display.FirstArcPointcomboBox.currentText()
                if FirstArcPoint_option == "Coordinates":
                    self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(True)
                elif FirstArcPoint_option == "Length and Angle":
                    self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstArcPointYlineEdit.setEnabled(True)
                self.ellipsearc_display.setFirstArcPointpushButton.setEnabled(True)
                self.ellipsearc_display.SecondArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.addEllipseArcpushButton.setEnabled(False)

            elif NumCtrlPt == 4:
                self.ellipsearc_display.CenterXlineEdit.setEnabled(False)
                self.ellipsearc_display.CenterYlineEdit.setEnabled(False)
                self.ellipsearc_display.setCenterpushButton.setEnabled(False)
                self.ellipsearc_display.FirstAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.FirstAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstAxispushButton.setEnabled(False)
                self.ellipsearc_display.SecondAxiscomboBox.setEnabled(False)
                self.ellipsearc_display.SecondAxisXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
                self.ellipsearc_display.setSecondAxispushButton.setEnabled(False)
                self.ellipsearc_display.FirstArcPointcomboBox.setEnabled(False)
                self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.FirstArcPointYlineEdit.setEnabled(False)
                self.ellipsearc_display.setFirstArcPointpushButton.setEnabled(False)
                self.ellipsearc_display.SecondArcPointcomboBox.setEnabled(True)
                SecondArcPoint_option = self.ellipsearc_display.SecondArcPointcomboBox.currentText()
                if SecondArcPoint_option == "Coordinates":
                    self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(True)
                elif SecondArcPoint_option == "Length and Angle":
                    self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
                self.ellipsearc_display.SecondArcPointYlineEdit.setEnabled(True)
                self.ellipsearc_display.addEllipseArcpushButton.setEnabled(True)

    # Set texts in lineEdits
    def set_curves_lineEdits_text(self, xW, yW):
        # get current canvas
        canvas = self.current_canvas

        # get curve type
        curve_type = canvas.collector.geoType

        # get current number of control points
        NumCtrlPt = canvas.collector.CurrentNumberOfControlPoints()

        # set lineEdits text
        if curve_type == "LINE":
            if NumCtrlPt == 0:
                self.line_display.InitialPointXlineEdit.setText(str(round(xW, 3)))
                self.line_display.InitialPointYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                self.line_display.EndPointXlineEdit.setText(str(round(xW, 3)))
                self.line_display.EndPointYlineEdit.setText(str(round(yW, 3)))

        elif curve_type == "POLYLINE":
            if NumCtrlPt == 0:
                self.polyline_display.InitialPointXlineEdit.setText(str(round(xW, 3)))
                self.polyline_display.InitialPointYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                self.polyline_display.EndPointXlineEdit.setText(str(round(xW, 3)))
                self.polyline_display.EndPointYlineEdit.setText(str(round(yW, 3)))

            else:
                v1, v2 = canvas.collector.updateLineEditValues(NumCtrlPt, 0.0, False)
                self.polyline_display.InitialPointXlineEdit.setText(str(round(v1, 3)))
                self.polyline_display.InitialPointYlineEdit.setText(str(round(v2, 3)))
                self.polyline_display.EndPointXlineEdit.setText(str(round(xW, 3)))
                self.polyline_display.EndPointYlineEdit.setText(str(round(yW, 3)))

        elif curve_type == "CUBICSPLINE":
            if NumCtrlPt == 0:
                self.cubicspline_display.InitialPointXlineEdit.setText(str(round(xW, 3)))
                self.cubicspline_display.InitialPointYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                self.cubicspline_display.EndPointXlineEdit.setText(str(round(xW, 3)))
                self.cubicspline_display.EndPointYlineEdit.setText(str(round(yW, 3)))

            else:
                v1, v2 = canvas.collector.updateLineEditValues(NumCtrlPt, 0.0, False)
                self.cubicspline_display.InitialPointXlineEdit.setText(str(round(v1, 3)))
                self.cubicspline_display.InitialPointYlineEdit.setText(str(round(v2, 3)))
                self.cubicspline_display.EndPointXlineEdit.setText(str(round(xW, 3)))
                self.cubicspline_display.EndPointYlineEdit.setText(str(round(yW, 3)))

        elif curve_type == "CIRCLE":
            if NumCtrlPt == 0:
                self.circle_display.CenterXlineEdit.setText(str(round(xW, 3)))
                self.circle_display.CenterYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                Radius_option = self.circle_display.RadiuscomboBox.currentText()
                if Radius_option == "Coordinates":
                    LenAndAng = False
                elif Radius_option == "Radius and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.circle_display.RadiusXlineEdit.setText(str(round(v1, 3)))
                self.circle_display.RadiusYlineEdit.setText(str(round(v2, 3)))

        elif curve_type == "CIRCLEARC":
            if NumCtrlPt == 0:
                self.circlearc_display.CenterXlineEdit.setText(str(round(xW, 3)))
                self.circlearc_display.CenterYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                FirstArcPoint_option = self.circlearc_display.FirstArcPointcomboBox.currentText()
                if FirstArcPoint_option == "Coordinates":
                    LenAndAng = False
                elif FirstArcPoint_option == "Radius and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.circlearc_display.FirstArcPointXlineEdit.setText(str(round(v1, 3)))
                self.circlearc_display.FirstArcPointYlineEdit.setText(str(round(v2, 3)))

            elif NumCtrlPt == 2:
                SecondArcPoint_option = self.circlearc_display.SecondArcPointcomboBox.currentText()
                if SecondArcPoint_option == "Coordinates":
                    LenAndAng = False
                elif SecondArcPoint_option == "Radius and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.circlearc_display.SecondArcPointXlineEdit.setText(str(round(v1, 3)))
                self.circlearc_display.SecondArcPointYlineEdit.setText(str(round(v2, 3)))

        elif curve_type == "ELLIPSE":
            if NumCtrlPt == 0:
                self.ellipse_display.CenterXlineEdit.setText(str(round(xW, 3)))
                self.ellipse_display.CenterYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                FirstAxis_option = self.ellipse_display.FirstAxiscomboBox.currentText()
                if FirstAxis_option == "Coordinates":
                    LenAndAng = False
                elif FirstAxis_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipse_display.FirstAxisXlineEdit.setText(str(round(v1, 3)))
                self.ellipse_display.FirstAxisYlineEdit.setText(str(round(v2, 3)))

            elif NumCtrlPt == 2:
                SecondAxis_option = self.ellipse_display.SecondAxiscomboBox.currentText()
                if SecondAxis_option == "Coordinates":
                    LenAndAng = False
                elif SecondAxis_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipse_display.SecondAxisXlineEdit.setText(str(round(v1, 3)))
                self.ellipse_display.SecondAxisYlineEdit.setText(str(round(v2, 3)))

        elif curve_type == "ELLIPSEARC":
            if NumCtrlPt == 0:
                self.ellipsearc_display.CenterXlineEdit.setText(str(round(xW, 3)))
                self.ellipsearc_display.CenterYlineEdit.setText(str(round(yW, 3)))

            elif NumCtrlPt == 1:
                FirstAxis_option = self.ellipsearc_display.FirstAxiscomboBox.currentText()
                if FirstAxis_option == "Coordinates":
                    LenAndAng = False
                elif FirstAxis_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipsearc_display.FirstAxisXlineEdit.setText(str(round(v1, 3)))
                self.ellipsearc_display.FirstAxisYlineEdit.setText(str(round(v2, 3)))

            elif NumCtrlPt == 2:
                SecondAxis_option = self.ellipsearc_display.SecondAxiscomboBox.currentText()
                if SecondAxis_option == "Coordinates":
                    LenAndAng = False
                elif SecondAxis_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipsearc_display.SecondAxisXlineEdit.setText(str(round(v1, 3)))
                self.ellipsearc_display.SecondAxisYlineEdit.setText(str(round(v2, 3)))

            elif NumCtrlPt == 3:
                FirstArcPoint_option = self.ellipsearc_display.FirstArcPointcomboBox.currentText()
                if FirstArcPoint_option == "Coordinates":
                    LenAndAng = False
                elif FirstArcPoint_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipsearc_display.FirstArcPointXlineEdit.setText(str(round(v1, 3)))
                self.ellipsearc_display.FirstArcPointYlineEdit.setText(str(round(v2, 3)))

            elif NumCtrlPt == 4:
                SecondArcPoint_option = self.ellipsearc_display.SecondArcPointcomboBox.currentText()
                if SecondArcPoint_option == "Coordinates":
                    LenAndAng = False
                elif SecondArcPoint_option == "Length and Angle":
                    LenAndAng = True
                v1, v2 = canvas.collector.updateLineEditValues(xW, yW, LenAndAng)
                self.ellipsearc_display.SecondArcPointXlineEdit.setText(str(round(v1, 3)))
                self.ellipsearc_display.SecondArcPointYlineEdit.setText(str(round(v2, 3)))

    # Check Circle comboBoxes options
    def setCircleRadiusOptions(self):
        _translate = QtCore.QCoreApplication.translate
        Radius_option = self.circle_display.RadiuscomboBox.currentText()

        if Radius_option == "Coordinates":
            self.circle_display.RadiusXTitle.setText(_translate("MainWindow", "X:"))
            self.circle_display.RadiusYTitle.setText(_translate("MainWindow", "Y:"))
            self.circle_display.RadiusXlineEdit.clear()
            self.circle_display.RadiusYlineEdit.clear()
        elif Radius_option == "Radius and Angle":
            self.circle_display.RadiusXTitle.setText(_translate("MainWindow", "Radius:"))
            self.circle_display.RadiusYTitle.setText(_translate("MainWindow", "Angle:"))
            self.circle_display.RadiusXlineEdit.clear()
            self.circle_display.RadiusYlineEdit.clear()

    # Check Circle Arc comboBoxes options
    def setCircleArcFirstArcPointOptions(self):
        _translate = QtCore.QCoreApplication.translate
        FirstArcPoint_option = self.circlearc_display.FirstArcPointcomboBox.currentText()

        if FirstArcPoint_option == "Coordinates":
            self.circlearc_display.FirstArcPointXTitle.setText(_translate("MainWindow", "X:"))
            self.circlearc_display.FirstArcPointYTitle.setText(_translate("MainWindow", "Y:"))
            self.circlearc_display.FirstArcPointXlineEdit.clear()
            self.circlearc_display.FirstArcPointYlineEdit.clear()
        elif FirstArcPoint_option == "Radius and Angle":
            self.circlearc_display.FirstArcPointXTitle.setText(_translate("MainWindow", "Radius:"))
            self.circlearc_display.FirstArcPointYTitle.setText(_translate("MainWindow", "Angle:"))
            self.circlearc_display.FirstArcPointXlineEdit.clear()
            self.circlearc_display.FirstArcPointYlineEdit.clear()

    def setCircleArcSecondArcPointOptions(self):
        _translate = QtCore.QCoreApplication.translate
        SecondArcPoint_option = self.circlearc_display.SecondArcPointcomboBox.currentText()

        if SecondArcPoint_option == "Coordinates":
            self.circlearc_display.SecondArcPointXTitle.setText(_translate("MainWindow", "X:"))
            self.circlearc_display.SecondArcPointYTitle.setText(_translate("MainWindow", "Y:"))
            self.circlearc_display.SecondArcPointXlineEdit.setEnabled(True)
            self.circlearc_display.SecondArcPointXlineEdit.clear()
            self.circlearc_display.SecondArcPointYlineEdit.clear()
        elif SecondArcPoint_option == "Radius and Angle":
            self.circlearc_display.SecondArcPointXTitle.setText(_translate("MainWindow", "Radius:"))
            self.circlearc_display.SecondArcPointYTitle.setText(_translate("MainWindow", "Angle:"))
            self.circlearc_display.SecondArcPointXlineEdit.setEnabled(False)
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.circlearc_display.SecondArcPointYlineEdit.clear()

    # Check Ellipse comboBoxes options
    def setEllipseFirstAxisOptions(self):
        _translate = QtCore.QCoreApplication.translate
        FirstAxis_option = self.ellipse_display.FirstAxiscomboBox.currentText()

        if FirstAxis_option == "Coordinates":
            self.ellipse_display.FirstAxisXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipse_display.FirstAxisYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipse_display.FirstAxisXlineEdit.clear()
            self.ellipse_display.FirstAxisYlineEdit.clear()
        elif FirstAxis_option == "Length and Angle":
            self.ellipse_display.FirstAxisXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipse_display.FirstAxisYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipse_display.FirstAxisXlineEdit.clear()
            self.ellipse_display.FirstAxisYlineEdit.clear()

    def setEllipseSecondAxisOptions(self):
        _translate = QtCore.QCoreApplication.translate
        SecondAxis_option = self.ellipse_display.SecondAxiscomboBox.currentText()

        if SecondAxis_option == "Coordinates":
            self.ellipse_display.SecondAxisXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipse_display.SecondAxisYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipse_display.SecondAxisYlineEdit.setEnabled(True)
            self.ellipse_display.SecondAxisXlineEdit.clear()
            self.ellipse_display.SecondAxisYlineEdit.clear()
        elif SecondAxis_option == "Length and Angle":
            self.ellipse_display.SecondAxisXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipse_display.SecondAxisYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipse_display.SecondAxisYlineEdit.setEnabled(False)
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.ellipse_display.SecondAxisXlineEdit.clear()

    # Check Ellipse Arc comboBoxes options
    def setEllipseArcFirstAxisOptions(self):
        _translate = QtCore.QCoreApplication.translate
        FirstAxis_option = self.ellipsearc_display.FirstAxiscomboBox.currentText()

        if FirstAxis_option == "Coordinates":
            self.ellipsearc_display.FirstAxisXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipsearc_display.FirstAxisYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipsearc_display.FirstAxisXlineEdit.clear()
            self.ellipsearc_display.FirstAxisYlineEdit.clear()
        elif FirstAxis_option == "Length and Angle":
            self.ellipsearc_display.FirstAxisXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipsearc_display.FirstAxisYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipsearc_display.FirstAxisXlineEdit.clear()
            self.ellipsearc_display.FirstAxisYlineEdit.clear()

    def setEllipseArcSecondAxisOptions(self):
        _translate = QtCore.QCoreApplication.translate
        SecondAxis_option = self.ellipsearc_display.SecondAxiscomboBox.currentText()

        if SecondAxis_option == "Coordinates":
            self.ellipsearc_display.SecondAxisXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipsearc_display.SecondAxisYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(True)
            self.ellipsearc_display.SecondAxisXlineEdit.clear()
            self.ellipsearc_display.SecondAxisYlineEdit.clear()
        elif SecondAxis_option == "Length and Angle":
            self.ellipsearc_display.SecondAxisXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipsearc_display.SecondAxisYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipsearc_display.SecondAxisYlineEdit.setEnabled(False)
            self.set_curves_lineEdits_text(0.0, 0.0)
            self.ellipsearc_display.SecondAxisXlineEdit.clear()

    def setEllipseArcFirstArcPointOptions(self):
        _translate = QtCore.QCoreApplication.translate
        FirstArcPoint_option = self.ellipsearc_display.FirstArcPointcomboBox.currentText()

        if FirstArcPoint_option == "Coordinates":
            self.ellipsearc_display.FirstArcPointXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipsearc_display.FirstArcPointYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(True)
            self.ellipsearc_display.FirstArcPointXlineEdit.clear()
            self.ellipsearc_display.FirstArcPointYlineEdit.clear()
        elif FirstArcPoint_option == "Length and Angle":
            self.ellipsearc_display.FirstArcPointXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipsearc_display.FirstArcPointYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipsearc_display.FirstArcPointXlineEdit.setEnabled(False)
            self.ellipsearc_display.FirstArcPointXlineEdit.clear()
            self.ellipsearc_display.FirstArcPointYlineEdit.clear()

    def setEllipseArcSecondArcPointOptions(self):
        _translate = QtCore.QCoreApplication.translate
        SecondArcPoint_option = self.ellipsearc_display.SecondArcPointcomboBox.currentText()

        if SecondArcPoint_option == "Coordinates":
            self.ellipsearc_display.SecondArcPointXTitle.setText(_translate("MainWindow", "X:"))
            self.ellipsearc_display.SecondArcPointYTitle.setText(_translate("MainWindow", "Y:"))
            self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(True)
            self.ellipsearc_display.SecondArcPointXlineEdit.clear()
            self.ellipsearc_display.SecondArcPointYlineEdit.clear()
        elif SecondArcPoint_option == "Length and Angle":
            self.ellipsearc_display.SecondArcPointXTitle.setText(_translate("MainWindow", "Length:"))
            self.ellipsearc_display.SecondArcPointYTitle.setText(_translate("MainWindow", "Angle:"))
            self.ellipsearc_display.SecondArcPointXlineEdit.setEnabled(False)
            self.ellipsearc_display.SecondArcPointXlineEdit.clear()
            self.ellipsearc_display.SecondArcPointYlineEdit.clear()

    # Check Number os Subdivisions comboBox options
    def setNumSubdivisionsOptions(self):
        _translate = QtCore.QCoreApplication.translate
        Subdivision_option = self.nsudv_display.nsudvcomboBox.currentText()

        if Subdivision_option == "Set Subdivisions":
            self.nsudv_display.valueTitle.show()
            self.nsudv_display.valuelineEdit.show()
            self.nsudv_display.ratioTitle.show()
            self.nsudv_display.ratiolineEdit.show()
            self.nsudv_display.nsudvpushButton.setGeometry(QtCore.QRect(70, 140, 60, 25))
            self.nsudv_display.nsudvpushButton.setText(_translate("MainWindow", "Set"))
            self.nsudv_display.knotrefinementTitle.hide()
            self.nsudv_display.knotrefinementpushButton.hide()
            self.nsudv_display.rescuepushButton.hide()
            self.nsudv_display.knotconformTitle.hide()
            self.nsudv_display.knotconformpushButton.hide()
        elif Subdivision_option == "Get from Knot Vector":
            self.nsudv_display.valueTitle.hide()
            self.nsudv_display.valuelineEdit.hide()
            self.nsudv_display.ratioTitle.hide()
            self.nsudv_display.ratiolineEdit.hide()
            self.nsudv_display.nsudvpushButton.setGeometry(QtCore.QRect(70, 100, 60, 25))
            self.nsudv_display.nsudvpushButton.setText(_translate("MainWindow", "Get"))
            self.nsudv_display.knotrefinementTitle.show()
            self.nsudv_display.knotrefinementpushButton.show()
            self.nsudv_display.rescuepushButton.show()
            self.nsudv_display.knotconformTitle.show()
            self.nsudv_display.knotconformpushButton.show()