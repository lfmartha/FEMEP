from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import knotvector
from geomdl import fitting
from geomdl import convert
from geomdl import operations
from geomdl import NURBS
import numpy as np
import nurbspy as nrb
import math


class CubicSpline(Curve):
    def __init__(self, _pts=None):
        super(Curve, self).__init__()
        self.type = 'CUBICSPLINE'
        self.pts = _pts
        self.nurbs = []
        if self.pts is None:
            self.pts = []
        self.nPts = len(self.pts)
        self.eqPoly = []
        if self.nPts > 1:
            if len(self.pts) == 2:
                degree = 1
            elif len(self.pts) == 3:
                degree = 2
            elif len(self.pts) > 3:
                degree = 3
            crvPts = []
            for pt in self.pts:
                crvPts.append([pt.getX(), pt.getY()])
            spline = fitting.interpolate_curve(crvPts, degree)
            self.nurbs = convert.bspline_to_nurbs(spline)
            self.nurbs.sample_size = 10
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            self.eqPoly.append(self.pts[-1])

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        pt = Pnt2D(_x, _y)
        closeToOther = False
        for i in range(0, self.nPts):
           if Pnt2D.euclidiandistance(self.pts[i], pt) <= 0.01:
                closeToOther = True
        if closeToOther:
            return
        self.pts.append(pt)
        self.nPts += 1
        if self.nPts > 1:
            if len(self.pts) == 2:
                degree = 1
            elif len(self.pts) == 3:
                degree = 2
            elif len(self.pts) > 3:
                degree = 3
            crvPts = []
            for pt in self.pts:
                crvPts.append([pt.getX(), pt.getY()])
            spline = fitting.interpolate_curve(crvPts, degree)
            #spline.knotvector = knotvector.generate(degree, len(crvPts))
            self.nurbs = convert.bspline_to_nurbs(spline)
            self.nurbs.sample_size = 10
            self.eqPoly = []
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            self.eqPoly.append(self.pts[-1])

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

    # Adicionado --------------------
    def evalPointCurvature(self, _t):
        pt = self.evalPoint(_t)
        CurvVec = 0.0
        return pt, CurvVec
        # pt = self.evalPoint(_t)
        # ders = self.nurbs.derivatives(_t, order=2)
        # CurvVecX = abs(ders[2][0]) / ((1 + ders[1][0] ** 2) ** (3/2))
        # CurvVecY = abs(ders[2][1]) / ((1 + ders[1][1] ** 2) ** (3/2))
        # return pt, Pnt2D(CurvVecX, CurvVecY)
    # Adicionado --------------------

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

        if len(self.pts) == 2:
            degree = 1
        elif len(self.pts) == 3:
            degree = 2
        elif len(self.pts) > 3:
            degree = 3
        crvPts = []
        for pt in self.pts:
            crvPts.append([pt.getX(), pt.getY()])
        spline = fitting.interpolate_curve(crvPts, degree)
        self.nurbs = convert.bspline_to_nurbs(spline)
        self.eqPoly = []
        self.nurbs.sample_size = 10
        L = self.lengthInerpPts()
        self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
        self.eqPoly.append(self.pts[-1])
        return True

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
        if _t > 0.5 and _t <= (0.5 + Curve.PARAM_TOL):
            _t = 0.5
        elif _t < 0.5 and _t >= (0.5 - Curve.PARAM_TOL):
            _t = 0.5
            
        try:
            left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
        except:
            try:
                left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t - Curve.PARAM_TOL)
            except:
                left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t + Curve.PARAM_TOL)

        return left, right

    # ---------------------------------------------------------------------
    def split(self, _t):
        left, right = self.splitRaw(_t)
        if (left == None) or (right == None):
            return left, right

        # Generate equivalent polylines for each resulting curve
        lenOrig = self.length(0.0, 1.0)
        tol = lenOrig * 0.001
        left.eqPoly = []
        left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, tol)
        ptLeftEnd = Pnt2D(left.nurbs.ctrlpts[-1][0], left.nurbs.ctrlpts[-1][1])
        left.eqPoly.append(ptLeftEnd)
        right.eqPoly = []
        right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, tol)
        ptRightEnd = Pnt2D(right.nurbs.ctrlpts[-1][0], right.nurbs.ctrlpts[-1][1])
        right.eqPoly.append(ptRightEnd)

        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, _tol)
            ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
            self.eqPoly.append(ptEnd)

        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []
        if self.nPts < 1:
            return tempEqPoly

        tempCurve = CubicSpline()

        closeToOther = False
        for i in range(0, self.nPts):
            tempCurve.pts.append(self.pts[i])
            if Pnt2D.euclidiandistance(tempCurve.pts[i], _pt) <= 0.01:
                closeToOther = True
        if not closeToOther:
            tempCurve.pts.append(_pt)

        tempCurve.nPts = len(tempCurve.pts)

        if tempCurve.nPts < 2:
            return tempEqPoly
        elif tempCurve.nPts < 3:
            degree = 1
        elif tempCurve.nPts < 4:
            degree = 2
        else:
            degree = 3

        crvPts = []
        for pt in tempCurve.pts:
            crvPts.append([pt.getX(), pt.getY()])
        spline = fitting.interpolate_curve(crvPts, degree)
        #spline.knotvector = knotvector.generate(degree, len(crvPts))
        tempCurve.nurbs = convert.bspline_to_nurbs(spline)
        tempCurve.nurbs.sample_size = 10
        L = tempCurve.lengthInerpPts()
        tempEqPoly = Curve.genEquivPolyline(tempCurve, tempEqPoly, 0.001 * L)
        tempEqPoly.append(tempCurve.pts[-1])
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

        tolLen = self.length(0.0, 1.0)
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
    def length(self, _tInit, _tEnd):
        L = 0.0
        for i in range(0, len(self.eqPoly) - 1):
            L += math.sqrt((self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) *
                           (self.eqPoly[i + 1].getX() - self.eqPoly[i].getX()) +
                           (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()) *
                           (self.eqPoly[i + 1].getY() - self.eqPoly[i].getY()))
        return L * (_tEnd - _tInit)

    # ---------------------------------------------------------------------
    def updateLineEditValues(self, _NumctrlPts, _y, _LenAndAng):
        x = self.pts[_NumctrlPts - 1].getX()
        y = self.pts[_NumctrlPts - 1].getY()
        return x, y

    # ---------------------------------------------------------------------
    @staticmethod
    def joinTwoCurves(_curv1, _curv2, pt):
        if _curv1.nurbs.degree == _curv2.nurbs.degree:
            degree = _curv1.nurbs.degree
        else:
            error_text = "Both curves must have the same degree"
            return None, error_text

        curv1_ctrlpts = _curv1.nurbs.ctrlpts
        curv2_ctrlpts = _curv2.nurbs.ctrlpts
        curv1_knotvector = _curv1.nurbs.knotvector
        curv2_knotvector = _curv2.nurbs.knotvector
        tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)

        if Pnt2D.equal(Pnt2D(curv1_ctrlpts[0][0], curv1_ctrlpts[0][1]), pt, tol):
            init_pt1 = True
        else:
            init_pt1 = False

        if Pnt2D.equal(Pnt2D(curv2_ctrlpts[0][0], curv2_ctrlpts[0][1]), pt, tol):
            init_pt2 = True
        else:
            init_pt2 = False

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
        
        L1 = _curv1.length(0.0, 1.0)
        L2 = _curv2.length(0.0, 1.0)
        L = (L1 + L2) / 2.0
        curv.eqPoly = Curve.genEquivPolyline(curv, curv.eqPoly, 0.001 * L)
        curv.eqPoly.append(Pnt2D(curv.nurbs.ctrlpts[-1][0], curv.nurbs.ctrlpts[-1][1]))

        return curv, None

    # ---------------------------------------------------------------------
    @staticmethod
    def jointwoCurves(_curv1, _curv2, pt):
        if _curv1.nurbs.degree == _curv2.nurbs.degree:
            deg = _curv1.nurbs.degree
        else:
            error_text = "Both curves must have the same degree"
            return None, error_text

        curv1_ctrlpts = _curv1.nurbs.ctrlpts
        curv2_ctrlpts = _curv2.nurbs.ctrlpts
        curv1_knotvector = _curv1.nurbs.knotvector
        curv2_knotvector = _curv2.nurbs.knotvector
        tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)

        if Pnt2D.equal(Pnt2D(curv1_ctrlpts[0][0], curv1_ctrlpts[0][1]), pt, tol):
            init_pt1 = True
        else:
            init_pt1 = False

        if Pnt2D.equal(Pnt2D(curv2_ctrlpts[0][0], curv2_ctrlpts[0][1]), pt, tol):
            init_pt2 = True
        else:
            init_pt2 = False

        if init_pt1 and init_pt2:
            # Control Points
            curv1_ctrlpts.reverse()

            # Knot vector
            curv1_knotvector.reverse()
            for i in range(len(curv1_knotvector)):
                curv1_knotvector[i] = 1.0 - curv1_knotvector[i]

            curv1_knotvector = np.array(curv1_knotvector)
            curv1_ctrlpts = np.transpose(np.array(curv1_ctrlpts))

            curv2_knotvector = np.array(curv2_knotvector)
            curv2_ctrlpts = np.transpose(np.array(curv2_ctrlpts))

            curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
            curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
            curv = curv1.attach_nurbs(curv2)

        elif not init_pt1 and not init_pt2:
            # Control Points
            curv2_ctrlpts.reverse()

            # Knot vector
            curv2_knotvector.reverse()
            for i in range(len(curv2_knotvector)):
                curv2_knotvector[i] = 1.0 - curv2_knotvector[i]

            curv1_knotvector = np.array(curv1_knotvector)
            curv1_ctrlpts = np.transpose(np.array(curv1_ctrlpts))

            curv2_knotvector = np.array(curv2_knotvector)
            curv2_ctrlpts = np.array(curv2_ctrlpts)

            curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
            curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
            curv = curv1.attach_nurbs(curv2)

        elif init_pt1 and not init_pt2:

            curv1_knotvector = np.array(curv1_knotvector)
            curv1_ctrlpts = np.transpose(np.array(curv1_ctrlpts))

            curv2_knotvector = np.array(curv2_knotvector)
            curv2_ctrlpts = np.transpose(np.array(curv2_ctrlpts))

            curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
            curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
            curv = curv2.attach_nurbs(curv1)

        elif not init_pt1 and init_pt2:

            curv1_knotvector = np.array(curv1_knotvector)
            curv1_ctrlpts = np.transpose(np.array(curv1_ctrlpts))

            curv2_knotvector = np.array(curv2_knotvector)
            curv2_ctrlpts = np.transpose(np.array(curv2_ctrlpts))

            curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
            curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
            curv = curv1.attach_nurbs(curv2)

        curv_geomdl = CubicSpline()
        curv_geomdl.nurbs = NURBS.Curve()
        curv_geomdl.nurbs.degree = curv.p
        curv_geomdl.nurbs.ctrlpts = np.transpose(curv.P).tolist()
        curv_geomdl.nurbs.knotvector = curv.U.tolist()
        curv_geomdl.nurbs.sample_size = 10

        L1 = _curv1.length(0.0, 1.0)
        L2 = _curv2.length(0.0, 1.0)
        L = (L1 + L2) / 2.0
        curv_geomdl.eqPoly = Curve.genEquivPolyline(curv_geomdl, curv_geomdl.eqPoly, 0.001 * L)
        curv_geomdl.eqPoly.append(Pnt2D(curv_geomdl.nurbs.ctrlpts[-1][0], curv_geomdl.nurbs.ctrlpts[-1][1]))

        return curv_geomdl, None
