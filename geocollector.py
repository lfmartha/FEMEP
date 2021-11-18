from geometry.point import Point
from geometry.segments.line import Line
from geometry.segments.polyline import Polyline
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

    def endGeoCollection(self):
        self.geo = None

    def isActive(self):
        if self.geo is not None:
            return True
        return False

    def isCollecting(self):
        if self.geo is not None:
            if self.geo.getNumberOfPoints() > 0:
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

    def insertPoint(self, _x, _y, _tol):
        if self.isCollecting():
            if (abs(_x - self.prevPt.getX()) <= _tol and
                    abs(_y - self.prevPt.getY()) <= _tol):
                return 0

        self.geo.addPoint(_x, _y)
        self.prevPt.setCoords(_x, _y)
        return 1

    def addTempPoint(self, _x, _y):
        self.tempPt.setCoords(_x, _y)
        return 1

    def getCollectedGeo(self):
        return self.geo

    def getDrawPoints(self):
        return self.geo.getPointsToDrawPt(self.tempPt)

    def getPoints(self):
        return self.geo.getPoints()

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

        pts = self.geo.getPoints()

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
            xC, yC, dist = self.geo.closestPoint(_x, _y)

            if dist < dmin:
                dmin = dist
                xmin = xC
                ymin = yC
                return True, xmin, ymin
            else:
                return False, _x, _y
