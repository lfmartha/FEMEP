from geometry.point import Point
from geometry.segments.segment import Segment
from geometry.segments.line import Line
import math
from compgeom.compgeom import CompGeom


class Polyline(Segment):
    def __init__(self, _pts=None):
        self.pts = _pts
        if self.pts is None:
            self.pts = []
        self.nPts = 0
        self.edge = None
        self.attributes = []

    def addPoint(self, _x, _y):
        self.pts.append(Point(_x, _y))
        self.nPts += 1

    def getNumberOfPoints(self):
        return self.nPts

    def getPoint(self, _t):

        if _t <= 0:
            return Point(self.pts[0].getX(), self.pts[0].getY())

        if _t >= 1.0:
            return Point(self.pts[-1].getX(), self.pts[-1].getY())

        length = self.length(0, 1)
        s = _t*length
        loc_t = 1.0
        prev_id = 0
        next_id = 0
        length = 0

        for i in range(1, len(self.pts)):
            prev_id = i - 1
            next_id = i
            dist = math.sqrt((self.pts[i].getX() - self.pts[i - 1].getX()) *
                             (self.pts[i].getX() - self.pts[i - 1].getX()) +
                             (self.pts[i].getY() - self.pts[i - 1].getY()) *
                             (self.pts[i].getY() - self.pts[i - 1].getY()))

            if (length + dist) >= s:
                loc_t = (s - length) / dist
                break

            length += dist

        x = self.pts[prev_id].getX() + loc_t * \
            (self.pts[next_id].getX() - self.pts[prev_id].getX())
        y = self.pts[prev_id].getY() + loc_t * \
            (self.pts[next_id].getY() - self.pts[prev_id].getY())

        return Point(x, y)

    def isPossible(self):
        if self.nPts < 2:
            return False

        return True

    def getPoints(self):
        return self.pts

    def getPointsToDraw(self):
        return self.pts

    def getPointsToDrawPt(self, _pt):
        tempPts = []
        for i in range(0, self.nPts):
            tempPts.append(self.pts[i])

        tempPts.append(_pt)
        return tempPts

    def setInitPoint(self, _pt):
        self.pts[0] = _pt

    def setEndPoint(self, _pt):
        self.pts[-1] = _pt

    def closestPoint(self, _x, _y):

        aux = Line(self.pts[0], self.pts[1])
        x, y, d = aux.closestPoint(_x, _y)
        xOn = x
        yOn = y

        dmin = d

        for i in range(2, len(self.pts)):
            aux = Line(self.pts[i - 1], self.pts[i])
            x, y, d = aux.closestPoint(_x, _y)

            if d < dmin:
                xOn = x
                yOn = y
                dmin = d

        return xOn, yOn, dmin

    def getBoundBox(self):
        x = []
        y = []
        for point in self.pts:
            x.append(point.getX())
            y.append(point.getY())

        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)

        return xmin, xmax, ymin, ymax

    def getType(self):
        return 'POLYLINE'

    def isUnlimited(self):
        return True

    def getXinit(self):
        return self.pts[0].getX()

    def getYinit(self):
        return self.pts[0].getY()

    def getXend(self):
        return self.pts[-1].getX()

    def getYend(self):
        return self.pts[-1].getY()

    def boundIntegral(self):
        area = 0

        for i in range(0, len(self.pts)-1):
            pt1 = self.pts[i]
            pt2 = self.pts[i+1]
            area += (pt1.getX())*(pt2.getY()) - (pt2.getX())*(pt1.getY())

        return area*0.5

    def curvature(self, _t):
        return 0.0

    def tangent(self, _t):

        if _t <= 0.0:
            tan = self.pts[1]-self.pts[0]
            tan = Point.normalize(tan)
            return tan

        if _t >= 1.0:
            tan = self.pts[-1]-self.pts[-2]
            tan = Point.normalize(tan)
            return tan

        length = 0.0

        for j in range(1, len(self.pts)):
            length += math.sqrt((self.pts[j].getX()-self.pts[j-1].getX())
                                * (self.pts[j].getX()-self.pts[j-1].getX()) +
                                (self.pts[j].getY()-self.pts[j-1].getY()) *
                                (self.pts[j].getY()-self.pts[j-1].getY()))

        s = _t*length
        prev_id = 0
        next_id = 0

        for i in range(1, len(self.pts)):
            prev_id = i - 1
            next_id = i

            d = math.sqrt((self.pts[i].getX()-self.pts[i-1].getX())
                          * (self.pts[i].getX()-self.pts[i-1].getX()) +
                          (self.pts[i].getY()-self.pts[i-1].getY()) *
                          (self.pts[i].getY()-self.pts[i-1].getY()))

            if length + d >= s:
                break

            length += d

        tan = self.pts[next_id] - self.pts[prev_id]
        tan = Point.normalize(tan)

        return tan

    def selfIntersect(self):
        flag, pts, params = CompGeom.splitSelfIntersected(self.getPoints())
        return flag, pts, params

    def clone(self):
        myClone = Polyline(self.pts)
        return myClone

    def length(self, _t0, _t1):
        L = 0.0
        pts = self.getPoints()
        for i in range(1, len(pts)):
            L += math.sqrt((pts[i].getX()-pts[i-1].getX())*(pts[i].getX()-pts[i-1].getX()) + (
                pts[i].getY()-pts[i-1].getY()) * (pts[i].getY()-pts[i-1].getY()))

        return L*(_t1-_t0)

    def splitSegment(self, _t, _pt):
        if _t <= Segment.PARAM_TOL:
            _segment1 = None
            _segment2 = self
            return _segment1, _segment2

        if 1.0 - _t <= Segment.PARAM_TOL:
            _segment1 = self
            _segment2 = None
            return _segment1, _segment2

        L = self.length(0, 1)
        s = _t*L
        loc_t = 1.0
        prev_id = 0
        next_id = 0
        L = 0.0
        pts = self.getPoints()
        for j in range(1, len(pts)):
            prev_id = j - 1
            next_id = j
            d = math.sqrt((pts[j].getX()-pts[j-1].getX())*(pts[j].getX()-pts[j-1].getX()) + (
                pts[j].getY()-pts[j-1].getY()) * (pts[j].getY()-pts[j-1].getY()))

            if (L+d) >= s:
                loc_t = (s-L)/d
                break
            L += d

        segment1_pts = []
        segment2_pts = []

        for i in range(0, prev_id):
            segment1_pts.append(pts[i])

        # check whether the split point is one of the points of the polyline itself
        if loc_t > Segment.PARAM_TOL:
            segment1_pts.append(pts[prev_id])

        segment1_pts.append(_pt)
        segment2_pts.append(_pt)

        if 1.0 - loc_t > Segment.PARAM_TOL:
            segment2_pts.append(pts[next_id])

        for j in range(next_id+1, len(pts)):
            segment2_pts.append(pts[j])

        _segment1 = Polyline(segment1_pts)

        _segment2 = Polyline(segment2_pts)

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

    def ray(self, _pt):
        x = _pt.getX()
        y = _pt.getY()
        n = len(self.pts)
        ni = 0

        for i in range(0, n-1):
            pt1 = self.pts[i]
            pt2 = self.pts[i+1]

            if pt1.getY() == pt2.getY():  # discard horizontal line
                continue

            if pt1.getY() > y and pt2.getY() > y:  # discard line above ray
                continue

            if pt1.getY() < y and pt2.getY() < y:  # Discard line below ray
                continue

            if pt1.getX() < x and pt2.getX() < x:  # discard line to the left of point
                continue

            if pt1.getY() == y:  # ray passes at first line point
                if pt1.getX() > x and pt2.getY() > y:
                    # Count intersection if first point is to the right of given point
                    # and second point is above.
                    ni += 1
            else:
                if pt2.getY() == y:  # ray passes at second point
                    if pt2.getX() > x and pt1.getY() > y:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                else:  # ray passes with first and second points
                    if pt1.getX() > x and pt2.getX() > x:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                    else:
                        # Compute x coordinate of intersection of ray with line segment
                        dx = pt1.getX() - pt2.getX()
                        xc = pt1.getX()

                        if dx != 0:
                            xc += (y - pt1.getY())*dx / \
                                (pt1.getY() - pt2.getY())

                        if xc > x:
                            # Count intersection if first point is to the right of given point
                            # and second point is above.
                            ni += 1

        return ni

    def isEqual(self, _segment, _tol):
        tol = Point(_tol, _tol)
        if _segment.getType() == 'LINE':
            if len(self.pts) == 2:
                ptsLine = _segment.getPoints()
                if Point.equal(ptsLine[0], self.pts[0], tol):
                    if Point.equal(ptsLine[1], self.pts[1], tol):
                        return True

                elif Point.equal(ptsLine[0], self.pts[1], tol):
                    if Point.equal(ptsLine[1], self.pts[0], tol):
                        return True

                return False

            else:
                return False

        elif _segment.getType() == 'POLYLINE':
            thatPts = _segment.getPoints()

            if len(self.pts) != len(thatPts):
                return False

            if Point.equal(self.pts[0], thatPts[0], tol):
                for i in range(1, len(self.pts)):
                    if not Point.equal(self.pts[i], thatPts[i], tol):
                        return False

                return True

            else:

                for i in range(0, len(self.pts)):
                    if not Point.equal(self.pts[-1-i], thatPts[i], tol):
                        return False

                return True

        else:
            return _segment.isEqual(self, _tol)

    def intersectPoint(self, _pt, _tol):

        partialLength = 0
        totalLength = self.length(0, 1)
        interStatus = False
        param = None

        if Point.euclidiandistance(_pt, self.pts[0]) <= _tol:
            param = 0

        for i in range(1, len(self.pts)):
            p1 = Point(self.pts[i-1].getX(), self.pts[i-1].getY())
            p2 = Point(self.pts[i].getX(), self.pts[i].getY())

            dist, pi, t = CompGeom.getClosestPointSegment(p1, p2, _pt)
            length = math.sqrt(((self.pts[i].getX() - self.pts[i-1].getX()) *
                                (self.pts[i].getX() - self.pts[i-1].getX())) +
                               ((self.pts[i].getY() - self.pts[i-1].getY()) *
                                (self.pts[i].getY() - self.pts[i-1].getY())))

            # skip init intersections at each segment (no repeated intersections)
            if dist <= _tol and t*length > _tol:
                param = ((partialLength + t*length) / totalLength)
                interStatus = True
                break

            partialLength += length

        return interStatus, param, pi

    def intersectSegment(self, _segment):

        status = []
        param1 = []
        param2 = []
        pts = []

        if _segment.getType() == 'LINE' or _segment.getType() == 'POLYLINE':
            poly = _segment.getPoints()
            return CompGeom.computePolyPolyIntersection(self.pts, poly)
        else:
            # for each segment, create a line and intersect each line with the given segment
            totalLength = 0.0
            segLength = 0.0

            for i in range(0, len(self.pts)-1):
                segment = Line(self.pts[i], self.pts[i + 1])
                segLength = segment.length(0, 1)
                segPts, segmentParams, segParams = _segment.intersectsegment(
                    segment)

                for i in range(0, len(segPts)):
                    pts.append(segPts[i])
                    param1.append((segParams[i]*segLength) + totalLength)
                    param2.append(segmentParams[i])

                status.append(len(param1) > 0)
                totalLength += segLength
                segParams = []
                segmentParams = []
                segPts = []

        return status, pts, param1, param2
