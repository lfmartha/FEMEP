from geometry.point import Point
import math
from compgeom.compgeom import CompGeom
from geometry.segments.segment import Segment


class Line(Segment):

    def __init__(self, _pt1=None, _pt2=None):
        self.pt1 = _pt1
        self.pt2 = _pt2
        self.nPts = 0
        self.edge = None
        self.attributes = []

        if _pt1 is not None:
            self.nPts += 1

        if _pt2 is not None:
            self.nPts += 1

    def addPoint(self, _x, _y):
        if self.nPts == 0:
            self.pt1 = Point(_x, _y)
            self.nPts += 1
        elif self.nPts == 1:
            self.pt2 = Point(_x, _y)
            self.nPts += 1

    def getNumberOfPoints(self):
        return self.nPts

    def getPoint(self, _t):
        vx = self.pt2.getX() - self.pt1.getX()
        vy = self.pt2.getY() - self.pt1.getY()
        if _t < 0:
            xOn = self.pt1.getX()
            yOn = self.pt1.getY()
        elif _t > 1:
            xOn = self.pt2.getX()
            yOn = self.pt2.getY()
        else:
            xOn = self.pt1.getX() + _t * vx
            yOn = self.pt1.getY() + _t * vy
        return Point(xOn, yOn)

    def isPossible(self):
        if self.nPts < 2:
            return False
        return True

    def getPoints(self):
        tempPts = []
        if self.nPts == 1:
            tempPts.append(self.pt1)
            return tempPts

        tempPts.append(self.pt1)
        tempPts.append(self.pt2)
        return tempPts

    def getPointsToDraw(self):
        tempPts = []
        tempPts.append(self.pt1)
        tempPts.append(self.pt2)
        return tempPts

    def getPointsToDrawPt(self, _pt):
        tempPts = []
        tempPts.append(self.pt1)
        if self.nPts == 2:
            tempPts.append(self.pt2)
        elif self.nPts == 1:
            tempPts.append(_pt)
        return tempPts

    def setInitPoint(self, _pt):
        self.pt1 = _pt

    def setEndPoint(self,_pt):
        self.pt2 = _pt

    def closestPoint(self, _x, _y):
        vx = self.pt2.getX() - self.pt1.getX()
        vy = self.pt2.getY() - self.pt1.getY()
        t = (vx*(_x - self.pt1.getX()) + vy *
             (_y - self.pt1.getY())) / (vx*vx + vy*vy)

        if t < 0.0:
            xOn = self.pt1.getX()
            yOn = self.pt1.getY()
        elif t > 1.0:
            xOn = self.pt2.getX()
            yOn = self.pt2.getY()
        else:
            xOn = self.pt1.getX() + t * vx
            yOn = self.pt1.getY() + t * vy

        dist = math.sqrt((xOn - _x)*(xOn - _x)+(yOn - _y)*(yOn - _y))
        return xOn, yOn, dist

    def getBoundBox(self):

        xmax = max(self.pt1.getX(), self.pt2.getX())
        xmin = min(self.pt1.getX(), self.pt2.getX())
        ymax = max(self.pt1.getY(), self.pt2.getY())
        ymin = min(self.pt1.getY(), self.pt2.getY())
        return xmin, xmax, ymin, ymax

    def getType(self):
        return 'LINE'

    def isUnlimited(self):
        return False

    def getXinit(self):
        return self.pt1.getX()

    def getYinit(self):
        return self.pt1.getY()

    def getXend(self):
        return self.pt2.getX()

    def getYend(self):
        return self.pt2.getY()

    def boundIntegral(self):
        return (self.pt1.getX()*self.pt2.getY() - self.pt2.getX()*self.pt1.getY())*0.5

    def length(self, _t0, _t1):
        p1 = self.getPoint(_t0)
        p2 = self.getPoint(_t1)
        len = math.sqrt((p2.getX() - p1.getX()) *
                        (p2.getX() - p1.getX()) +
                        (p2.getY() - p1.getY()) *
                        (p2.getY() - p1.getY()))

        return len

    def tangent(self, _t):
        pts = self.getPoints()
        tan = pts[1] - pts[0]
        tan = Point.normalize(tan)

        return tan

    def curvature(self, _t):
        return 0.0

    def selfIntersect(self):
        return False, None, None

    def clone(self):
        myClone = Line(self.pt1, self.pt2)
        return myClone

    def splitSegment(self, _t, _pt):
        if _t <= Segment.PARAM_TOL:
            _segment1 = None
            _segment2 = self
            return _segment1, _segment2

        if 1.0 - _t <= Segment.PARAM_TOL:
            _segment1 = self
            _segment2 = None
            return _segment1, _segment2

        _segment1 = Line(self.pt1, _pt)
        _segment2 = Line(_pt, self.pt2)

        return _segment1, _segment2

    def split(self, _params, _pts):
        seg2 = self.clone()
        segments = []

        for i in range(0, len(_params)):
            seg1, seg2 = seg2.splitSegment(_params[i], _pts[i])
            segments.append(seg1)

            # update the remaining parameters
            for j in range(i+1, len(_params)):
                _params[j] = (_params[j] - _params[i])/(1-_params[i])

        segments.append(seg2)

        return segments

    def intersectPoint(self, _pt, _tol):
        pts = self.getPoints()
        dist, pi, t = CompGeom.getClosestPointSegment(pts[0], pts[1], _pt)

        if dist <= _tol:
            return True, t, pi

        return False, t, pi

    def intersectSegment(self, _segment):

        poly = _segment.getPoints()
        if _segment.getType() == 'LINE':
            return CompGeom.computeLineIntersection(self.pt1, self.pt2, poly[0], poly[1])
        elif _segment.getType() == 'POLYLINE':
            pts = self.getPoints()
            return CompGeom.computePolyPolyIntersection(pts, poly)

    def isEqual(self, _segment, _tol):

        if _segment.getType() == 'LINE':

            pts1 = self.getPoints()
            pts2 = _segment.getPoints()
            tol = Point(_tol, _tol)

            if Point.equal(pts1[0], pts2[0], tol):
                if Point.equal(pts1[1], pts2[1], tol):
                    return True
            elif Point.equal(pts1[1], pts2[0], tol):
                if Point.equal(pts1[0], pts2[1], tol):
                    return True
            return False

        else:
            return _segment.isEqual(self, _tol)

    def ray(self, _pt):
        x = _pt.getX()
        y = _pt.getY()

        if self.pt1.getY() == self.pt2.getY():  # discard horizontal line
            return 0.0

        if self.pt1.getY() > y and self.pt2.getY() > y:  # discard line above ray
            return 0.0

        if self.pt1.getY() < y and self.pt2.getY() < y:  # Discard line below ray
            return 0.0

        if self.pt1.getX() < x and self.pt2.getX() < x:  # discard line to the left of point
            return 0.0

        if self.pt1.getY() == y:  # ray passes at first line point
            if self.pt1.getX() > x and self.pt2.getY() > y:
                # Intersects if first point is to the right of given point
                # and second point is above.
                return 1
        else:
            if self.pt2.getY() == y:  # ray passes at second point
                if self.pt2.getX() > x and self.pt1.getY() > y:
                    # Intersects if first point is to the right of given point
                    # and second point is above.
                    return 1
            else:  # ray passes with first and second points
                if self.pt1.getX() > x and self.pt2.getX() > x:
                    # Intersects if first point is to the right of given point
                    # and second point is above.
                    return 1
                else:
                    # Compute x coordinate of intersection of ray with line segment
                    dx = self.pt1.getX() - self.pt2.getX()
                    xc = self.pt1.getX()

                    if dx != 0:
                        xc += (y - self.pt1.getY())*dx / \
                            (self.pt1.getY() - self.pt2.getY())

                    if xc > x:
                        # Intersects if first point is to the right of given point
                        # and second point is above.
                        return 1

        return 0.0
