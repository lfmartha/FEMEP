from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import NURBS
from geomdl import operations
from geomdl import fitting
from geomdl import convert
import numpy as np
import nurbspy as nrb
import math


class CubicSpline(Curve):
    def __init__(self, _pts=None):
        super(Curve, self).__init__()
        self.type = 'CUBICSPLINE'
        self.pts = _pts
        self.nPts = 0
        self.nurbs = []
        self.eqPoly = []

        if self.pts is not None:
            self.nPts = len(self.pts)

            if self.nPts >= 2:
                # Nurbs degree and control points
                if len(self.pts) == 2:
                    degree = 1
                elif len(self.pts) == 3:
                    degree = 2
                elif len(self.pts) > 3:
                    degree = 3

                ctrlPts = []
                for pt in self.pts:
                    ctrlPts.append([pt.getX(), pt.getY()])

                # Creating Nurbs
                spline = fitting.interpolate_curve(ctrlPts, degree)
                self.nurbs = convert.bspline_to_nurbs(spline)
                self.nurbs.sample_size = 10

                # Generating equivalent polyline
                L = self.lengthInerpPts()
                self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
                self.eqPoly.append(self.pts[-1])

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        pt = Pnt2D(_x, _y)

        if self.nPts == 0:
            self.pts = [pt]
            self.nPts += 1
            # self.eqPoly.append(pt)

        else:
            closeToOther = False
            for i in range(0, self.nPts):
                if Pnt2D.euclidiandistance(self.pts[i], pt) <= 0.01:
                    closeToOther = True
            if closeToOther:
                return
            self.pts.append(pt)
            self.nPts += 1

            # Nurbs degree and control points
            if len(self.pts) == 2:
                degree = 1
            elif len(self.pts) == 3:
                degree = 2
            elif len(self.pts) > 3:
                degree = 3

            ctrlPts = []
            for pt in self.pts:
                ctrlPts.append([pt.getX(), pt.getY()])

            # Creating Nurbs
            spline = fitting.interpolate_curve(ctrlPts, degree)
            self.nurbs = convert.bspline_to_nurbs(spline)
            self.nurbs.sample_size = 10

            # Generating equivalent polyline
            self.eqPoly = []
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            self.eqPoly.append(self.pts[-1])

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t <= 0.0:
            return Pnt2D(self.nurbs.ctrlpts[0][0], self.nurbs.ctrlpts[0][1])
        elif _t >= 1.0:
            return Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])

        pt = self.nurbs.evaluate_single(_t)
        return Pnt2D(pt[0], pt[1])

    # ---------------------------------------------------------------------
    def evalPointTangent(self, _t):
        if _t < 0.0:
            _t = 0.0
        elif _t > 1.0:
            _t = 1.0

        ders = self.nurbs.derivatives(_t, order=1)
        pt = ders[0]
        tang = ders[1]
        return Pnt2D(pt[0], pt[1]), Pnt2D(tang[0], tang[1])

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
    def isStraight(self, _tol):
        ptInit = Pnt2D(self.nurbs.ctrlpts[0][0], self.nurbs.ctrlpts[0][1])
        ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
        for i in range(1, len(self.nurbs.ctrlpts) - 1):
            pt = Pnt2D(self.nurbs.ctrlpts[i][0], self.nurbs.ctrlpts[i][1])
            if not CompGeom.pickLine(ptInit, ptEnd, pt, _tol):
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
        knots = self.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()
    
        for knot in knots:
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
        left = CubicSpline()
        right = CubicSpline()

        # Create the corresponding NURBS curves resulting from splitting
        left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
        return left, right

    # ---------------------------------------------------------------------
    def split(self, _t):
        left, right = self.splitRaw(_t)
        if (left == None) or (right == None):
            return left, right

        # Generate equivalent polylines for each resulting curve
        L = self.length()
        left.eqPoly = []
        left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, 0.001 * L)
        ptLeftEnd = Pnt2D(left.nurbs.ctrlpts[-1][0], left.nurbs.ctrlpts[-1][1])
        left.eqPoly.append(ptLeftEnd)
        right.eqPoly = []
        right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, 0.001 * L)
        ptRightEnd = Pnt2D(right.nurbs.ctrlpts[-1][0], right.nurbs.ctrlpts[-1][1])
        right.eqPoly.append(ptRightEnd)
        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            self.eqPoly.append(self.pts[-1])
        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []
        pt = Pnt2D(_pt.x, _pt.y)

        pts = []
        pts.extend(self.pts)
        pts.append(pt)

        if self.nPts == 1:
            tempEqPoly = pts

        if self.nPts >= 2 and pts[-1] != pts[-2]:
            # Nurbs degree and control points
            if len(pts) == 2:
                degree = 1
            elif len(pts) == 3:
                degree = 2
            elif len(pts) > 3:
                degree = 3

            ctrlPts = []
            for p in pts:
                ctrlPts.append([p.getX(), p.getY()])

            # Creating Nurbs
            cubic_spline = CubicSpline()
            spline = fitting.interpolate_curve(ctrlPts, degree)
            cubic_spline.nurbs = convert.bspline_to_nurbs(spline)
            cubic_spline.nurbs.sample_size = 10

            # Generating equivalent polyline
            L = self.lengthInerpPts()
            tempEqPoly = Curve.genEquivPolyline(cubic_spline, tempEqPoly, 0.001 * L)
            tempEqPoly.append(pts[-1])
        return tempEqPoly

    # ---------------------------------------------------------------------
    def closestPointSeg(self, _x, _y):
        if self.eqPoly is []:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        if len(self.eqPoly) < 2:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        aux = Line(self.eqPoly[0], self.eqPoly[1])
        status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
        xOn = clstPtSeg.getX()
        yOn = clstPtSeg.getY()
        dmin = d
        seg = 0

        for i in range(1, len(self.eqPoly) - 1):
            aux = Line(self.eqPoly[i], self.eqPoly[i + 1])
            status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
            if d < dmin:
                xOn = clstPtSeg.getX()
                yOn = clstPtSeg.getY()
                dmin = d
                seg = i

        arcLen = 0.0
        for i in range(0, seg):
            arcLen += math.sqrt((self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) *
                                (self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) +
                                (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()) *
                                (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()))
        arcLen += math.sqrt((xOn - self.eqPoly[seg].getX()) *
                            (xOn - self.eqPoly[seg].getX()) +
                            (yOn - self.eqPoly[seg].getY()) *
                            (yOn - self.eqPoly[seg].getY()))

        clstPt = Pnt2D(xOn, yOn)
        return status, clstPt, dmin, seg, arcLen

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        status, clstPt, dmin, seg, arcLen = self.closestPointSeg(_x, _y)
        if not status:
            return status, clstPt, dmin, 0.0, Pnt2D(0,0)

        tolLen = self.length()
        t = arcLen / tolLen
        if (t > -Curve.PARAM_TOL) and (t < Curve.PARAM_TOL):
            t = 0.0
            seg = 0
            clstPt = self.eqPoly[seg]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
            status = True
        elif (t > 1.0 - Curve.PARAM_TOL) and (t < 1.0 + Curve.PARAM_TOL):
            t = 1.0
            seg = len(self.eqPoly) - 2
            clstPt = self.eqPoly[seg + 1]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
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
        if t < Curve.PARAM_TOL:
            t = 0.0
            seg = 0
            clstPt = self.eqPoly[seg]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
            status = True
        elif t > 1.0 - Curve.PARAM_TOL:
            t = 1.0
            seg = len(self.eqPoly) - 2
            clstPt = self.eqPoly[seg + 1]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
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
        for point in self.eqPoly:
            x.append(point.getX())
            y.append(point.getY())
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        return xmin, xmax, ymin, ymax

    # ---------------------------------------------------------------------
    def getXinit(self):
        return self.nurbs.ctrlpts[0][0]

    # ---------------------------------------------------------------------
    def getYinit(self):
        return self.nurbs.ctrlpts[0][1]

    # ---------------------------------------------------------------------
    def getXend(self):
        return self.nurbs.ctrlpts[-1][0]

    # ---------------------------------------------------------------------
    def getYend(self):
        return self.nurbs.ctrlpts[-1][1]

    # ---------------------------------------------------------------------
    def lengthInerpPts(self):
        L = 0.0
        for i in range(0, len(self.pts) - 1):
            L += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
                           (self.pts[i + 1].getX() - self.pts[i].getX()) +
                           (self.pts[i + 1].getY() - self.pts[i].getY()) *
                           (self.pts[i + 1].getY() - self.pts[i].getY()))
        return L

    # ---------------------------------------------------------------------
    def length(self):
        L = 0.0
        for i in range(0, len(self.eqPoly) - 1):
            L += math.sqrt((self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) *
                           (self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) +
                           (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()) *
                           (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()))
        return L

    # ---------------------------------------------------------------------
    def updateLineEditValues(self, _NumctrlPts, _y, _LenAndAng):
        x = self.pts[_NumctrlPts - 1].getX()
        y = self.pts[_NumctrlPts - 1].getY()
        return x, y

    # ---------------------------------------------------------------------
    @staticmethod
    def joinTwoCurves(_curv1, _curv2, _pt, _tol):
        if _curv1.nurbs.degree == _curv2.nurbs.degree:
            degree = _curv1.nurbs.degree
        else:
            error_text = "Both curves must have the same degree"
            return None, error_text

        curv1_ctrlpts = _curv1.nurbs.ctrlpts
        curv2_ctrlpts = _curv2.nurbs.ctrlpts
        curv1_knotvector = _curv1.nurbs.knotvector
        curv2_knotvector = _curv2.nurbs.knotvector
        tol = Pnt2D(_tol, _tol)

        # check curves initial point
        if Pnt2D.equal(Pnt2D(curv1_ctrlpts[0][0], curv1_ctrlpts[0][1]), _pt, tol):
            init_pt1 = True
        else:
            init_pt1 = False

        if Pnt2D.equal(Pnt2D(curv2_ctrlpts[0][0], curv2_ctrlpts[0][1]), _pt, tol):
            init_pt2 = True
        else:
            init_pt2 = False

        # cubicspline properties
        curv_ctrlpts = []
        curv_knotvector = []
        if init_pt1 and init_pt2:
            # Control Points
            curv1_ctrlpts.reverse()
            curv1_ctrlpts.pop()
            curv_ctrlpts.extend(curv1_ctrlpts)
            curv_ctrlpts.extend(curv2_ctrlpts)

            # Knot vector
            curv1_knotvector.reverse()
            for i in range(len(curv1_knotvector)):
                curv1_knotvector[i] = 1.0 - curv1_knotvector[i]
            curv1_knotvector.pop()

            for i in range(degree + 1):
                curv2_knotvector.pop(0)

            for i in range(len(curv2_knotvector)):
                curv2_knotvector[i] = curv2_knotvector[i] + 1.0
            
            curv_knotvector.extend(curv1_knotvector)
            curv_knotvector.extend(curv2_knotvector)

        elif not init_pt1 and not init_pt2:
            # Control Points
            curv1_ctrlpts.pop()
            curv2_ctrlpts.reverse()
            curv_ctrlpts.extend(curv1_ctrlpts)
            curv_ctrlpts.extend(curv2_ctrlpts)

            # Knot vector
            curv1_knotvector.pop()

            curv2_knotvector.reverse()
            for i in range(len(curv2_knotvector)):
                curv2_knotvector[i] = 1.0 - curv2_knotvector[i]

            for i in range(degree + 1):
                curv2_knotvector.pop(0)

            for i in range(len(curv2_knotvector)):
                curv2_knotvector[i] = curv2_knotvector[i] + 1.0
            
            curv_knotvector.extend(curv1_knotvector)
            curv_knotvector.extend(curv2_knotvector)

        elif init_pt1 and not init_pt2:
            # Control Points
            curv2_ctrlpts.pop()
            curv_ctrlpts.extend(curv2_ctrlpts)
            curv_ctrlpts.extend(curv1_ctrlpts)

            # Knot vector
            curv2_knotvector.pop()

            for i in range(degree + 1):
                curv1_knotvector.pop(0)

            for i in range(len(curv1_knotvector)):
                curv1_knotvector[i] = curv1_knotvector[i] + 1.0
            
            curv_knotvector.extend(curv2_knotvector)
            curv_knotvector.extend(curv1_knotvector)

        elif not init_pt1 and init_pt2:
            # Control Points
            curv1_ctrlpts.pop()
            curv_ctrlpts.extend(curv1_ctrlpts)
            curv_ctrlpts.extend(curv2_ctrlpts)

            # Knot vector
            curv1_knotvector.pop()

            for i in range(degree + 1):
                curv2_knotvector.pop(0)

            for i in range(len(curv2_knotvector)):
                curv2_knotvector[i] = curv2_knotvector[i] + 1.0
            
            curv_knotvector.extend(curv1_knotvector)
            curv_knotvector.extend(curv2_knotvector)

        
        for i in range(len(curv_knotvector)):
            curv_knotvector[i] = curv_knotvector[i] / 2.0

        curv = CubicSpline()
        curv.nurbs = NURBS.Curve()
        curv.nurbs.degree = degree
        curv.nurbs.ctrlpts = curv_ctrlpts
        curv.nurbs.knotvector = curv_knotvector
        curv.nurbs.sample_size = 10
        
        L1 = _curv1.length()
        L2 = _curv2.length()
        L = (L1 + L2) / 2.0
        curv.eqPoly = Curve.genEquivPolyline(curv, curv.eqPoly, 0.001 * L)
        curv.eqPoly.append(Pnt2D(curv.nurbs.ctrlpts[-1][0], curv.nurbs.ctrlpts[-1][1]))
        return curv, None