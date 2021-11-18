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
        # É so um teste rsrsrs
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

        # QpushButtons
        self.grid_display.gridOKpushButton.clicked.connect(self.setgrid)
        self.line_display.addlinepushButton.clicked.connect(self.add_line)
        self.polyline_display.addlinepushButton.clicked.connect(
            self.add_polyline)
        self.polyline_display.endsegmenttpushButton.clicked.connect(
            self.end_segment)
        self.point_display.addpointpushButton.clicked.connect(self.add_point)
        self.select_display.propertiespushButton.clicked.connect(
            self.properties)
        self.attribute_display.addpushButton.clicked.connect(self.addAttribute)
        self.attribute_display.saveAttpushButton.clicked.connect(
            self.saveAttributeValues)
        self.attribute_display.delpushButton.clicked.connect(self.delAttribute)
        self.attribute_display.setAttpushButton.clicked.connect(
            self.setAttribute)
        self.attribute_display.unsetpushButton.clicked.connect(
            self.unSetAttribute)
        self.attribute_display.renamepushButton.clicked.connect(
            self.renameAttribute)
        self.prop_face_display.closepushbutton.clicked.connect(
            self.close_propFace)
        self.prop_edge_display.closepushbutton.clicked.connect(
            self.close_propEdge)
        self.prop_vertex_display.closepushbutton.clicked.connect(
            self.close_propVertex)
        self.mesh_display.genMeshpushButton.clicked.connect(self.generateMesh)
        self.mesh_display.delMeshpushButton.clicked.connect(self.delMesh)
        self.exportFile_display.exportpushButton.clicked.connect(
            self.exportFile)
        self.nsudv_display.nsudvpushButton.clicked.connect(
            self.setNumberOfSubdivisions)

        # checkBoxes
        self.snapcheckBox.clicked.connect(self.change_snapgrid)
        self.select_display.pointcheckBox.clicked.connect(self.change_select)
        self.select_display.segmentcheckBox.clicked.connect(self.change_select)
        self.select_display.patchcheckBox.clicked.connect(self.change_select)

        # comboBoxes
        self.attribute_display.attcomboBox.activated.connect(
            self.setAttPropertiesDisplay)
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
        self.setEnableLineEdits(self.current_canvas)
        self.current_canvas.collector.endGeoCollection()
        self.clearDispText(self.line_display)
        self.clearDispText(self.polyline_display)

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
            self.setEnableLineEdits(self.current_canvas)
            self.clearDispText(self.line_display)
            self.clearDispText(self.polyline_display)

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

        try:
            x = float(self.point_display.xlineEdit.text())
            y = float(self.point_display.ylineEdit.text())
        except:
            self.clearDispText(self.point_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        self.current_canvas.hecontroller.insertPoint(
            Point(x, y), 0.01)
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

        # clear txts
        self.clearDispText(self.point_display)

    def add_line(self):
        if len(self.canvas_list) == 0:
            return

        # get current canvas
        canvas = self.current_canvas

        # Get points from lineEdits
        try:
            x1 = float(self.line_display.firstpointXlineEdit.text())
            y1 = float(self.line_display.firstpointYlineEdit.text())
            x2 = float(self.line_display.endpointXlineEdit.text())
            y2 = float(self.line_display.endpointYlineEdit.text())
        except:
            self.clearDispText(self.line_display)
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check if the points given are equal
        if x1 == x2 and y1 == y2:
            self.clearDispText(self.line_display)
            msg = QMessageBox()
            msg.setWindowTitle('Warning')
            msg.setText(
                'The first point is equal to the second.Thus, it is not possible to make a line')
            msg.exec()
            return

        pick_tol = 0
        # start collection and add the first point
        if not canvas.collector.isActive():
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x1, y1, pick_tol)

        # add the end point
        canvas.collector.insertPoint(x2, y2, pick_tol)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, 0.01)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # Set enable first point Line Edit
        self.line_display.firstpointXlineEdit.setEnabled(True)
        self.line_display.firstpointYlineEdit.setEnabled(True)

        # clear txts
        self.clearDispText(self.line_display)

    def add_polyline(self):
        if len(self.canvas_list) == 0:
            return

        # Get points from lineEdit
        try:
            x1 = float(self.polyline_display.firstpointXlineEdit.text())
            y1 = float(self.polyline_display.firstpointYlineEdit.text())
            x2 = float(self.polyline_display.endpointXlineEdit.text())
            y2 = float(self.polyline_display.endpointYlineEdit.text())
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        # check if the points given are equal
        if x1 == x2 and y1 == y2:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText(
                'The first point is equal to the second. Thus, it is not possible to make a line')
            msg.exec()
            return

        pick_tol = 0
        canvas = self.current_canvas
        if not canvas.collector.isActive():
            # start collection
            canvas.collector.startGeoCollection()
            canvas.collector.insertPoint(x1, y1, pick_tol)
            canvas.collector.insertPoint(x2, y2, pick_tol)

            # Set enable first point Line Edit
            self.polyline_display.firstpointXlineEdit.setEnabled(False)
            self.polyline_display.firstpointYlineEdit.setEnabled(False)

        else:
            canvas.collector.insertPoint(x2, y2, pick_tol)

        # set texts in the first point
        self.polyline_display.firstpointXlineEdit.setText(str(x2))
        self.polyline_display.firstpointYlineEdit.setText(str(y2))

        # Actives the drawing in the canvas
        canvas.mouseButton = QtCore.Qt.LeftButton
        canvas.collector.addTempPoint(x2, y2)
        canvas.update()

        # clear texts in the end point of the line
        self.polyline_display.endpointXlineEdit.clear()
        self.polyline_display.endpointYlineEdit.clear()

    def end_segment(self):
        if len(self.canvas_list) == 0:
            return

        canvas = self.current_canvas
        if not canvas.collector.isActive():
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('The segment has no lines added')
            msg.exec()
            return

        # Set enable first point Line Edit
        self.polyline_display.firstpointXlineEdit.setEnabled(True)
        self.polyline_display.firstpointYlineEdit.setEnabled(True)

        # end collection:
        segment = canvas.collector.getCollectedGeo()
        canvas.hecontroller.insertSegment(segment, 0.01)
        canvas.collector.endGeoCollection()
        canvas.updatedDsp = False
        canvas.update()

        # clear texts
        self.clearDispText(self.polyline_display)

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

        try:
            self.current_canvas.openFile(filename)
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText('It was not possible read the file')
            msg.exec()
            return

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

    def setNumberOfSubdivisions(self):

        try:
            number = int(self.nsudv_display.valuelineEdit.text())
            ratio = float(self.nsudv_display.ratiolineEdit.text())
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle('Warning')
            msg.setText('These data fields only accept numbers')
            msg.exec()
            return

        self.current_hecontroller.setNumberOfSubdivisions(number, ratio)
        self.current_canvas.updatedDsp = False
        self.current_canvas.update()

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
        self.mesh_display.genMeshpushButton.show()
        mesh_type = self.mesh_display.meshcomboBox.currentText()
        self.mesh_display.shapecomboBox.hide()
        self.mesh_display.flagcomboBox.hide()
        self.mesh_display.flagLabel.hide()
        self.mesh_display.diagcomboBox.hide()
        self.mesh_display.diagTypesLabel.hide()

        if mesh_type == "Bilinear Transfinite":
            self.mesh_display.shapecomboBox.show()
            self.setDiagOptions()

            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 160, 150, 20))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(55, 260, 90, 23))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(55, 290, 90, 23))

        elif mesh_type == "Triangular Boundary Contraction":
            self.mesh_display.flagcomboBox.show()
            self.mesh_display.flagLabel.show()

            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 130, 150, 20))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(55, 220, 90, 23))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(55, 250, 90, 23))
        else:
            self.mesh_display.elemcomboBox.setGeometry(
                QtCore.QRect(25, 130, 150, 20))
            self.mesh_display.genMeshpushButton.setGeometry(
                QtCore.QRect(55, 160, 90, 23))
            self.mesh_display.delMeshpushButton.setGeometry(
                QtCore.QRect(55, 190, 90, 23))

    def setDiagOptions(self):

        shape_type = self.mesh_display.shapecomboBox.currentText()

        if shape_type == "Triangular":
            self.mesh_display.diagcomboBox.show()
            self.mesh_display.diagTypesLabel.show()
        else:
            self.mesh_display.diagcomboBox.hide()
            self.mesh_display.diagTypesLabel.hide()

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
        else:
            shape_type = self.mesh_display.shapecomboBox.currentText()

        try:
            self.current_canvas.generateMesh(
                mesh_type, shape_type, elem_type, diag_type, bc_flag)
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
        self.actionLine.setChecked(False)
        self.actionPoint.setChecked(False)
        self.actionNsudv.setChecked(False)

    def showCurrentdisplay(self):
        if self.actionLine.isChecked():
            self.line_display.show()
        elif self.actionPolyline.isChecked():
            self.polyline_display.show()
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
        if _display == self.line_display or _display == self.polyline_display:
            _display.firstpointXlineEdit.clear()
            _display.firstpointYlineEdit.clear()
            _display.endpointXlineEdit.clear()
            _display.endpointYlineEdit.clear()
        elif _display == self.point_display:
            _display.xlineEdit.clear()
            _display.ylineEdit.clear()

    def setFirstLineEditText(self, xW, yW, _canvas):

        geo_type = _canvas.collector.getGeoType()

        if geo_type == 'LINE':
            self.line_display.firstpointXlineEdit.setText(str(round(xW, 3)))
            self.line_display.firstpointYlineEdit.setText(str(round(yW, 3)))
            self.line_display.firstpointXlineEdit.setEnabled(False)
            self.line_display.firstpointYlineEdit.setEnabled(False)
        elif geo_type == 'POLYLINE':
            self.polyline_display.firstpointXlineEdit.setText(
                str(round(xW, 3)))
            self.polyline_display.firstpointYlineEdit.setText(
                str(round(yW, 3)))
            self.polyline_display.firstpointXlineEdit.setEnabled(False)
            self.polyline_display.firstpointYlineEdit.setEnabled(False)

    def setEndLineEditText(self, xW, yW, _canvas):

        geo_type = _canvas.collector.getGeoType()

        if geo_type == 'LINE':
            self.line_display.endpointXlineEdit.setText(str(round(xW, 3)))
            self.line_display.endpointYlineEdit.setText(str(round(yW, 3)))
        elif geo_type == 'POLYLINE':
            self.polyline_display.endpointXlineEdit.setText(str(round(xW, 3)))
            self.polyline_display.endpointYlineEdit.setText(str(round(yW, 3)))

    def setEnableLineEdits(self, _canvas):

        geo_type = _canvas.collector.getGeoType()

        if geo_type == 'LINE':
            self.clearDispText(self.line_display)
            self.line_display.firstpointXlineEdit.setEnabled(True)
            self.line_display.firstpointYlineEdit.setEnabled(True)
        elif geo_type == 'POLYLINE':
            self.clearDispText(self.polyline_display)
            self.polyline_display.firstpointXlineEdit.setEnabled(True)
            self.polyline_display.firstpointYlineEdit.setEnabled(True)
