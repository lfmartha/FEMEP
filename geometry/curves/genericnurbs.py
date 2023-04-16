from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geometry.point import Point
from geomdl import fitting
from geomdl import convert
from geomdl import operations
from geomdl import NURBS
import numpy as np
import math


class GenericNurbs(Curve):
    def __init__(self, _nurbs=None):
        super(Curve, self).__init__()
        self.type = 'GENERICNURBS'
        self.nurbs = _nurbs
        self.pt0 = None
        self.pt1 = None
        self.eqPoly = []
        if self.nurbs is not None:
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
            self.eqPoly.append(ptEnd)
            self.pt0 = Point(self.nurbs.ctrlpts[0][0], self.nurbs.ctrlpts[0][1])
            self.pt1 = Point(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])

    # ---------------------------------------------------------------------
    def splitRaw(self, _t):
        round = False
        for knot in self.nurbs.knotvector:
            if _t >= (knot - 1000*Curve.PARAM_TOL) and _t <= (knot + 1000*Curve.PARAM_TOL):
                _t2 = knot
                round = True

        if not round:
            if _t <= Curve.PARAM_TOL:
                left = None
                right = self
                return left, right
            if (1.0 - _t) <= Curve.PARAM_TOL:
                left = self
                right = None
                return left, right
        else:
            if _t2 <= Curve.PARAM_TOL:
                left = None
                right = self
                return left, right
            if (1.0 - _t2) <= Curve.PARAM_TOL:
                left = self
                right = None
                return left, right

        # Create two curve objects resulting from splitting
        left = GenericNurbs()
        right = GenericNurbs()

        # Create the corresponding NURBS curves resulting from splitting
        # if _t > 0.5 and _t <= (0.5 + Curve.PARAM_TOL):
        #     _t = 0.5
        # elif _t < 0.5 and _t >= (0.5 - Curve.PARAM_TOL):
        #     _t = 0.5
        #r = int(1.0 / Curve.PARAM_TOL)
        
        # decimals = int(math.log(1.0 / Curve.PARAM_TOL, 10))
        # _t = round(_t, decimals)

        if not round:
            try:
                left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
            except:
                pass
        else:
            left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t2)

        # try:
        #     left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
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

        # Generate equivalent polylines for each resulting curve
        lenOrig = self.length()
        tol = lenOrig * 0.001
        left.eqPoly = []
        left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, tol)
        ptLeftEnd = Pnt2D(left.nurbs.ctrlpts[-1][0], left.nurbs.ctrlpts[-1][1])
        left.eqPoly.append(ptLeftEnd)
        left.pt0 = Point(left.nurbs.ctrlpts[0][0], left.nurbs.ctrlpts[0][1])
        left.pt1 = Point(left.nurbs.ctrlpts[-1][0], left.nurbs.ctrlpts[-1][1])

        right.eqPoly = []
        right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, tol)
        ptRightEnd = Pnt2D(right.nurbs.ctrlpts[-1][0], right.nurbs.ctrlpts[-1][1])
        right.eqPoly.append(ptRightEnd)
        right.pt0 = Point(right.nurbs.ctrlpts[0][0], right.nurbs.ctrlpts[0][1])
        right.pt1 = Point(right.nurbs.ctrlpts[-1][0], right.nurbs.ctrlpts[-1][1])

        return left, right

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
    def getEquivPolyline(self, _tol):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.01 * L)
            ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
            self.eqPoly.append(ptEnd)

        return self.eqPoly

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
    def getInitPt(self):
        return self.pt0
    
    # ---------------------------------------------------------------------
    def getEndPt(self):
        return self.pt1

    # ---------------------------------------------------------------------
    def lengthInerpPts(self):
        L = 0.0
        for i in range(0, len(self.nurbs.ctrlpts) - 1):
            L += math.sqrt((self.nurbs.ctrlpts[i + 1][0] - self.nurbs.ctrlpts[i][0]) *
                           (self.nurbs.ctrlpts[i + 1][0] - self.nurbs.ctrlpts[i][0]) +
                           (self.nurbs.ctrlpts[i + 1][1] - self.nurbs.ctrlpts[i][1]) *
                           (self.nurbs.ctrlpts[i + 1][1] - self.nurbs.ctrlpts[i][1]))
        return L

    # ---------------------------------------------------------------------
    def length(self):
        length = operations.length_curve(self.nurbs)
        return length