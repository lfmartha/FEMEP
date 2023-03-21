from geometry.point import Point
from geometry.curves.line import Line
from geometry.curves.polyline import Polyline
from geometry.curves.cubicspline import CubicSpline
from geometry.curves.circle import Circle
from geometry.curves.circlearc import CircleArc
from geometry.curves.ellipse import Ellipse
from geometry.curves.ellipsearc import EllipseArc
import math


class GeoCollector:
    def __init__(self):
        self.geo = None
        self.prevPt = Point(0.0, 0.0)
        self.tempPt = Point(0.0, 0.0)
        self.geoType = None  # POINT, LINE, POLYLINE...

    def __del__(self):
        if self.geo is not None:
            del self.geo

    def setGeoType(self, _type):
        self.geoType = _type

    def getGeoType(self):
        return self.geoType

    def startGeoCollection(self):
        if self.geo is not None:
            del self.geo

        if self.geoType == 'LINE':
            self.geo = Line()
        elif self.geoType == 'POLYLINE':
            self.geo = Polyline()
        elif self.geoType == 'CUBICSPLINE':
            self.geo = CubicSpline()
        elif self.geoType == 'CIRCLE':
            self.geo = Circle()
        elif self.geoType == 'CIRCLEARC':
            self.geo = CircleArc()
        elif self.geoType == 'ELLIPSE':
            self.geo = Ellipse()
        elif self.geoType == 'ELLIPSEARC':
            self.geo = EllipseArc()

    def endGeoCollection(self):
        self.geo = None

    def isActive(self):
        if self.geo is not None:
            return True
        return False

    def isCollecting(self):
        if self.geo is not None:
            if self.geo.getNumberOfCtrlPoints() > 0:
                return True
        return False

    def hasFinished(self):
        if self.geo is not None:
            if self.geo.isPossible():
                return True
        return False

    def isUnlimited(self):
        if self.geo is not None:
            if self.geo.isUnlimited():
                return True
        return False

    def insertPoint(self, _x, _y, _LenAndAng, _tol):
        if self.isCollecting():
            if (abs(_x - self.prevPt.getX()) <= _tol and
                    abs(_y - self.prevPt.getY()) <= _tol):
                return 0

        self.geo.addCtrlPoint(_x, _y, _LenAndAng)
        self.prevPt.setCoords(_x, _y)
        return 1

    def addTempPoint(self, _x, _y):
        self.tempPt.setCoords(_x, _y)
        return 1

    def getCollectedGeo(self):
        return self.geo

    def getDrawPoints(self):
        return self.geo.getEquivPolylineCollecting(self.tempPt)

    def getPoints(self):
        return self.geo.getCtrlPoints()

    def getBoundBox(self):
        if self.geo is None:
            return
        return self.geo.getBoundBox()

    def reset(self):
        self.geo = None

    def kill(self):
        if self.geo is not None:
            del self.geo
        del self

    def SnaptoCurrentSegment(self, _x, _y, _tol):

        if not self.geo.isUnlimited():
            return False, _x, _y

        pts = self.geo.getCtrlPoints()

        if len(pts) < 3:
            return False, _x, _y

        snap = False
        dmin = _tol

        for i in range(0, len(pts)):
            pt_x = pts[i].getX()
            pt_y = pts[i].getY()
            d = math.sqrt((_x-pt_x)*(_x-pt_x)+(_y-pt_y)*(_y-pt_y))

            if d < dmin:
                xmin = pt_x
                ymin = pt_y
                dmin = d
                snap = True

        if snap:
            return True, xmin, ymin
        else:
            status, clstPt, dist, t, tangVec = self.geo.closestPoint(_x, _y)
            if not status:
                return False, _x, _y
            if dist < dmin:
                dmin = dist
                xmin = clstPt.getX()
                ymin = clstPt.getY()
                return True, xmin, ymin
            else:
                return False, _x, _y

    def CurrentNumberOfControlPoints(self):
        try:
            NumCtrlPts = self.geo.nPts
        except:
            NumCtrlPts = 0

        return NumCtrlPts

    def updateLineEditValues(self, _x, _y, _LenAndAng):
        v1, v2 = self.geo.updateLineEditValues(_x, _y, _LenAndAng)

        return v1, v2