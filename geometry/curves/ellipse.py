from compgeom.pnt2d import Pnt2D
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geometry.curves.ellipsearc import EllipseArc
from geomdl import NURBS
from geomdl import operations
import math


class Ellipse(Curve):
    def __init__(self, _center=None, _ellip1=None, _ellip2=None):
        super(Curve, self).__init__()
        self.type = 'ELLIPSE'
        self.center = _center
        self.ellip1 = _ellip1
        self.ellip2 = _ellip2
        self.nPts = 0
        self.axis1 = 0.0
        self.axis2 = 0.0
        self.ang1 = 0.0  # Angle of ellipse point (0 <= angle < +2PI)
        self.nurbs = []
        self.eqPoly = []

        if self.center is not None:
            self.nPts += 1

            if self.ellip1 is not None:
                # Compute first axis
                drX1 = self.ellip1.getX() - self.center.getX()
                drY1 = self.ellip1.getY() - self.center.getY()
                self.axis1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
                if self.axis1 > 0.0:

                    # Compute angle for the ellipse point
                    self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                    if self.ang1 < 0.0:
                        self.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI
                    self.nPts += 1

                    if self.ellip2 is not None:
                        # Compute second axis
                        axis1_vec = self.ellip1 - self.center
                        ellip2_vec = self.ellip2 - self.center
                        projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
                        self.axis2 = math.sqrt(abs(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1))
                        self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang1)
                        if self.axis2 > 0.0:
                            self.nPts += 1

                        # Nurbs control points
                        ctrlPts = []
                        ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY()))
                        ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() + self.axis2))
                        ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() + self.axis2))
                        ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() + self.axis2))
                        ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY()))
                        ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() - self.axis2))
                        ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() - self.axis2))
                        ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() - self.axis2))
                        ctrlPts.append(ctrlPts[0])

                        # Applying the rotation matrix
                        ctrlPtsValues =[]
                        for Pt in ctrlPts:
                            PtRotated = Pnt2D.rotate(Pt, self.center, self.ang1)
                            ctrlPtsValues.append([PtRotated.getX(), PtRotated.getY()])

                        # Nurbs weights
                        weights = [1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0),
                                    1, 1/math.sqrt(2.0), 1]

                        # Nurbs knot vector
                        knotVector = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]

                        # Creating Nurbs circle
                        self.nurbs = NURBS.Curve()
                        self.nurbs.degree = 2
                        self.nurbs.ctrlpts = ctrlPtsValues
                        self.nurbs.weights = weights
                        self.nurbs.knotvector = knotVector
                        self.nurbs.sample_size = 10

                        # Generating equivalent polyline
                        self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.axis1)
                        self.eqPoly.append(self.ellip1)

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
            refPtX = self.center.getX()
            refPtY = self.center.getY()
            if _LenAndAng:
                # Compute first axis
                drX = _x - self.center.getX()
                drY = _y - self.center.getY()
                len_axis1 = math.sqrt(drX * drX + drY * drY)
                v1 = len_axis1

                # Compute angle for the first axis
                ang1 = math.atan2(drY, drX)  # -PI < angle <= +PI
                if ang1 < 0.0:
                    ang1 += 2.0 * math.pi  # 0 <= angle < +2PI
                ang1 *= (180.0 / math.pi)
                v2 = ang1
            else:
                v1 = _x
                v2 = _y

        elif self.nPts == 2:
            refPtX = self.center.getX()
            refPtY = self.center.getY()
            # Compute second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = Pnt2D(_x, _y) - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            if _LenAndAng:
                len_axis2 = math.sqrt(abs(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1))
                v1 = len_axis2
                ang2 = self.ang1 * (180.0 / math.pi) + 90.0
                if ang2 > 360.0:
                    ang2 -= 360.0  # 0 <= angle < +2PI
                v2 = ang2
            else:
                ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang1)
                v1 = ellip2.getX()
                v2 = ellip2.getY()

        return refPtX, refPtY, v1, v2

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _v1, _v2, _LenAndAng):
        if self.nPts == 0:
            pt = Pnt2D(_v1, _v2)
            self.center = pt
            self.nPts += 1

        elif self.nPts == 1:
            if not _LenAndAng:
                pt = Pnt2D(_v1, _v2)
            else:
                dist = _v1
                ang = _v2 * (math.pi / 180.0)
                dX = dist * math.cos(ang)
                dY = dist * math.sin(ang)
                pt = Pnt2D(self.center.getX() + dX, self.center.getY() + dY)
            if Pnt2D.euclidiandistance(self.center, pt) <= Curve.COORD_TOL:
                return
            self.ellip1 = pt

            # Compute first axis
            drX1 = self.ellip1.getX() - self.center.getX()
            drY1 = self.ellip1.getY() - self.center.getY()
            self.axis1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.axis1 > 0.0:

                # Compute angle for the ellipse point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 = 2.0 * math.pi + self.ang1  # 0 <= angle < +2PI
                self.nPts += 1

        elif self.nPts == 2:
            if not _LenAndAng:
                pt = Pnt2D(_v1, _v2)
            else:
                dist = _v1
                ang = _v2 * (math.pi / 180.0)
                dX = dist * math.cos(ang)
                dY = dist * math.sin(ang)
                pt = Pnt2D(self.center.getX() + dX, self.center.getY() + dY)
            if Pnt2D.euclidiandistance(self.center, pt) <= Curve.COORD_TOL:
                return
            if Pnt2D.euclidiandistance(self.ellip1, pt) <= Curve.COORD_TOL:
                return
            self.ellip2 = pt

            # Compute second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = self.ellip2 - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            self.axis2 = math.sqrt(abs(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1))
            self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang1)
            if self.axis2 > 0.0:
                self.nPts += 1

            # Nurbs control points
            ctrlPts = []
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY()))
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY()))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() - self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() - self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() - self.axis2))
            ctrlPts.append(ctrlPts[0])

            # Applying the rotation matrix
            ctrlPtsValues =[]
            for Pt in ctrlPts:
                PtRotated = Pnt2D.rotate(Pt, self.center, self.ang1)
                ctrlPtsValues.append([PtRotated.getX(), PtRotated.getY()])

            # Nurbs weights
            weights = [1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0),
                        1, 1/math.sqrt(2.0), 1]

            # Nurbs knot vector
            knotVector = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]

            # Creating Nurbs circle
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = 2
            self.nurbs.ctrlpts = ctrlPtsValues
            self.nurbs.weights = weights
            self.nurbs.knotvector = knotVector
            self.nurbs.sample_size = 10

            # Generating equivalent polyline
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.axis1)
            self.eqPoly.append(self.ellip1)

    # ---------------------------------------------------------------------
    def isPossible(self):
        if self.nPts < 3:
            return False
        return True

    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        if self.nPts == 1:
            return [self.center, self.ellip1]
        elif self.nPts == 2:
            return [self.center, self.ellip1, self.ellip2]
        elif self.nPts == 3:
            return [self.center, self.ellip1, self.ellip2]

    # ---------------------------------------------------------------------
    def isStraight(self, _tol):
        return False

    # ---------------------------------------------------------------------
    def isClosed(self):
        return True

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t <= 0.0:
            return self.ellip1
        elif _t >= 1.0:
            return self.ellip1

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
        left = EllipseArc()
        right = EllipseArc()

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
        left_center = self.center
        left_ellip1 = self.ellip1
        left_ellip2 = self.ellip2
        left_arc1 = self.ellip1
        left_arc2 = pt

        # Right curve properties
        right_center = self.center
        right_ellip1 = self.ellip1
        right_ellip2 = self.ellip2
        right_arc1 = pt
        right_arc2 = self.ellip1

        # Create curve objects resulting from splitting
        left = EllipseArc(left_center, left_ellip1, left_ellip2, left_arc1, left_arc2)
        right = EllipseArc(right_center, right_ellip1, right_ellip2, right_arc1, right_arc2)
        return left, right

    # ---------------------------------------------------------------------
    def join(self, _joinCurve, _pt, _tol):
        return False, None, 'Cannot join segments:\n A closed curve may not be joined with another curve.'

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.axis1)
            self.eqPoly.append(self.ellip1)
        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []
        pt = Pnt2D(_pt.x, _pt.y)

        if self.nPts == 1:
            self.ellip1 = pt

            drX1 = self.ellip1.getX() - self.center.getX()
            drY1 = self.ellip1.getY() - self.center.getY()
            self.axis1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.axis1 > 0.0:

                # Compute angle for the ellipse point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI
                tempEqPoly = [self.ellip1, Pnt2D.rotate(self.ellip1, self.center, math.pi)]

        if self.nPts == 2:
            self.ellip2 = pt
            tempEqPoly = []

            # Compute second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = self.ellip2 - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            self.axis2 = math.sqrt(abs(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1))
            self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang1)

            # Nurbs control points
            ctrlPts = []
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY()))
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() + self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY()))
            ctrlPts.append(Pnt2D(self.center.getX() - self.axis1, self.center.getY() - self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX(), self.center.getY() - self.axis2))
            ctrlPts.append(Pnt2D(self.center.getX() + self.axis1, self.center.getY() - self.axis2))
            ctrlPts.append(ctrlPts[0])

            # Applying the rotation matrix
            ctrlPtsValues =[]
            for Pt in ctrlPts:
                PtRotated = Pnt2D.rotate(Pt, self.center, self.ang1)
                ctrlPtsValues.append([PtRotated.getX(), PtRotated.getY()])

            # Nurbs weights
            weights = [1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0), 1, 1/math.sqrt(2.0),
                        1, 1/math.sqrt(2.0), 1]

            # Nurbs knot vector
            knotVector = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]

            # Creating Nurbs ellipse
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = 2
            self.nurbs.ctrlpts = ctrlPtsValues
            self.nurbs.weights = weights
            self.nurbs.knotvector = knotVector
            self.nurbs.sample_size = 10

            # Generating equivalent polyline
            tempEqPoly = Curve.genEquivPolyline(self, tempEqPoly, 0.005 * self.axis1)
            tempEqPoly.append(self.ellip1)
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
        if t <= 0.0:
            t = 0.0
            seg = 0
            clstPt = self.eqPoly[seg]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
            status = True
        elif t >= 1.0:
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
    def getPntInit(self):
        pt = Pnt2D(self.nurbs.ctrlpts[0][0], self.nurbs.ctrlpts[0][1])
        return pt

    # ---------------------------------------------------------------------
    def getPntEnd(self):
        pt = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
        return pt

    # ---------------------------------------------------------------------
    def length(self):
        L = operations.length_curve(self.nurbs)
        return L
    
    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        data = {'center': [self.center.getX(), self.center.getY()],
                'ellip1': [self.ellip1.getX(), self.ellip1.getY()],
                'ellip2': [self.ellip2.getX(), self.ellip2.getY()]}
        return data
