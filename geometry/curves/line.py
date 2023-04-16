from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geomdl import NURBS
from geomdl import operations
from geomdl import knotvector


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

                    # Nurbs knot vector
                    knotvector = [0.0, 0.0, 1.0, 1.0]

                    # Creating Nurbs line
                    self.nurbs = NURBS.Curve()
                    self.nurbs.degree = 1
                    self.nurbs.ctrlpts = crvPts
                    self.nurbs.knotvector = knotvector
                    self.nurbs.sample_size = 10

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

                # Nurbs knot vector
                knotvector = [0.0, 0.0, 1.0, 1.0]

                # Creating Nurbs line
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 1
                self.nurbs.ctrlpts = crvPts
                self.nurbs.knotvector = knotvector
                self.nurbs.sample_size = 10

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t < 0.0:
            _t = 0.0
        elif _t > 1.0:
            _t = 1.0

        v = self.pt1 - self.pt0
        pt = self.pt0 +  v * _t
        return pt

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
    def isUnlimited(self):
        return False
    
    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        return [self.pt0, self.pt1]

    # ---------------------------------------------------------------------
    def isStraight(self, _tol):
        return True

    # ---------------------------------------------------------------------
    def isClosed(self):
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
        left = Line()
        right = Line()

        # Create the corresponding NURBS curves resulting from splitting
        left.nurbs, right.nurbs = operations.split_curve(self.nurbs, _t)
        return left, right

    # ---------------------------------------------------------------------
    def split(self, _t):
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

        pt = self.evalPoint(_t)

        # Left curve properties
        left_pt0 = self.pt0
        left_pt1 = pt

        # Right curve properties
        right_pt0 = pt
        right_pt1 = self.pt1

        # Create curve objects resulting from splitting
        left = Line(left_pt0, left_pt1)
        right = Line(right_pt0, right_pt1)
        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        equivPoly = [self.pt0, self.pt1]
        return equivPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempPts = []
        if self.nPts == 1:
            self.pt1 = Pnt2D(_pt.x, _pt.y)
            tempPts.append(self.pt0)
            tempPts.append(self.pt1)
        return tempPts

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        pt = Pnt2D(_x, _y)
        dist, clstPt, t = CompGeom.getClosestPointSegment(self.pt0, self.pt1, pt)
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
    def getInitPt(self):
        return self.pt0
    
    # ---------------------------------------------------------------------
    def getEndPt(self):
        return self.pt1

    # ---------------------------------------------------------------------
    def length(self):
        L = Pnt2D.euclidiandistance(self.pt0, self.pt1)
        return L
    
    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        data = {'pt0': [self.pt0.getX(), self.pt0.getY()],
                'pt1': [self.pt1.getX(), self.pt1.getY()]}
        return data