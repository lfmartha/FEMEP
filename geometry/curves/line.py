from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geomdl import NURBS
from geomdl import operations
from geomdl import knotvector
import math


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
    def isUnlimited(self):
        return False

    # ---------------------------------------------------------------------
    def updateCollectingPntInfo(self, _x, _y, _LenAndAng):
        if self.nPts == 0:
            refPtX = None
            refPtY = None
            v1 = _x
            v2 = _y

        elif self.nPts == 1:
            refPtX = self.pt0.getX()
            refPtY = self.pt0.getY()
            if _LenAndAng:
                # Compute radius
                drX = _x - refPtX
                drY = _y - refPtY
                radius = math.sqrt(drX * drX + drY * drY)
                v1 = radius

                # Compute angle
                ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                if ang < 0.0:
                    ang += 2.0 * math.pi  # 0 <= angle < +2PI
                ang *= (180.0 / math.pi)
                v2 = ang
            else:
                v1 = _x
                v2 = _y

        return refPtX, refPtY, v1, v2

    # ---------------------------------------------------------------------
    def buildCurve(self, _v1, _v2, _LenAndAng):
        if self.nPts == 0:
            pt = Pnt2D(_v1, _v2)
            self.pt0 = pt
            self.nPts += 1

        elif self.nPts == 1:
            if not _LenAndAng:
                pt = Pnt2D(_v1, _v2)
            else:
                dist = _v1
                ang = _v2 * (math.pi / 180.0)
                dX = dist * math.cos(ang)
                dY = dist * math.sin(ang)
                pt = Pnt2D(self.pt0.getX() + dX, self.pt0.getY() + dY)
            if Pnt2D.euclidiandistance(self.pt0, pt) <= Curve.COORD_TOL:
                return

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
    def isPossible(self):
        if self.nPts < 2:
            return False
        return True
    
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
            
        ders = self.nurbs.derivatives(_t, order=1)
        pt = ders[0]
        tang = ders[1]
        return Pnt2D(pt[0], pt[1]), Pnt2D(tang[0], tang[1])

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
    def join(self, _joinCurve, _pt, _tol):
        if _joinCurve.getType() == 'POLYLINE':
            status, curv, error_text = _joinCurve.join(self, _pt, _tol)
            return status, curv, error_text
        elif _joinCurve.getType() != 'LINE':
            return False, None, 'Cannot join segments:\n A LINE curve may be joined only with a LINE or a POLYLINE.'

        # Order the points of the two curves. The first curve is always
        # the self.
        # It is assumed that the given point _pt is the common point of
        # the curves to be joined.
        selfPtInit = self.getPntInit()
        selfPtEnd = self.getPntEnd()
        otherPtInit = _joinCurve.getPntInit()
        otherPtEnd = _joinCurve.getPntEnd()
        if ((Pnt2D.euclidiandistance(selfPtEnd, _pt) < _tol) and
            (Pnt2D.euclidiandistance(otherPtEnd, _pt) < _tol)):
            ptInit = selfPtInit
            ptMid = selfPtEnd
            ptEnd = otherPtInit
        elif ((Pnt2D.euclidiandistance(selfPtInit, _pt) < _tol) and
              (Pnt2D.euclidiandistance(otherPtInit, _pt) < _tol)):
            ptInit = selfPtEnd
            ptMid = selfPtInit
            ptEnd = otherPtEnd
        elif ((Pnt2D.euclidiandistance(selfPtInit, _pt) < _tol) and
              (Pnt2D.euclidiandistance(otherPtEnd, _pt) < _tol)):
            ptInit = selfPtEnd
            ptMid = selfPtInit
            ptEnd = otherPtInit
        else: # default: self is left and other is right
            ptInit = selfPtInit
            ptMid = selfPtEnd
            ptEnd = otherPtEnd

        # Check to see whether the three points form a straight line.
        # In which case, create a LINE curve. Otherwise, do not allow joinding.
        if CompGeom.pickLine(ptInit, ptEnd, ptMid, _tol):
            curv = Line(ptInit, ptEnd)
        else:
            return False, None, 'Cannot join segments:\n LINE curves must be collinear.'

        return True, curv, None

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
    def getPntInit(self):
        return self.pt0
        return pt

    # ---------------------------------------------------------------------
    def getPntEnd(self):
        return self.pt1
        return pt

    # ---------------------------------------------------------------------
    def length(self):
        L = Pnt2D.euclidiandistance(self.pt0, self.pt1)
        return L

    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        data = {'pt0': [self.pt0.getX(), self.pt0.getY()],
                'pt1': [self.pt1.getX(), self.pt1.getY()]}
        return data
