from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import NURBS
from geomdl import knotvector
from geomdl import operations
import math


class Polyline(Curve):
    def __init__(self, _pts=None):
        super(Curve, self).__init__()
        self.type = 'POLYLINE'
        self.pts = _pts
        self.nPts = 0
        self.nurbs = []

        if self.pts is not None:
            self.nPts = len(self.pts)

            if self.nPts >= 2:
                # Nurbs degree and control points
                degree = 1
                ctrlPts = []
                for pt in self.pts:
                    ctrlPts.append([pt.getX(), pt.getY()])

                # NURBS knotvector
                knotVector = knotvector.generate(degree, len(ctrlPts))

                # Creating Nurbs polyline
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = degree
                self.nurbs.ctrlpts = ctrlPts
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        pt = Pnt2D(_x,_y)

        if self.nPts == 0:
            self.pts = [pt]
            self.nPts += 1

        else:
            self.pts.append(pt)
            self.nPts += 1

            # Nurbs degree and control points
            degree = 1
            ctrlPts = []
            for pt in self.pts:
                ctrlPts.append([pt.getX(), pt.getY()])

            # NURBS knotvector
            knotVector = knotvector.generate(degree, len(ctrlPts))

            # Creating Nurbs polyline
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = degree
            self.nurbs.ctrlpts = ctrlPts
            self.nurbs.knotvector = knotVector
            self.nurbs.sample_size = 10

    # ---------------------------------------------------------------------
    # Evaluate a point for a given parametric value.
    # Also return the segment of the evaluated point and
    # the local parametric value in segment
    def evalPointSeg(self, _t):
        if _t <= 0.0:
            return Pnt2D(self.pts[0].getX(), self.pts[0].getY()), 0, 0.0

        if _t >= 1.0:
            return Pnt2D(self.pts[-1].getX(), self.pts[-1].getY()), self.nPts - 1, 1.0

        length = self.length(0.0, 1.0)
        s = _t * length
        loc_t = 1.0
        prev_id = 0
        next_id = 0
        lenToSeg = 0.0

        for i in range(1, len(self.pts)):
            prev_id = i - 1
            next_id = i
            dist = math.sqrt((self.pts[i].getX() - self.pts[i - 1].getX()) *
                             (self.pts[i].getX() - self.pts[i - 1].getX()) +
                             (self.pts[i].getY() - self.pts[i - 1].getY()) *
                             (self.pts[i].getY() - self.pts[i - 1].getY()))

            if (lenToSeg + dist) >= s:
                loc_t = (s - lenToSeg) / dist
                break

            lenToSeg += dist

        x = self.pts[prev_id].getX() + loc_t * \
            (self.pts[next_id].getX() - self.pts[prev_id].getX())
        y = self.pts[prev_id].getY() + loc_t * \
            (self.pts[next_id].getY() - self.pts[prev_id].getY())

        return Pnt2D(x, y), prev_id, loc_t

    # ---------------------------------------------------------------------
    # Evaluate a point for a given parametric value.
    def evalPoint(self, _t):
        if _t > 1.0:
            _t = 1.0
        elif _t <= 0.0:
            _t = 0.0

        pt = self.nurbs.evaluate_single(_t)
        x = pt[0]
        y = pt[1]

        return Pnt2D(x, y)

    # ---------------------------------------------------------------------
    def evalPointTangent(self, _t):
        if _t > 1.0:
            _t = 1.0
        elif _t <= 0.0:
            _t = 0.0

        ders = self.nurbs.derivatives(_t, order=1)
        pt = ders[0]
        x = pt[0]
        y = pt[1]
        tang = ders[1]
        dx = tang[0]
        dy = tang[1]

        return Pnt2D(x, y), Pnt2D(dx, dy)

        # pt, seg, loc_t = self.evalPointSeg(_t)

        # if _t <= 0.0:
        #     tan = self.pts[1]-self.pts[0]
        #     tan = Pnt2D.normalize(tan)
        #     return pt, tan

        # if _t >= 1.0:
        #     tan = self.pts[-1]-self.pts[-2]
        #     tan = Pnt2D.normalize(tan)
        #     return pt, tan

        # tangVec = self.pts[seg + 1] - self.pts[seg]

        # pt = self.nurbs.evaluate_single(_t)
        # x = pt[0]
        # y = pt[1]
        # pt = Pnt2D(x,y)

        # return pt, tangVec

    # ---------------------------------------------------------------------
    def evalPointCurvature(self, _t):
        pt = self.evalPoint(_t)
        CurvVec = 0.0
        return pt, CurvVec

    # ---------------------------------------------------------------------
    def isPossible(self):
        if self.nPts < 2:
            return False
        return True

    # ---------------------------------------------------------------------
    def isUnlimited(self):
        return True

    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        return self.pts

    # ---------------------------------------------------------------------
    def setCtrlPoint(self, _id, _x, _y, _tol):
        if self.nPts < 2:
            return False
        if _id < 0:
            return False
        if _id >= self.nPts:
            return False
        pt = Pnt2D(_x, _y)
        # Check to see whether coordinates of current control point will
        # be equal to the coordinates of other control point. Do not allow
        # creating a closed curve.
        for i in range(0, self.nPts):
            if i == _id:
                continue
            if Pnt2D.euclidiandistance(pt, self.pts[i]) <= _tol:
                return False
        self.pts[_id].setCoords(_x, _y)
        return True

    # ---------------------------------------------------------------------
    def isStraight(self, _tol):
        for i in range(1, len(self.pts) - 1):
            if not CompGeom.pickLine(self.pts[0], self.pts[-1], self.pts[i], _tol):
                return False
        return True

    # ---------------------------------------------------------------------
    def isClosed(self):
        xInit = self.getXinit()
        yInit = self.getYinit()
        xEnd = self.getXend()
        yEnd = self.getYend()
        if (xInit == xEnd) and (yInit == yEnd):
            return True
        return False

    # ---------------------------------------------------------------------
    def splitRaw(self, _t):
        for knot in self.nurbs.knotvector:
            if _t >= (knot - 1000*Curve.PARAM_TOL) and _t <= (knot + 1000*Curve.PARAM_TOL):
                _t = knot

        if _t <= Curve.PARAM_TOL:
            left = None
            right = self
            return left, right
        if (1.0 - _t) <= Curve.PARAM_TOL:
            left = self
            right = None
            return left, right

        # Create two curve objects resulting from splitting
        left = Polyline()
        right = Polyline()

        # Create the corresponding NURBS curves resulting from splitting
        # if _t > 0.5 and _t <= (0.5 + Curve.PARAM_TOL):
        #     _t = 0.5
        # elif _t < 0.5 and _t >= (0.5 - Curve.PARAM_TOL):
        #     _t = 0.5
            
        # try:
        left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
        # except:
        #     try:
        #         left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t - Curve.PARAM_TOL)
        #     except:
        #         left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t + Curve.PARAM_TOL)

        return left, right
        
    # ---------------------------------------------------------------------
    def split(self, _t):
        left, right = self.splitRaw(_t)
        if (left == None) or (right == None):
            return left, right

        left_pts = []
        right_pts = []
        # pt, prev_id, tloc = self.evalPointSeg(_t)

        # for i in range(0, prev_id):
        #     left_pts.append(self.pts[i])

        # # check whether the split point is one of the points of the polyline itself
        # if tloc > Curve.PARAM_TOL:
        #     left_pts.append(self.pts[prev_id])

        # left_pts.append(pt)
        # right_pts.append(pt)

        # if 1.0 - tloc > Curve.PARAM_TOL:
        #     right_pts.append(self.pts[prev_id + 1])

        # for j in range(prev_id + 2, self.nPts):
        #     right_pts.append(self.pts[j])


        for pt in left.nurbs.ctrlpts:
            left_pts.append(Pnt2D(pt[0], pt[1]))

        for pt in right.nurbs.ctrlpts:
            right_pts.append(Pnt2D(pt[0], pt[1]))


        left.pts = left_pts
        left.nPts = len(left_pts)
        right.pts = right_pts
        right.nPts = len(right_pts)

        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        return self.pts

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempPts = []
        for i in range(0, self.nPts):
            tempPts.append(self.pts[i])

        tempPts.append(_pt)
        return tempPts

    # ---------------------------------------------------------------------
    # Returns the closest point on polyline for a given point.
    # Also returns the segment of the closest point and the arc
    # length from the curve init to the closest point.
    # def closestPointSeg(self, _x, _y):
    #     pt = Pnt2D(_x, _y)
    #     d, clstPtSeg, t = CompGeom.getClosestPointSegment(self.pts[0], self.pts[1], pt)
    #     xOn = clstPtSeg.getX()
    #     yOn = clstPtSeg.getY()
    #     dmin = d
    #     seg = 0

    #     for i in range(1, self.nPts - 1):
    #         d, clstPtSeg, t = CompGeom.getClosestPointSegment(self.pts[i], self.pts[i + 1], pt)
    #         if d < dmin:
    #             xOn = clstPtSeg.getX()
    #             yOn = clstPtSeg.getY()
    #             dmin = d
    #             seg = i

    #     arcLen = 0.0
    #     for i in range(0, seg):
    #         arcLen += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
    #                             (self.pts[i + 1].getX() - self.pts[i].getX()) +
    #                             (self.pts[i + 1].getY() - self.pts[i].getY()) *
    #                             (self.pts[i + 1].getY() - self.pts[i].getY()))
    #     arcLen += math.sqrt((xOn - self.pts[seg].getX()) *
    #                         (xOn - self.pts[seg].getX()) +
    #                         (yOn - self.pts[seg].getY()) *
    #                         (yOn - self.pts[seg].getY()))

    #     clstPt = Pnt2D(xOn, yOn)
    #     return clstPt, dmin, seg, arcLen

    # # ---------------------------------------------------------------------
    # def closestPoint(self, _x, _y):

    #     clstPt, dmin, seg, arcLen = self.closestPointSeg(_x, _y)
    #     totLen = self.length(0.0, 1.0)
    #     t = arcLen / totLen
    #     tangVec = self.pts[seg + 1] - self.pts[seg]
    #     return True, clstPt, dmin, t, tangVec

    # # ---------------------------------------------------------------------
    # def closestPointParam(self, _x, _y, _tStart):
    #     clstPt, tangVec = self.evalPointTangent(_tStart)
    #     if ((abs(clstPt.getX() - _x) < Curve.COORD_TOL) and
    #         (abs(clstPt.getY() - _y) < Curve.COORD_TOL)):
    #         return True, clstPt, 0.0, _tStart, tangVec

    #     status, clstPt, dist, t, tangVec = self.closestPoint(_x, _y)
    #     return status, clstPt, dist, t, tangVec

    def closestPointSeg(self, _x, _y):
        if self.pts is []:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        if len(self.pts) < 2:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        aux = Line(self.pts[0], self.pts[1])
        status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
        xOn = clstPtSeg.getX()
        yOn = clstPtSeg.getY()
        dmin = d
        seg = 0

        for i in range(1, len(self.pts) - 1):
            aux = Line(self.pts[i], self.pts[i + 1])
            status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
            if d < dmin:
                xOn = clstPtSeg.getX()
                yOn = clstPtSeg.getY()
                dmin = d
                seg = i

        arcLen = 0.0
        for i in range(0, seg):
            arcLen += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
                                (self.pts[i + 1].getX() - self.pts[i].getX()) +
                                (self.pts[i + 1].getY() - self.pts[i].getY()) *
                                (self.pts[i + 1].getY() - self.pts[i].getY()))
        arcLen += math.sqrt((xOn - self.pts[seg].getX()) *
                            (xOn - self.pts[seg].getX()) +
                            (yOn - self.pts[seg].getY()) *
                            (yOn - self.pts[seg].getY()))

        clstPt = Pnt2D(xOn, yOn)
        return status, clstPt, dmin, seg, arcLen

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        status, clstPt, dmin, seg, arcLen = self.closestPointSeg(_x, _y)
        if not status:
            return status, clstPt, dmin, 0.0, Pnt2D(0,0)

        tolLen = self.length(0.0, 1.0)
        t = arcLen / tolLen
        t = self.updateParametricValue(t)
        if t <= 0.0:
            t = 0.0
            seg = 0
            clstPt = self.pts[seg]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        elif t >= 1.0:
            t = 1.0
            seg = len(self.pts) - 2
            clstPt = self.pts[seg + 1]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        else:
            status, clstPt, t, tang = Curve.ParamCurveClosestPt(self, _x, _y, t)
        if status:
            dmin = math.sqrt((clstPt.getX() - _x) * (clstPt.getX() - _x) +
                             (clstPt.getY() - _y) * (clstPt.getY() - _y))
        return status, clstPt, dmin, t, tang

    # ---------------------------------------------------------------------
    def closestPointParam(self, _x, _y, _tStart):
        t = _tStart
        t = self.updateParametricValue(t)
        if t < Curve.PARAM_TOL:
            t = 0.0
            seg = 0
            clstPt = self.pts[seg]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        elif t > 1.0 - Curve.PARAM_TOL:
            t = 1.0
            seg = len(self.pts) - 2
            clstPt = self.pts[seg + 1]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        else:
            status, clstPt, t, tang = Curve.ParamCurveClosestPt(self, _x, _y, t)
        if status:
            dmin = math.sqrt((clstPt.getX() - _x) * (clstPt.getX() - _x) +
                             (clstPt.getY() - _y) * (clstPt.getY() - _y))
        else:
            dmin = 0.0
        return status, clstPt, dmin, t, tang

    # ---------------------------------------------------------------------
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

    # ---------------------------------------------------------------------
    def getXinit(self):
        return self.pts[0].getX()

    # ---------------------------------------------------------------------
    def getYinit(self):
        return self.pts[0].getY()

    # ---------------------------------------------------------------------
    def getXend(self):
        return self.pts[-1].getX()

    # ---------------------------------------------------------------------
    def getYend(self):
        return self.pts[-1].getY()

    # ---------------------------------------------------------------------
    def updateParametricValue(self, _t):
        if _t == 0.0 or _t == 1.0:
            return _t

        knots = self.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()

        pt, prev_id, loc_t = self.evalPointSeg(_t)
        t = knots[prev_id] + loc_t * (knots[prev_id + 1] - knots[prev_id])
        return t

    # ---------------------------------------------------------------------
    def length(self, _tInit, _tEnd):
        L = 0.0
        for i in range(0, self.nPts - 1):
            L += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
                           (self.pts[i + 1].getX() - self.pts[i].getX()) +
                           (self.pts[i + 1].getY() - self.pts[i].getY()) *
                           (self.pts[i + 1].getY() - self.pts[i].getY()))

        return L * (_tEnd - _tInit)
        
    # ---------------------------------------------------------------------
    def updateLineEditValues(self, _NumctrlPts, _y, _LenAndAng):
        x = self.pts[_NumctrlPts - 1].getX()
        y = self.pts[_NumctrlPts - 1].getY()
        return x, y

    # ---------------------------------------------------------------------
    def degreeChange(self, _degree):
        # Check if degree change is possible
        if self.nPts <= (_degree + 1):
            return False

        # NURBS knotvector
        knotvector = []
        knotvector.extend([0.0] * (_degree + 1))
        knot = 0.0
        for i in range(len(self.pts) - 2):
            knot += 1.0 / (len(self.pts) - 1)
            knotvector.extend([knot] * _degree)
        knotvector.extend([1.0] * (_degree + 1))

        # NURBS Control Points
        ctrlPts = []
        if _degree == 1:
            for pt in self.pts:
                ctrlPts.append([pt.getX(), pt.getY()])

        elif _degree == 2:
            # For an even number of control points
            if self.nPts % 2 == 0:
                MiddleKnot2 = int(self.nPts / 2)
                MiddleKnot1 = MiddleKnot2 - 1
                MiddlePt = (self.pts[MiddleKnot2] - self.pts[MiddleKnot2]) / 2.0
                for pt in self.pts:
                    if pt == self.pts[MiddleKnot1]:
                        ctrlPts.append([pt.getX(), pt.getY()])
                        ctrlPts.append([MiddlePt.getX(), MiddlePt.getY()])
                    elif pt == self.pts[MiddleKnot2]:
                        ctrlPts.append([pt.getX(), pt.getY()])
                    else:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 2)
            # For an odd number of control points
            else:
                MiddleKnot = int(self.nPts / 2.0)
                for pt in self.pts:
                    if pt == self.pts[MiddleKnot]:
                        ctrlPts.append([pt.getX(), pt.getY()])
                    else:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 2)

        elif _degree == 3:
            # For an even number of control points
            if self.nPts % 2 == 0:
                MiddleKnot2 = int(self.nPts / 2)
                MiddleKnot1 = MiddleKnot2 - 1
                for pt in self.pts:
                    if pt == self.pts[MiddleKnot2] or pt == self.pts[MiddleKnot1]:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 2)
                    else:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 3)
            # For an odd number of control points
            else:
                for pt in self.pts:
                    if pt == self.pts[1] or pt == self.pts[-2]:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 2)
                    else:
                        ctrlPts.extend([[pt.getX(), pt.getY()]] * 3)

        # Creating Nurbs polyline
        self.nurbs = NURBS.Curve()
        self.nurbs.degree = _degree
        self.nurbs.ctrlpts = ctrlPts
        self.nurbs.knotvector = knotvector
        self.nurbs.sample_size = 10
        return True
