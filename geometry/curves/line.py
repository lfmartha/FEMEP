from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geomdl import NURBS
from geomdl import knotvector
from geomdl import operations


class Line(Curve):
    def __init__(self, _pt0=None, _pt1=None):
        super(Curve, self).__init__()
        self.type = 'LINE'
        self.pt0 = _pt0
        self.pt1 = _pt1
        self.nPts = 0
        self.nurbs = []
        
        if _pt0 is not None:
            self.nPts += 1

            if _pt1 is not None:
                self.nPts += 1

                if self.nPts >= 2:
                    # Nurbs control points
                    crvPts =[[self.pt0.getX(), self.pt0.getY()], [self.pt1.getX(), self.pt1.getY()]]

                    # Creating Nurbs line
                    self.nurbs = NURBS.Curve()
                    self.nurbs.degree = 1
                    self.nurbs.ctrlpts = crvPts
                    self.nurbs.knotvector = knotvector.generate(self.nurbs.degree, self.nurbs.ctrlpts_size)
                    self.nurbs.sample_size = 10

    # ---------------------------------------------------------------------
    def setPoints(self, _x0, _y0, _x1, _y1):
        self.pt0 = Pnt2D(_x0, _y0)
        self.pt1 = Pnt2D(_x1, _y1)
        self.nPts = 2

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        pt = Pnt2D(_x, _y)

        if self.nPts == 0:
            self.pt0 = pt
            self.nPts += 1

        elif self.nPts == 1:
            self.pt1 = pt
            self.nPts += 1

            if self.nPts >= 2:
                # Nurbs control points
                crvPts =[[self.pt0.getX(), self.pt0.getY()], [self.pt1.getX(), self.pt1.getY()]]

                # Creating Nurbs line
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 1
                self.nurbs.ctrlpts = crvPts
                self.nurbs.knotvector = knotvector.generate(self.nurbs.degree, self.nurbs.ctrlpts_size)
                self.nurbs.sample_size = 10

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t > 1.0:
            _t = 1.0
        elif _t <= 0.0:
            _t = 0.0

        vx = self.pt1.getX() - self.pt0.getX()
        vy = self.pt1.getY() - self.pt0.getY()
        if _t < 0.0:
            xOn = self.pt0.getX()
            yOn = self.pt0.getY()
        elif _t > 1.0:
            xOn = self.pt1.getX()
            yOn = self.pt1.getY()
        else:
            xOn = self.pt0.getX() + _t * vx
            yOn = self.pt0.getY() + _t * vy
        return Pnt2D(xOn, yOn)

    # ---------------------------------------------------------------------
    def evalPointTangent(self, _t):
        if _t > 1.0:
            _t = 1.0
        elif _t <= 0.0:
            _t = 0.0
            
        pt = self.evalPoint(_t)
        tangVec = self.pt1 - self.pt0
        return pt, tangVec

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
    def getCtrlPoints(self):
        tempPts = []
        if self.nPts == 0:
            return tempPts
        if self.nPts == 1:
            tempPts.append(self.pt0)
            return tempPts
        tempPts.append(self.pt0)
        tempPts.append(self.pt1)
        return tempPts

    # ---------------------------------------------------------------------
    def setCtrlPoint(self, _id, _x, _y, _tol):
        if self.nPts != 2:
            return False
        pt = Pnt2D(_x, _y)
        if _id == 0:
            if Pnt2D.euclidiandistance(pt, self.pt1) <= _tol:
                return False
            self.pt0.setCoords(_x, _y)
            return True
        if _id == 1:
            if Pnt2D.euclidiandistance(pt, self.pt0) <= _tol:
                return False
            self.pt1.setCoords(_x, _y)
            return True
        return False

    # ---------------------------------------------------------------------
    def isStraight(self, _tol):
        return True

    # ---------------------------------------------------------------------
    def isClosed(self):
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
        left = Line()
        right = Line()

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

        pt = self.evalPoint(_t)

        left.pt0 = self.pt0
        left.pt1 = pt

        right.pt0 = pt
        right.pt1 = self.pt1

        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        equivPoly = []
        if (_tEnd - _tInit) <= Curve.PARAM_TOL:
            return equivPoly

        if _tInit <= Curve.PARAM_TOL:
            ptInit = self.pt0
        elif (1.0 - _tInit) <= Curve.PARAM_TOL:
            return equivPoly
        else:
            ptInit = self.evalPoint(_tInit)

        if _tEnd <= Curve.PARAM_TOL:
            return equivPoly
        elif (1.0 - _tEnd) <= Curve.PARAM_TOL:
            ptEnd = self.pt1
        else:
            ptEnd = self.evalPoint(_tEnd)

        equivPoly.append(ptInit)
        equivPoly.append(ptEnd)
        return equivPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempPts = []
        tempPts.append(self.pt0)
        if self.nPts == 2:
            tempPts.append(self.pt1)
        elif self.nPts == 1:
            tempPts.append(_pt)
        return tempPts

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        p0 = self.pt0
        p1 = self.pt1
        pt = Pnt2D(_x, _y)
        dist, clstPt, t = CompGeom.getClosestPointSegment(p0, p1, pt)
        tangVec = self.pt1 - self.pt0
        return True, clstPt, dist, t, tangVec

    # ---------------------------------------------------------------------
    def closestPointParam(self, _x, _y, _tStart):
        clstPt, tangVec = self.evalPointTangent(_tStart)
        if ((abs(clstPt.getX() - _x) < Curve.COORD_TOL) and
            (abs(clstPt.getY() - _y) < Curve.COORD_TOL)):
            return True, clstPt, 0.0, _tStart, tangVec

        status, clstPt, dist, t, tangVec = self.closestPoint(_x, _y)
        return status, clstPt, dist, t, tangVec

    # ---------------------------------------------------------------------
    def getBoundBox(self):
        xmax = max(self.pt0.getX(), self.pt1.getX())
        xmin = min(self.pt0.getX(), self.pt1.getX())
        ymax = max(self.pt0.getY(), self.pt1.getY())
        ymin = min(self.pt0.getY(), self.pt1.getY())
        return xmin, xmax, ymin, ymax

    # ---------------------------------------------------------------------
    def getXinit(self):
        return self.pt0.getX()

    # ---------------------------------------------------------------------
    def getYinit(self):
        return self.pt0.getY()

    # ---------------------------------------------------------------------
    def getXend(self):
        return self.pt1.getX()

    # ---------------------------------------------------------------------
    def getYend(self):
        return self.pt1.getY()

    # ---------------------------------------------------------------------
    def length(self, _tInit, _tEnd):
        L = Pnt2D.euclidiandistance(self.pt0,self.pt1)
        len = L * (_tEnd - _tInit)
        return len
