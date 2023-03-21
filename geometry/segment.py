from compgeom.pnt2d import Pnt2D
from geometry.curves.curve import Curve
from compgeom.compgeom import CompGeom
from geometry.point import Point
from geomdl import operations
import math
import copy


class Segment():
    def __init__(self, _polypts, _curve=None):
        self.polyline = _polypts  # segment equiv. polyline
        self.curve = _curve  # owning curve (can be empty [])
        self.edge = None
        self.attributes = []
        self.selected = False
        self.nsudv = None
        self.sdvPoints = None
        self.originalNurbs = None

    # ---------------------------------------------------------------------
    def getCurve(self):
        return self.curve

    # ---------------------------------------------------------------------
    def setSelected(self, _status):
        self.selected = _status

    # ---------------------------------------------------------------------
    def isSelected(self):
        return self.selected

    # ---------------------------------------------------------------------
    def getPoints(self):
        return self.polyline

    # ---------------------------------------------------------------------
    def getInitTangent(self):
        # tan = self.polyline[1] - self.polyline[0]
        # tan = Pnt2D.normalize(tan)
        pt, tan = self.curve.evalPointTangent(0.0)
        tan = Pnt2D.normalize(tan)
        return tan

    # ---------------------------------------------------------------------
    def getEndTangent(self):
        # tan = self.polyline[-1] - self.polyline[-2]
        # tan = Pnt2D.normalize(tan)
        pt, tan = self.curve.evalPointTangent(1.0)
        tan = Pnt2D.normalize(tan)
        return tan

    # ---------------------------------------------------------------------
    # THIS WILL BE REMOVED
    def curvature(self, _t):
        return 0.0

    # ---------------------------------------------------------------------
    def intersectPoint(self, _pt, _tol):
        # partialLength = 0
        # totalLength = Segment.polylineLength(self.polyline, 0.0, 1.0)
        # interStatus = False
        # param = None

        # if Point.euclidiandistance(_pt, self.polyline[0]) <= _tol:
        #     param = 0

        # for i in range(1, len(self.polyline)):
        #     p1 = Point(self.polyline[i-1].getX(), self.polyline[i-1].getY())
        #     p2 = Point(self.polyline[i].getX(), self.polyline[i].getY())

        #     dist, pi, t = CompGeom.getClosestPointSegment(p1, p2, _pt)
        #     length = math.sqrt(((self.polyline[i].getX() - self.polyline[i-1].getX()) *
        #                         (self.polyline[i].getX() - self.polyline[i-1].getX())) +
        #                        ((self.polyline[i].getY() - self.polyline[i-1].getY()) *
        #                         (self.polyline[i].getY() - self.polyline[i-1].getY())))

        #     # skip init intersections at each segment (no repeated intersections)
        #     if dist <= _tol and t*length > _tol:
        #     #if dist <= _tol and t > 0.0:
        #         param = ((partialLength + t*length) / totalLength)
        #         status, pi, dmin, param, tang = self.curve.closestPointParam(pi.getX(), pi.getY(), param)
        #         if status == True:
        #             interStatus = True
        #         break

        #     partialLength += length

        # return interStatus, param, pi
        status, clstPt, dmin, t, tang = self.curve.closestPoint(_pt.getX(), _pt.getY())
        if dmin <= _tol:
            return True, t, clstPt
        else:
            return False, t, clstPt

    # ---------------------------------------------------------------------
    def selfIntersectPoly(self):
        flag, pts, params = CompGeom.splitSelfIntersected(self.getPoints())

        return flag, pts, params

    # ---------------------------------------------------------------------
    def split(self, _params, _pts):
        seglen = Segment.polylineLength(self.polyline, 0.0, 1.0)
        tol = 0.001 * seglen
        curv2 = self.curve
        segments = []

        for i in range(0, len(_pts)):
            status, clstPt, dmin, t, tangVec = curv2.closestPointParam(_pts[i].getX(), _pts[i].getY(), _params[i])
            curv1, curv2 = curv2.split(t)

            if curv1 is not None:
                seg1Pts = curv1.getEquivPolyline(0.0, 1.0, tol)
                seg1 = Segment(seg1Pts, curv1)
                segments.append(seg1)

            # update the remaining parameters
            for j in range(i+1, len(_params)):
                _params[j] = (_params[j] - _params[i])/(1-_params[i])

        if curv2 is not None:
            seg2Pts = curv2.getEquivPolyline(0.0, 1.0, tol)
            seg2 = Segment(seg2Pts, curv2)
            segments.append(seg2)
        return segments

    # ---------------------------------------------------------------------
    def length(self, _t0, _t1):
        lenSeg = Segment.polylineLength(self.polyline, _t0, _t1)
        return lenSeg

    # ---------------------------------------------------------------------
    def isEqual(self, _segment, _tol):
        # # Check curves types:
        # if _segment.curve.type != self.curve.type:
        #     return False

        Maybe = False
        # Check knot vector:
        if len(_segment.curve.nurbs.knotvector) == len(self.curve.nurbs.knotvector):
            knotvector1 = _segment.curve.nurbs.knotvector
            knotvector2 = self.curve.nurbs.knotvector
            for i in range (len(knotvector1)):
                diff = knotvector1[i] - knotvector2[i]
                if abs(diff) > Curve.PARAM_TOL:
                    Maybe = True
        else:
            return False

        # Check ctrlpts
        if len(_segment.curve.nurbs.ctrlpts) == len(self.curve.nurbs.ctrlpts):
            ctrlpts1 = _segment.curve.nurbs.ctrlpts
            ctrlpts2 = self.curve.nurbs.ctrlpts
            for i in range (len(ctrlpts1)):
                Pt1 = Pnt2D(ctrlpts1[i][0], ctrlpts1[i][1])
                Pt2 = Pnt2D(ctrlpts2[i][0], ctrlpts2[i][1])
                tol = Pnt2D(_tol, _tol)
                if not Pnt2D.equal(Pt1, Pt2, tol):
                    Maybe = True
        else:
            return False

        # Check weights
        if len(_segment.curve.nurbs.weights) == len(self.curve.nurbs.weights):
            weights1 = _segment.curve.nurbs.weights
            weights2 = self.curve.nurbs.weights
            for i in range (len(weights1)):
                diff = weights1[i] - weights2[i]
                if abs(diff) > Curve.PARAM_TOL:
                    Maybe = True
        else:
            return False

        # Try inversed curve
        if Maybe:
            for i in range(len(knotvector1)):
                if knotvector1[i] != 1.0 and knotvector1[i] != 0.0:
                    knotvector1[i] = 1.0 - knotvector1[i]
            ctrlpts1.reverse()
            weights1.reverse()

            # Check knot vector:
            if len(_segment.curve.nurbs.knotvector) == len(self.curve.nurbs.knotvector):
                for i in range (len(knotvector1)):
                    diff = knotvector1[i] - knotvector2[i]
                    if abs(diff) > Curve.PARAM_TOL:
                        return False
            else:
                return False

            # Check ctrlpts
            if len(_segment.curve.nurbs.ctrlpts) == len(self.curve.nurbs.ctrlpts):
                for i in range (len(_segment.curve.nurbs.ctrlpts)):
                    Pt1 = Pnt2D(ctrlpts1[i][0], ctrlpts1[i][1])
                    Pt2 = Pnt2D(ctrlpts2[i][0], ctrlpts2[i][1])
                    tol = Pnt2D(_tol, _tol)
                    if not Pnt2D.equal(Pt1, Pt2, tol):
                        return False
            else:
                return False

            # Check weights
            if len(_segment.curve.nurbs.weights) == len(self.curve.nurbs.weights):
                for i in range (len(weights1)):
                    diff = weights1[i] - weights2[i]
                    if abs(diff) > Curve.PARAM_TOL:
                        return False
            else:
                return False

        # If reached here return True
        return True

    # ---------------------------------------------------------------------
    def boundIntegral(self):
        area = 0
        for i in range(0, len(self.polyline)-1):
            pt0 = self.polyline[i]
            pt1 = self.polyline[i+1]
            area += (pt0.getX())*(pt1.getY()) - (pt1.getX())*(pt0.getY())
        return area*0.5

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        return self.curve.evalPoint(_t)

    # ---------------------------------------------------------------------
    def getXinit(self):
        pt = self.polyline[0]
        return pt.getX()

    # ---------------------------------------------------------------------
    def getYinit(self):
        pt = self.polyline[0]
        return pt.getY()

    # ---------------------------------------------------------------------
    def getXend(self):
        pt = self.polyline[-1]
        return pt.getX()

    # ---------------------------------------------------------------------
    def getYend(self):
        pt = self.polyline[-1]
        return pt.getY()

    # ---------------------------------------------------------------------
    def getType(self):
        return self.curve.getType()

    # ---------------------------------------------------------------------
    def ray(self, _pt):
        x = _pt.getX()
        y = _pt.getY()
        n = len(self.polyline)
        ni = 0

        for i in range(0, n-1):
            pt1 = self.polyline[i]
            pt2 = self.polyline[i+1]

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

    # ---------------------------------------------------------------------
    def getInitPoint(self):
        xInit = self.polyline[0].getX()
        yInit = self.polyline[0].getY()
        return Point(xInit, yInit)

    # ---------------------------------------------------------------------
    def getEndPoint(self):
        xEnd = self.polyline[-1].getX()
        yEnd = self.polyline[-1].getY()
        return Point(xEnd, yEnd)

    # ---------------------------------------------------------------------
    def setInitPoint(self, _pt):
        self.polyline[0].setX(_pt.getX())
        self.polyline[0].setY(_pt.getY())

    # ---------------------------------------------------------------------
    def setEndPoint(self, _pt):
        self.polyline[-1].setX(_pt.getX())
        self.polyline[-1].setY(_pt.getY())

    # ---------------------------------------------------------------------
    def setNumberSdv(self, _nsudv):
        self.nsudv = _nsudv

    # ---------------------------------------------------------------------
    def getNumberSdv(self):
        if self.nsudv is None:
            return 1
        return self.nsudv

    # ---------------------------------------------------------------------
    def setSdvPoints(self, _sdvPoints):
        self.nsudv = len(_sdvPoints) + 1
        self.sdvPoints = _sdvPoints

    # ---------------------------------------------------------------------
    def delSdvPoints(self):
        if self.sdvPoints is not []:
            del self.sdvPoints
            self.sdvPoints = []
        self.nsudv = None

    # ---------------------------------------------------------------------
    def getSdvPoints(self):
        if self.nsudv is None:
            return []
        return self.sdvPoints

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        if self.curve is not None:
            status, clstPt, dmin, t, tang = self.curve.closestPoint(_x, _y)
            xOn = clstPt.getX()
            yOn = clstPt.getY()
            if status:
                if (t < 0.0) or (t > 1.0):
                    return False, xOn, xOn, dmin
        else:
            status = True
            pt = Pnt2D(_x, _y)
            polypts = self.polyline
            d, clstPtSeg, t = CompGeom.getClosestPointSegment(polypts[0], polypts[1], pt)
            xOn = clstPtSeg.getX()
            yOn = clstPtSeg.getY()
            dmin = d
            for i in range(1, len(polypts) - 1):
                d, clstPtSeg, t = CompGeom.getClosestPointSegment(polypts[i], polypts[i + 1], pt)
                if d < dmin:
                    xOn = clstPtSeg.getX()
                    yOn = clstPtSeg.getY()
                    dmin = d
        return status, xOn, yOn, dmin

    # ---------------------------------------------------------------------
    def getBoundBox(self):
        # Compute segment bounding box based on segment polypoints
        x = []
        y = []
        for point in self.polyline:
            x.append(point.getX())
            y.append(point.getY())
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        return xmin, xmax, ymin, ymax

    # ---------------------------------------------------------------------
    def refineNumberSdv(self):
        if self.nsudv is None:
            return

        if self.originalNurbs is None:
            self.originalNurbs = copy.deepcopy(self.curve.nurbs)

        knots = self.curve.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()

        knotsToBeInserted = []
        for i in range(len(knots) - 1):
            mediumKnot = (knots[i] + knots[i + 1]) / 2.0
            knotsToBeInserted.append(mediumKnot)

        for knot in knotsToBeInserted:
            operations.insert_knot(self.curve.nurbs, [knot], [1])
        
    # ---------------------------------------------------------------------
    def BackToOriginalNurbs(self):
        if self.originalNurbs is None:
            return

        self.curve.nurbs = copy.deepcopy(self.originalNurbs)

    # ---------------------------------------------------------------------
    def getNurbs(self):
        return self.curve.nurbs

    # ---------------------------------------------------------------------
    def degreeChange(self, _degree):
        status = self.curve.degreeChange(_degree)
        return status

    # ---------------------------------------------------------------------
        
    # def evalPoint(self, _t):
    #     # Get the owning curve and polyline of given segmente.
    #     curve = self.curve

    #     # Evaluate point on segment based on its polyline
    #     pt, locSeg, tloc = Segment.evalPolylinePointSeg(self.polyline, _t)
 
    #     # Get closest point on onwing curve
    #     if curve is not None:  # In case there is a supporting curve
    #         status, pt, dist, par, tangVec = curve.closestPointParam(pt.getX(), pt.getY(), _t)

    #     return pt

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # --------------------------- CLASS METHODS ---------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    @staticmethod
    def polylineLength(_polypts, _tInit, _tEnd):
        nPts = len(_polypts)
        L = 0.0
        for i in range(0, nPts - 1):
            L += math.sqrt((_polypts[i + 1].getX() - _polypts[i].getX()) *
                           (_polypts[i + 1].getX() - _polypts[i].getX()) +
                           (_polypts[i + 1].getY() - _polypts[i].getY()) *
                           (_polypts[i + 1].getY() - _polypts[i].getY()))

        return L * (_tEnd - _tInit)

    # ---------------------------------------------------------------------
    # Evaluate a point on polyline for a given parametric value.
    # Also return the segment of the polyline of the evaluated point and
    # the local parametric value in segment
    @staticmethod
    def evalPolylinePointSeg(_polypts, _t):
        nPts = len(_polypts)
        if _t <= 0.0:
            return Pnt2D(_polypts[0].getX(), _polypts[0].getY()), 0, 0.0

        if _t >= 1.0:
            return Pnt2D(_polypts[-1].getX(), _polypts[-1].getY()), nPts - 1, 1.0

        length = Segment.polylineLength(_polypts, 0.0, 1.0)
        s = _t * length
        loc_t = 1.0
        prev_id = 0
        next_id = 0
        lenToSeg = 0.0

        for i in range(1, nPts):
            prev_id = i - 1
            next_id = i
            dist = math.sqrt((_polypts[i].getX() - _polypts[i - 1].getX()) *
                             (_polypts[i].getX() - _polypts[i - 1].getX()) +
                             (_polypts[i].getY() - _polypts[i - 1].getY()) *
                             (_polypts[i].getY() - _polypts[i - 1].getY()))

            if (lenToSeg + dist) >= s:
                loc_t = (s - lenToSeg) / dist
                break

            lenToSeg += dist

        x = _polypts[prev_id].getX() + loc_t * \
            (_polypts[next_id].getX() - _polypts[prev_id].getX())
        y = _polypts[prev_id].getY() + loc_t * \
            (_polypts[next_id].getY() - _polypts[prev_id].getY())

        return Pnt2D(x, y), prev_id, loc_t

    # ---------------------------------------------------------------------
    @staticmethod
    def generatePartialPolyline(_polypts, _tInit, _tEnd):
        nPts = len(_polypts)
        equivPoly = []
        if (_tEnd - _tInit) <= Curve.PARAM_TOL:
            return equivPoly

        ptInit, segInit, tlocInit = Segment.evalPolylinePointSeg(_polypts, _tInit)
        ptEnd, segEnd, tlocEnd = Segment.evalPolylinePointSeg(_polypts, _tEnd)

        if abs(tlocInit) <= Curve.PARAM_TOL:
            ptInit = _polypts[segInit]
        elif abs(tlocInit - 1.0) <= Curve.PARAM_TOL:
            segInit += 1
            ptInit = _polypts[segInit]

        if abs(tlocEnd) <= Curve.PARAM_TOL:
            ptEnd = _polypts[segEnd]
            segEnd -= 1
        elif abs(tlocEnd - 1.0) <= Curve.PARAM_TOL:
            if segEnd < (nPts - 1):
                ptEnd = _polypts[segEnd + 1]
            else:
                ptEnd = _polypts[segEnd]
                segEnd -= 1

        equivPoly.append(ptInit)
        for i in range(segInit + 1, segEnd + 1):
            equivPoly.append(_polypts[i])
        equivPoly.append(ptEnd)
        return equivPoly
