from geometry.point import Point
from compgeom.tesselation import Tesselation
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt5 import QtOpenGL, QtCore, QtGui
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from grid import Grid
from geocollector import GeoCollector
from geometry.attributes.attribsymbols import AttribSymbols
import math


class Canvas(QtOpenGL.QGLWidget):

    def __init__(self, _App, _hecontroller):
        super(Canvas, self).__init__()

        self.Apptools = _App  # handle to App tools
        self.hecontroller = _hecontroller  # handle to controller of half-edge structer
        self.view = None  # view to be displayed
        self.viewDsp = 0  # GL list index for model display
        self.attDsp = 0  # GL list index for att model display
        self.updatedDsp = False  # if true, model display is updated

        self.canvas_widht = 1.0  # width: Gl canvas horizontal size
        self.canvas_height = 1.0  # height Gl canvas vertical size
        self.left = -1.0  # left limit of object space window
        self.right = 11.0  # right limit of object space window
        self.bottom = -1.0  # bottom limit of object space window
        self.top = 11.0  # top limit of object space window

        self.curMouseAction = 'SELECTION'  # UNDEFINED, SELECTION, COLLECTION
        self.collector = GeoCollector()  # Collector of entities on canvas

        # mouse button that was pressed
        # (QCore.Qt.LeftButton, QCore.Qt.RightButton QCore.Qt.MidButton)
        self.mouseButton = QtCore.Qt.NoButton
        self.mousebuttonPressed = False  # if true, mouse button is pressed

        # QPoint is a Qt class that defines a point in a plane
        self.pt0W = QtCore.QPointF(0.0, 0.0)  # first point to calculate dist
        self.pt0 = QtCore.QPointF(0.0, 0.0)  # first mouse position
        self.pt1 = QtCore.QPointF(0.0, 0.0)  # current mouse position
        self.pickTolFac = 0.01  # factor for pick tolerance
        self.mouseMoveTol = 2  # tolerance for mouse move

        # Pressed key properties
        self.shiftKeyPressed = False
        self.controlKeyPressed = False

        self.grid = Grid()  # Background modeling grid
        self.viewGrid = False  # if true , grid is on
        self.gridDsp = 0  # GL list index for grid display
        self.updatedGridDsp = False  # if true, grid display is updated

        # Defined colors
        self.colorCollecting = [1.00, 0.00, 0.00]  # red
        self.colorsegment = [0.00, 0.00, 0.00]  # black
        self.colorVertex = [0.00, 0.00, 0.50]  # dark blue
        self.colorSelection = [1.00, 0.00, 0.00]  # red
        self.colorGrid = [0.00, 0.00, 0.00]  # black
        self.colorSdvPoint = [0.00, 0.00, 0.50]  # dark blue
        self.colorPatcheSelection = [1.00, 0.75, 0.75]  # light red
        self.colorPatch = [0.50, 0.75, 0.50]  # medium green
        self.colorHole = [1.00, 1.00, 1.00]  # White
        self.colorHoleSelection = [0.75, 0.75, 0.75]  # light gray
        self.colorhe = [0.0, 0.0, 0.0]  # black
        self.colorEntity_1 = [0.00, 0.00, 1.00]  # blue
        self.colorEntity_2 = [1, 0.3, 0]  # OrangeRed

        self.panmove_flag = False  # flag for panmove
        self.tempPanPoint = []  # handle to panmove event
        self.prop_disp = False  # if true , prop_disp is on

    def setView(self, _view):
        self.view = _view

    def getView(self):
        return self.view

    def resetViewDisplay(self):
        if self.view is None:
            return
        self.updatedDsp = False
        self.update()

    def setMouseAction(self, _action):

        if self.curMouseAction == _action:
            return

        if _action == 'SELECTION':
            self.curMouseAction = 'SELECTION'
            self.collector.reset()

        if _action == 'COLLECTION':
            self.curMouseAction = 'COLLECTION'
            self.collector.reset()

        self.update()

    def setGeoType(self, _type):
        if ((self.curMouseAction == 'COLLECTION') and
                (self.collector.getGeoType() == _type)):
            return
        self.collector.reset()
        self.collector.setGeoType(_type)
        self.update()

    def setGridSnap(self, _viewGrid, _isSnapOn, _dx, _dy):
        self.grid.setSnapData(_isSnapOn, _dx, _dy)
        self.viewGrid = _viewGrid
        self.updatedGridDsp = False
        self.update()

    def getGridSnapInfo(self, _dx, _dy):
        _dx, _dy = self.grid.getGridSpace()
        return self.grid.getSnapInfo(), _dx, _dy

    def setGridSnapData(self, viewGrid, _isSnapOn, _dx,  _dy):
        self.grid.setSnapData(_isSnapOn, _dx, _dy)
        self.viewGrid = viewGrid
        self.updatedGridDsp = False
        self.update()

    def delSelectedEntities(self):
        if not ((self.view is None) and (self.view.isEmpty())):
            self.hecontroller.delSelectedEntities()
            self.updatedDsp = False
            self.update()

    def Undo(self):
        if not ((self.view is None) and (self.view.isEmpty())):
            self.hecontroller.undo()
            self.updatedDsp = False
            self.update()

    def Redo(self):
        if not ((self.view is None) and (self.view.isEmpty())):
            self.hecontroller.redo()
            self.updatedDsp = False
            self.update()

    def saveFile(self, _filename):
        self.hecontroller.saveFile(_filename)

    def openFile(self, _filename):
        self.hecontroller.openFile(_filename)
        self.updatedDsp = False
        self.fitWorldToViewport()

    def setAttribute(self, _name):
        self.hecontroller.setAttribute(_name)
        self.updatedDsp = False
        self.update()

    def unSetAttribute(self, _name):
        self.hecontroller.unSetAttribute(_name)
        self.updatedDsp = False
        self.update()

    def saveAtribute(self, _name, _values):
        self.hecontroller.saveAtribute(_name, _values)
        self.updatedDsp = False
        self.update()

    def delAttribute(self, _name, _cbox):
        self.hecontroller.removeAttribute(_name, _cbox)
        self.updatedDsp = False
        self.update()

    def createPatch(self):
        if (self.view is not None) and not (self.view.isEmpty()):
            self.hecontroller.createPatch()
            self.updatedDsp = False
            self.update()

    def generateMesh(self, _mesh_type, _shape_type, _elem_type, _diag_type, _flag):
        self.hecontroller.generateMesh(
            _mesh_type, _shape_type, _elem_type, _diag_type, _flag)
        self.updatedDsp = False
        self.update()

    def delMesh(self):
        self.hecontroller.delSelectedMesh()
        self.updatedDsp = False
        self.update()

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # --------------------CANVAS PREDEFINED SLOTS--------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)  # set white background color
        glClear(GL_COLOR_BUFFER_BIT)  # clear window

    def resizeGL(self, _width, _height):

        # Avoid division by zero
        if _width == 0:
            _width = 1

        # store GL canvas sizes in object properties
        self.canvas_widht = _width
        self.canvas_height = _height

        # Setup world space window limits based on model bounding box
        if (self.view is None) and (self.view.isEmpty()):
            self.scaleWorldWindow(1.0)
        else:
            self.left, self.right, self.bottom, self.top = self.view.getBoundBox()
            self.scaleWorldWindow(1.1)

        # Setup the viewport to canvas dimesions
        glViewport(0, 0, self.canvas_widht, self.canvas_height)

        # Reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish the clipping volume by setting up an
        # orthographic projection
        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)

        # Setup display model in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.updatedDsp = False
        self.update()

    def paintGL(self):

        # clear the buffer with the current color
        glClear(GL_COLOR_BUFFER_BIT)

        # Display view (if there is one)
        if (self.view is not None) and not(self.view.isEmpty()):
            if not self.updatedDsp:
                if self.viewDsp > 0:
                    glDeleteLists(self.viewDsp, 1)
                self.viewDsp = self.makeDisplayView()

            if self.viewDsp > 0:
                glCallList(self.viewDsp)
                self.updatedDsp = True

        # Display grid (if it is visible)
        if self.viewGrid:
            if not self.updatedGridDsp:
                if self.gridDsp > 0:
                    glDeleteLists(self.gridDsp, 1)
                self.gridDsp = self.makeDisplayGrid()

            if self.gridDsp > 0:
                glCallList(self.gridDsp)
                self.updatedGridDsp = True

        if self.curMouseAction == 'SELECTION' and not self.panmove_flag:
            # Check to see whether there is selection fence and,
            # if that is the case, draw it
            col_fence = self.drawSelectionFence()
            if col_fence > 0:
                glCallList(col_fence)
                glDeleteLists(col_fence, 1)
        elif self.curMouseAction == 'COLLECTION':
            # Check to see whether there is a segment being collected and,
            # if that is the case, draw it
            col_segment = self.drawCollectedsegment()
            if col_segment > 0:
                glCallList(col_segment)
                glDeleteLists(col_segment, 1)

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # -----------------------DISPLAY FUNCTIONS-----------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    def makeDisplayView(self):
        if (self.view is None) or (self.view.isEmpty()):
            return 0

        list = glGenLists(1)
        glNewList(list, GL_COMPILE)

        # get patches
        patches = self.view.getPatches()

        symbols = []  # list of symbols to be drawn later

        # scale for attributes symbols
        scale = max(0.02*(self.top-self.bottom), 0.02*(self.right-self.left))

        # draw patches
        for i in range(0, len(patches)):

            if patches[i].isDeleted:
                if patches[i].isSelected():
                    glColor3d(self.colorHoleSelection[0], self.colorHoleSelection[1],
                              self.colorHoleSelection[2])
                else:
                    glColor3d(self.colorHole[0], self.colorHole[1],
                              self.colorHole[2])
            else:
                material = False
                if len(patches[i].attributes) > 0:
                    for att in patches[i].attributes:
                        if att['type'] == "Material":
                            attColor = att['properties']['Color']
                            glColor3d(attColor[0]/255,
                                      attColor[1]/255, attColor[2]/255)
                            material = True
                        else:
                            symbol = AttribSymbols.getSymbol(
                                att, scale, _patch=patches[i])
                            symbols.append(symbol)

                if not material:
                    glColor3d(self.colorPatch[0],
                              self.colorPatch[1],
                              self.colorPatch[2])

                if patches[i].isSelected():
                    glColor3d(self.colorPatcheSelection[0],
                              self.colorPatcheSelection[1],
                              self.colorPatcheSelection[2])

            pts = patches[i].getPoints()
            triangs = Tesselation.tessellate(pts)
            for j in range(0, len(triangs)):
                glBegin(GL_TRIANGLES)
                glVertex2d(pts[triangs[j][0]].getX(),
                           pts[triangs[j][0]].getY())
                glVertex2d(pts[triangs[j][1]].getX(),
                           pts[triangs[j][1]].getY())
                glVertex2d(pts[triangs[j][2]].getX(),
                           pts[triangs[j][2]].getY())
                glEnd()

            if not patches[i].isDeleted:
                mesh = patches[i].mesh
                if mesh is not None:
                    model = mesh.model
                    mesh_segments = model.segments

                    # Draw mesh segments
                    glLineWidth(0.5)
                    for i in range(0, len(mesh_segments)):

                        # Display segments lines
                        Pts = mesh_segments[i].getPointsToDraw()
                        if mesh_segments[i].isSelected():
                            glColor3d(self.colorSelection[0],
                                      self.colorSelection[1], self.colorSelection[2])
                        else:
                            glColor3d(self.colorsegment[0],
                                      self.colorsegment[1], self.colorsegment[2])

                        glBegin(GL_LINE_STRIP)

                        for j in range(0, len(Pts)):
                            glVertex2d(Pts[j].getX(), Pts[j].getY())
                        glEnd()

        # Draw segments
        glLineWidth(0.5)
        segments = self.view.getSegments()
        for i in range(0, len(segments)):

            # Display segments lines
            Pts = segments[i].getPointsToDraw()
            if segments[i].isSelected():
                glColor3d(self.colorSelection[0],
                          self.colorSelection[1], self.colorSelection[2])
            else:
                glColor3d(self.colorsegment[0],
                          self.colorsegment[1], self.colorsegment[2])

            glBegin(GL_LINE_STRIP)

            for j in range(0, len(Pts)):
                glVertex2d(Pts[j].getX(), Pts[j].getY())
            glEnd()

            # get segment attributes
            attributes = segments[i].attributes
            for att in attributes:
                symbol = AttribSymbols.getSymbol(att, scale, _seg=segments[i])

                if symbol['time'] == 'before':
                    self.drawSymbol(symbol)
                else:
                    symbols.append(symbol)

        # Draw  points
        points = self.view.getPoints()
        for i in range(0, len(points)):

            attributes = points[i].attributes
            for att in attributes:
                symbol = AttribSymbols.getSymbol(att, scale, _pt=points[i])

                if symbol['time'] == 'before':
                    self.drawSymbol(symbol)
                else:
                    symbols.append(symbol)

            glPointSize(4.0)
            if points[i].isSelected():
                glColor3d(self.colorSelection[0],
                          self.colorSelection[1], self.colorSelection[2])
            else:
                glColor3d(self.colorVertex[0],
                          self.colorVertex[1], self.colorVertex[2])

            glBegin(GL_POINTS)
            glVertex2d(points[i].getX(), points[i].getY())
            glEnd()

        # draws remaining symbols
        for symbol in symbols:
            self.drawSymbol(symbol)

        glEndList()
        return list

    def makeDisplayGrid(self):
        oX = 0.0
        oY = 0.0
        x = self.left
        y = self.bottom
        gridX, gridY = self.grid.getGridSpace()

        #  treatment for multiple zoom out
        if ((self.right - self.left)/gridX) > 150 or ((self.top - self.bottom)/gridY) > 150:
            return 0

        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glColor3d(self.colorGrid[0],
                  self.colorGrid[1], self.colorGrid[2])

        # Display grid points
        glPointSize(1.0)
        glBegin(GL_POINTS)
        x = oX - (int((oX - self.left) / gridX) * gridX) - gridX
        while x <= self.right:
            y = oY - (int((oY - self.bottom) / gridY) * gridY) - gridY
            while y <= self.top:
                glVertex2d(x, y)
                y += gridY
            x += gridX
        glEnd()

        # Display crossed lines at origin
        glLineWidth(0.5)
        glBegin(GL_LINES)
        x = oX - gridX * 0.5
        y = oY
        glVertex2d(x, y)
        x = oX + gridX * 0.5
        y = oY
        glVertex2d(x, y)
        x = oX
        y = oY - gridY * 0.5
        glVertex2d(x, y)
        x = oX
        y = oY + gridY * 0.5
        glVertex2d(x, y)
        glEnd()

        glEndList()
        return list

    def drawSymbol(self, _symbol):

        lines = _symbol['lines']
        triangles = _symbol['triangles']
        squares = _symbol['squares']
        circles = _symbol['circles']
        points = _symbol['points']

        if len(_symbol['colors']) > 0:
            color = _symbol['colors'][-1]
        else:
            color = None

        if color is not None:
            glColor3d(color[0]/255, color[1]/255, color[2]/255)

        # draw attribute lines
        glLineWidth(0.5)

        for line in lines:
            glBegin(GL_LINE_STRIP)
            for pt in line:
                glVertex2d(pt.getX(), pt.getY())
            glEnd()

        # draw attribute triangles
        for tr in triangles:
            glBegin(GL_TRIANGLES)
            for pt in tr:
                glVertex2d(pt.getX(), pt.getY())
            glEnd()

        for circ in circles:
            glBegin(GL_LINE_STRIP)
            for pt in circ:
                glVertex2d(pt.getX(), pt.getY())
            glEnd()

        # draw attribute squares
        for sq in squares:
            glBegin(GL_QUADS)
            for pt in sq:
                glVertex2d(pt.getX(), pt.getY())
            glEnd()

        # draw attribute points
        for pt in points:
            glPointSize(4.0)
            glBegin(GL_POINTS)
            glVertex2d(pt.getX(), pt.getY())
            glEnd()

    def drawSelectionFence(self):
        # It is assumed that the current mouse action is for segment selection
        # Only draw a fence if mouse button is presse
        if not self.mousebuttonPressed:
            return 0

        # If current mouse point is in the same position of initial mouse point
        # do not display anything
        if (self.pt0.x() == self.pt1.x()
                and self.pt0.y() == self.pt1.y()):
            return 0

        # If there is no model or it is empty, do nothing
        if ((self.view is None) or self.view.isEmpty()):
            return 0

        # Display a fence from initial mouse point to current mouse point
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glLineWidth(0.5)
        glColor3d(self.colorSelection[0],
                  self.colorSelection[1], self.colorSelection[2])
        glBegin(GL_LINE_STRIP)
        pt0W = self.convertPtCoordsToUniverse(self.pt0)
        pt1W = self.convertPtCoordsToUniverse(self.pt1)
        glVertex2d(pt0W.x(), pt0W.y())
        glVertex2d(pt1W.x(), pt0W.y())
        glVertex2d(pt1W.x(), pt1W.y())
        glVertex2d(pt0W.x(), pt1W.y())
        glVertex2d(pt0W.x(), pt0W.y())
        glEnd()

        glEndList()
        return list

    def drawCollectedsegment(self):
        # It is assumed that the current mouse
        # action if for segment collection
        if not(self.collector.isActive()
                or self.collector.isCollecting()):
            return 0

        list = glGenLists(1)
        glNewList(list, GL_COMPILE)

        glColor3d(self.colorCollecting[0],
                  self.colorCollecting[1], self.colorCollecting[2])

        # Display lines of segment being collected
        glLineWidth(0.5)
        glBegin(GL_LINE_STRIP)

        pts = self.collector.getDrawPoints()
        for i in range(0, len(pts)):
            glVertex2d(pts[i].getX(), pts[i].getY())
        glEnd()

        # Display control points of segment being collected
        glPointSize(4.0)
        glBegin(GL_POINTS)
        ctrl_pts = self.collector.getPoints()
        for i in range(0, len(ctrl_pts)):
            glVertex2d(ctrl_pts[i].getX(), ctrl_pts[i].getY())
        glEnd()
        glEndList()
        return list

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # -----------FUNCTIONS TO MANAGE VISUALIZATION WINDOW LIMITS-----------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    def fitWorldToViewport(self):
        if self.view is None:
            return
        self.left, self.right, self.bottom, self.top = self.view.getBoundBox()
        self.scaleWorldWindow(1.10)

    def scaleWorldWindow(self, _scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.canvas_height / self.canvas_widht  # viewport distortion ratio

        # Get current window center.
        cx = (self.left + self.right) / 2.0  # window center coord x
        cy = (self.bottom + self.top) / 2.0  # window center coord y

        # Set new window sizes based on scaling factor
        sizex = (self.right - self.left) * _scaleFac  # window size x
        sizey = (self.top - self.bottom) * _scaleFac  # window size y

        # Adjust window to keep the same aspect ratio of the viewport

        # Avoid division by zero
        if sizex == 0:
            sizex = 1
        if vpr == 0:
            vpr = 1

        if (sizey / sizex) > vpr:
            sizex = sizey / vpr
        elif (sizey / sizex) < vpr:
            sizey = sizex * vpr

        self.left = cx - (sizex * 0.5)
        self.right = cx + (sizex * 0.5)
        self.bottom = cy - (sizey * 0.5)
        self.top = cy + (sizey * 0.5)

        # Reset flag for updated grid display
        self.updatedGridDsp = False

        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)
        self.updatedDsp = False
        self.update()

    def panWorldWindow(self, _panFacX, _panFacY):
        # Compute pan distances in horizontal and vertical directions.
        panX = (self.right - self.left) * _panFacX
        panY = (self.top - self.bottom) * _panFacY

        # Shift current window.
        x = panX - (self.right - self.left)
        y = panY - (self.top - self.bottom)
        self.right = self.right + x
        self.left = self.left + x
        self.top = self.top + y
        self.bottom = self.bottom + y

        # Reset flag for updated grid display
        self.updatedGridDsp = False

        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)
        self.updatedDsp = False
        self.update()

    def zoomIn(self):
        if self.view is None:
            return
        self.scaleWorldWindow(0.9)

    def zoomOut(self):
        if self.view is None:
            return
        self.scaleWorldWindow(1.1)

    def PanLeft(self):
        if self.view is None:
            return
        self.panWorldWindow(1.1, 1.0)

    def PanRight(self):
        if self.view is None:
            return
        self.panWorldWindow(0.9, 1.0)

    def PanDown(self):
        if self.view is None:
            return
        self.panWorldWindow(1.0, 1.1)

    def PanUp(self):
        if self.view is None:
            return
        self.panWorldWindow(1.0, 0.9)

    def PanMove(self):
        Pt1 = self.convertPtCoordsToUniverse(self.pt1)
        Pt2 = self.convertPtCoordsToUniverse(self.tempPanPoint[0])
        panX = (Pt1.x()-Pt2.x())
        panY = (Pt1.y()-Pt2.y())

        self.tempPanPoint[0] = self.pt1

        self.right = self.right - panX
        self.left = self.left - panX
        self.top = self.top - panY
        self.bottom = self.bottom - panY

        # Reset flag for updated grid display
        self.updatedGridDsp = False

        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)
        self.update()

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.right - self.left  # Universe window horizontal size
        dY = self.top - self.bottom  # Universe window vertical size

        # Origin of canvas raster coordinates it at the left-top corner,
        # while origin of GL canvas floating point coordinates is at
        # left-bottom corner.
        # mX is the distance of point to left universe window limit
        # mY is the distance of point to bottom universe window limit
        mX = _pt.x() * dX / self.canvas_widht
        my = (self.canvas_height - _pt.y()) * dY / self.canvas_height
        x = self.left + mX
        y = self.bottom + my
        return QtCore.QPointF(x, y)

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------MOUSE EVENT SLOTS------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    def mousePressEvent(self, event):

        # Get current mouse position
        self.mousebuttonPressed = True
        self.pt0 = event.pos()
        self.pt1 = event.pos()

        # Convert mouse positions to world coordinates
        pt0W = self.convertPtCoordsToUniverse(self.pt0)
        pt1W = self.convertPtCoordsToUniverse(self.pt1)
        self.mouseButton = event.button()

        # verifies if the Middle button is turned on
        # if it is the case set panmove flag as true
        # and get first point position
        if self.mouseButton == QtCore.Qt.MiddleButton:
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            self.panmove_flag = True
            self.tempPanPoint.append(self.pt0)

        # Treat mouse move event according to current mouse action type
        if self.curMouseAction == 'SELECTION':
            return

        if (self.curMouseAction == 'COLLECTION' and
                self.mouseButton == QtCore.Qt.LeftButton):

            if not self.collector.isActive():
                # In case of left mouse button
                # if not doing any segment collection,
                # start a new segment collection
                self.collector.startGeoCollection()
                max_size = max(abs(self.right-self.left),
                               abs(self.top-self.bottom))
                pick_tol = max_size * self.pickTolFac
                pt0W = self.convertPtCoordsToUniverse(self.pt0)
                xW = pt0W.x()
                yW = pt0W.y()

                # Snap point to grid (if it is visible). Also check for
                # snap-to-grid flag (which will be inverted by control key)
                if self.viewGrid:
                    isSnapOn = self.grid.getSnapInfo()
                    if ((not self.controlKeyPressed and isSnapOn) or
                            (self.controlKeyPressed and not isSnapOn)):
                        xW, yW = self.grid.snapTo(xW, yW)

                if (self.view is not None) and not(self.view.isEmpty()):
                    # Try to attract point to a point
                    check, _x, _y = self.view.snapToPoint(
                        xW,  yW, pick_tol)
                    if check:
                        xW = _x
                        yW = _y
                    else:
                        # Try to attract point to a segment
                        check, _x, _y = self.view.snapToSegment(
                            xW,  yW, pick_tol)
                        if check:
                            xW = _x
                            yW = _y

                # Add point to collected geometry
                if self.collector.getGeoType() == 'POINT':
                    self.hecontroller.insertPoint(Point(xW, yW), 0.01)
                    self.collector.endGeoCollection()
                    self.updatedDsp = False
                    self.update()
                else:
                    self.collector.insertPoint(xW, yW, pick_tol)
                    self.collector.addTempPoint(xW, yW)
                    self.pt0W = QtCore.QPoint(xW, yW)

                    # set text in LineEdit
                    self.Apptools.setFirstLineEditText(xW, yW, self)

            elif ((abs(self.pt0.x() - self.pt1.x()) <= self.mouseMoveTol) and
                  (abs(self.pt0.y() - self.pt1.y()) <= self.mouseMoveTol)):
                max_size = max(abs(self.right-self.left),
                               abs(self.top-self.bottom))
                pick_tol = max_size * self.pickTolFac
                xW = pt1W.x()
                yW = pt1W.y()

                # Snap point to grid (if it is visible). Also check for
                # snap-to-grid flag (which will be inverted by control key)
                if self.viewGrid:
                    isSnapOn = self.grid.getSnapInfo()
                    if ((not self.controlKeyPressed and isSnapOn) or
                            (self.controlKeyPressed and not isSnapOn)):
                        xW, yW = self.grid.snapTo(xW, yW)

                if (self.view) and not(self.view.isEmpty()):
                    # Try to attract point to a point
                    check, _x, _y = self.view.snapToPoint(
                        xW,  yW, pick_tol)
                    if check:
                        xW = _x
                        yW = _y
                    else:
                        # Try to attract point to a segment
                        check, _x, _y = self.view.snapToSegment(
                            xW,  yW, pick_tol)
                        if check:
                            xW = _x
                            yW = _y

                # try to attract point to current segment
                check, _x, _y = self.collector.SnaptoCurrentSegment(
                    xW,  yW, pick_tol)
                if check:
                    xW = _x
                    yW = _y

                # Add point to collected segment
                self.collector.insertPoint(xW, yW, pick_tol)
                self.pt0W = QtCore.QPoint(xW, yW)

                # set text in LineEdit
                self.Apptools.setFirstLineEditText(xW, yW, self)

    def mouseMoveEvent(self, event):

        # Get current mouse position
        self.pt1 = event.pos()
        # Convert current mouse position point to world coordinates
        pt1W = self.convertPtCoordsToUniverse(self.pt1)

        # verifies if the panmove_flag is true and active PanMove event
        if self.panmove_flag:
            self.PanMove()
            if self.curMouseAction == 'COLLECTION':
                self.mouseButton = QtCore.Qt.LeftButton
        else:
            # Line coords text
            self.Apptools.lineXCoords.setText(f'X:  {str(round(pt1W.x(), 3))}')
            self.Apptools.lineYCoords.setText(f'Y:  {str(round(pt1W.y(), 3))}')

        # Treat mouse move event according to current mouse action type
        if self.curMouseAction == 'SELECTION':
            # Disregard mouse move event if left mouse button is not pressed
            if ((self.mouseButton == QtCore.Qt.LeftButton)
                    and self.mousebuttonPressed):
                self.update()
                return

        if self.curMouseAction == 'COLLECTION':
            # Only consider current point if left mouse button was used,
            # if not button pressed, and if current point is not at the
            # same location of button press point.

            if (self.mouseButton == QtCore.Qt.LeftButton
                    and not (self.mousebuttonPressed)):
                if (abs(self.pt0.x() - self.pt1.x()) > self.mouseMoveTol
                        or abs(self.pt0.y() - self.pt1.y()) > self.mouseMoveTol):
                    if self.collector.isCollecting():
                        xW = pt1W.x()
                        yW = pt1W.y()

                        # Snap point to grid (if it is visible). Also check for
                        # Snap-to-grid flag (which will be inverted by control key)
                        if self.viewGrid:
                            isSnapOn = self.grid.getSnapInfo()
                            if ((not self.controlKeyPressed and isSnapOn) or
                                    (self.controlKeyPressed and not isSnapOn)):
                                xW, yW = self.grid.snapTo(xW, yW)

                        max_size = max(abs(self.right-self.left),
                                       abs(self.top-self.bottom))
                        pick_tol = max_size * self.pickTolFac

                        if (self.view) and not(self.view.isEmpty()):

                            # Try to attract point to a point
                            check, _x, _y = self.view.snapToPoint(
                                xW,  yW, pick_tol)
                            if check:
                                xW = _x
                                yW = _y
                            else:
                                # Try to attract point to a segment
                                check, _x, _y = self.view.snapToSegment(
                                    xW,  yW, pick_tol)
                                if check:
                                    xW = _x
                                    yW = _y

                        # try to attract point to current segment
                        check, _x, _y = self.collector.SnaptoCurrentSegment(
                            xW,  yW, pick_tol)
                        if check:
                            xW = _x
                            yW = _y

                        self.Apptools.lineXCoords.setText(
                            f'X:  {str(round(xW, 3))}')
                        self.Apptools.lineYCoords.setText(
                            f'Y:  {str(round(yW, 3))}')

                        # Add point as a temporary point for segment collection
                        self.collector.addTempPoint(xW, yW)
                        dist = round(math.sqrt((self.pt0W.x()-xW)*(self.pt0W.x()-xW) +
                                               (self.pt0W.y()-yW)*(self.pt0W.y()-yW)), 3)

                        # Set text in LenghtLineEdit
                        self.Apptools.lineLenght.setText(
                            f'Lenght: {str(dist)}')

                        # set text in LineEdit
                        self.Apptools.setEndLineEditText(xW, yW, self)
                        self.update()

    def mouseReleaseEvent(self, event):

        self.mousebuttonPressed = False
        # Get current mouse position
        self.pt1 = event.pos()

        # Finish PanMove event
        self.panmove_flag = False
        self.tempPanPoint = []
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Convert mouse positions to world coordinates
        pt0W = self.convertPtCoordsToUniverse(self.pt0)
        pt1W = self.convertPtCoordsToUniverse(self.pt1)

        # Treat mouse release event according to current mouse action type
        if self.curMouseAction == 'SELECTION':
            if self.mouseButton == QtCore.Qt.LeftButton:
                # If there is a view and it is not empty
                if not (self.view is None and self.view.isEmpty()):
                    # If current mouse point is in the same position
                    # of inital mouse point,
                    # consider a mouse pick selection.
                    # Otherwise, consider a mouse fence selection
                    if ((abs(self.pt0.x() - self.pt1.x()) <= self.mouseMoveTol) and
                            (abs(self.pt0.y() - self.pt1.y()) <= self.mouseMoveTol)):
                        max_size = max(abs(self.right-self.left),
                                       abs(self.top-self.bottom))
                        pick_tol = max_size * self.pickTolFac
                        self.hecontroller.selectPick(
                            pt1W.x(), pt1W.y(), pick_tol, self.shiftKeyPressed)
                    else:
                        xmin = min(pt0W.x(), pt1W.x())
                        xmax = max(pt0W.x(), pt1W.x())
                        ymin = min(pt0W.y(), pt1W.y())
                        ymax = max(pt0W.y(), pt1W.y())
                        self.hecontroller.selectFence(
                            xmin, xmax, ymin, ymax, self.shiftKeyPressed)
                self.updatedDsp = False
                self.update()

        if self.curMouseAction == 'COLLECTION':

            # clear Lenght line edit
            self.Apptools.lineLenght.clear()

            # Check for end of segment collection, which occurs in two situations:
            # (a) If left mouse button was used, and current collected segment has
            #     a limit in the number of points, verify whether current point
            #     finishes collection of current segment.
            # (b) If right mouse button was used, and current collected segment has
            #     no limit in the number of points, verify whether previously
            #     collected points can finish collection of current segment
            endCollection = False

            if self.mouseButton == QtCore.Qt.RightButton:
                # set enable and clear line Edits
                self.Apptools.setEnableLineEdits(self)

            if self.mouseButton == QtCore.Qt.LeftButton:
                if not self.collector.isUnlimited():
                    if self.collector.hasFinished():
                        endCollection = True
            elif self.mouseButton == QtCore.Qt.RightButton:
                if self.collector.isUnlimited() and self.collector.hasFinished():
                    endCollection = True
                else:
                    # If right mouse button was used, segment has
                    # an unlimited number of points, and
                    # previously collected points cannot finish
                    # collection of segment, reset current
                    # segment collection
                    self.collector.reset()
                    self.update()

            if endCollection:
                segment = self.collector.getCollectedGeo()
                max_size = max(abs(self.right-self.left),
                               abs(self.top-self.bottom))
                pick_tol = max_size * self.pickTolFac

                try:
                    self.hecontroller.insertSegment(segment, 0.01)
                except:
                    msg = QMessageBox(self.Apptools)
                    msg.setWindowTitle('Error')
                    msg.setText('It was not possible to add the segment')
                    msg.exec()

                self.collector.endGeoCollection()
                self.updatedDsp = False
                self.update()

                # set enable and clear line Edits
                self.Apptools.setEnableLineEdits(self)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------KEYBOARD EVENT SLOTS---------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    def keyPressEvent(self, event):
        self.shiftKeyPressed = (event.key() == QtCore.Qt.Key_Shift)
        self.controlKeyPressed = (event.key() == QtCore.Qt.Key_Control)

    def keyReleaseEvent(self, event):
        self.shiftKeyPressed = False
        self.controlKeyPressed = False
