from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import NURBS
from geomdl import operations
import math


class CircleArc(Curve):
    def __init__(self, _center=None, _circ1=None, _circ2=None):
        super(Curve, self).__init__()
        self.type = 'CIRCLEARC'
        self.center = _center
        self.circ1 = _circ1
        self.circ2 = _circ2
        self.nPts = 0
        self.radius = 0.0
        self.ang1 = 0.0  # Angle of pirst arc point (0 <= angle < +2PI)
        self.ang2 = 0.0  # Angle of second arc point (0 <= angle < +2PI)
        self.nurbs = []
        self.eqPoly = []

        if self.center is not None:
            self.nPts += 1

        if self.circ1 is not None:
            # Compute radius
            drX1 = self.circ1.getX() - self.center.getX()
            drY1 = self.circ1.getY() - self.center.getY()
            self.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.radius > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 = 2.0 * math.pi + self.ang1  # 0 <= angle < +2PI
                self.nPts += 1

                if self.circ2 is not None:
                    drX2 = self.circ2.getX() - self.center.getX()
                    drY2 = self.circ2.getY() - self.center.getY()
                    dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                    if dist2 > 0.0:

                        # Snap second arc point to circle
                        tRadius = self.radius / dist2
                        x2 = self.center.getX() + tRadius * drX2
                        y2 = self.center.getY() + tRadius * drY2
                        self.circ2.setCoords(x2, y2)

                        # Compute angle for second arc point
                        self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                        if self.ang2 <= 0.0:
                            self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI
                        self.nPts += 1

                        # Quadrants and knot vector
                        teta = self.ang2 - self.ang1
                        if teta <= 0.0:
                            teta += 2.0 * math.pi  # 0 <= angle < +2PI

                        if teta > 0.0 and teta <= (math.pi / 2.0 + Curve.COORD_TOL):
                            quad = 1
                            knotVector = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
                        elif teta > (math.pi / 2.0 + Curve.COORD_TOL) and teta <= (math.pi + Curve.COORD_TOL):
                            quad = 2
                            knotVector = [0.0, 0.0, 0.0, 1/2, 1/2, 1.0, 1.0, 1.0]
                        elif teta > (math.pi + Curve.COORD_TOL) and teta <= (3.0 / 2.0 * math.pi + Curve.COORD_TOL):
                            quad = 3
                            knotVector = [0.0, 0.0, 0.0, 1/3, 1/3, 2/3, 2/3, 1.0, 1.0, 1.0]
                        else:
                            quad = 4
                            knotVector = [0.0, 0.0, 0.0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1.0, 1.0, 1.0]

                        # Nurbs control points, weights and knot vector
                        ctrlPts = []
                        weights = []

                        if quad >= 1:
                            if quad > 1:
                                #tetaQ1 = math.pi / 2.0
                                tetaQ1 = teta / quad
                            else:
                                tetaQ1 = teta
                            r = self.radius
                            d = r / math.cos(tetaQ1 / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + tetaQ1 / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ1))
                            weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                        if quad >= 2:
                            if quad > 2:
                                tetaQ2 = tetaQ1 + teta / quad
                            else:
                                tetaQ2 = teta
                            r = self.radius
                            d = r / math.cos((tetaQ2 - tetaQ1) / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                            weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                        if quad >= 3:
                            if quad > 3:
                                tetaQ3 = tetaQ2 + teta / quad
                            else:
                                tetaQ3 = teta
                            r = self.radius
                            d = r / math.cos((tetaQ3 - tetaQ2) / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                            weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                        if quad == 4:
                            tetaQ4 = teta
                            r = self.radius
                            d = r / math.cos((tetaQ4 - tetaQ3) / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ4 + tetaQ3) / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ4))
                            weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                        ctrlPtsValues = []
                        for Pt in ctrlPts:
                            ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                        # Creating Nurbs circle
                        self.nurbs = NURBS.Curve()
                        self.nurbs.degree = 2
                        self.nurbs.ctrlpts = ctrlPtsValues
                        self.nurbs.weights = weights
                        self.nurbs.knotvector = knotVector
                        self.nurbs.sample_size = 10

                        # Generating equivalent polyline
                        self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.radius)
                        self.eqPoly.append(self.circ2)

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
                # Compute radius
                drX1 = _x - self.center.getX()
                drY1 = _y - self.center.getY()
                radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
                v1 = radius

                # Compute angle for first arc point
                ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
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
            # Compute angle for second arc point
            drX2 = _x - self.center.getX()
            drY2 = _y - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)

            ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
            if ang2 < 0.0:
                ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

            if _LenAndAng:
                radius = self.radius
                v1 = radius
                ang2 *= (180.0 / math.pi)
                v2 = ang2
            else:
                # Snap second arc point to circle
                if dist2 > 0.0:
                    tRadius = self.radius / dist2
                    v1 = self.center.getX() + tRadius * drX2
                    v2 = self.center.getY() + tRadius * drY2
                else:
                    v1 = self.circ1.getX()
                    v2 = self.circ1.getY()

        return refPtX, refPtY, v1, v2

    # ---------------------------------------------------------------------
    def buildCurve(self, _v1, _v2, _LenAndAng):
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
            self.circ1 = pt
            self.nPts += 1

            # Compute radius
            drX1 = self.circ1.getX() - self.center.getX()
            drY1 = self.circ1.getY() - self.center.getY()
            self.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.radius > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 = 2.0 * math.pi + self.ang1  # 0 <= angle < +2PI

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
            if Pnt2D.euclidiandistance(self.circ1, pt) <= Curve.COORD_TOL:
                return
            self.circ2 = pt
            self.nPts += 1

            drX2 = self.circ2.getX() - self.center.getX()
            drY2 = self.circ2.getY() - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
            if dist2 > 0.0:

                # Snap second arc point to circle
                tRadius = self.radius / dist2
                x2 = self.center.getX() + tRadius * drX2
                y2 = self.center.getY() + tRadius * drY2
                self.circ2.setCoords(x2, y2)

                # Compute angle for second arc point
                self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                if self.ang2 <= 0.0:
                    self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Quadrants and knot vector
                teta = self.ang2 - self.ang1
                if teta <= 0.0:
                    teta += 2.0 * math.pi  # 0 <= angle < +2PI

                if teta > 0.0 and teta <= (math.pi / 2.0 + Curve.COORD_TOL):
                    quad = 1
                    knotVector = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
                elif teta > (math.pi / 2.0 + Curve.COORD_TOL) and teta <= (math.pi + Curve.COORD_TOL):
                    quad = 2
                    knotVector = [0.0, 0.0, 0.0, 1/2, 1/2, 1.0, 1.0, 1.0]
                elif teta > (math.pi + Curve.COORD_TOL) and teta <= (3.0 / 2.0 * math.pi + Curve.COORD_TOL):
                    quad = 3
                    knotVector = [0.0, 0.0, 0.0, 1/3, 1/3, 2/3, 2/3, 1.0, 1.0, 1.0]
                else:
                    quad = 4
                    knotVector = [0.0, 0.0, 0.0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1.0, 1.0, 1.0]

                # Nurbs control points, weights and knot vector
                ctrlPts = []
                weights = []

                if quad >= 1:
                    if quad > 1:
                        tetaQ1 = teta / quad
                    else:
                        tetaQ1 = teta
                    r = self.radius
                    d = r / math.cos(tetaQ1 / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + tetaQ1 / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ1))
                    weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                if quad >= 2:
                    if quad > 2:
                        tetaQ2 = tetaQ1 + teta / quad
                    else:
                        tetaQ2 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ4 - tetaQ3) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ4 + tetaQ3) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ4))
                    weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                ctrlPtsValues = []
                for Pt in ctrlPts:
                    ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                # Creating Nurbs circle
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 2
                self.nurbs.ctrlpts = ctrlPtsValues
                self.nurbs.weights = weights
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

                # Generating equivalent polyline
                self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.radius)
                self.eqPoly.append(self.circ2)

    # ---------------------------------------------------------------------
    def isPossible(self):
        if self.nPts < 3:
            return False
        return True

    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        if self.nPts == 1:
            return [self.center, self.circ1]
        else:
            return [self.center, self.circ1, self.circ2]

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
        return False

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t <= 0.0:
            return self.circ1
        elif _t >= 1.0:
            return self.circ2

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
        left = CircleArc()
        right = CircleArc()

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
        left_circ1 = self.circ1
        left_circ2 = pt

        # Right curve properties
        right_center = self.center
        right_circ1 = pt
        right_circ2 = self.circ2

        # Create curve objects resulting from splitting
        left = CircleArc(left_center, left_circ1, left_circ2)
        right = CircleArc(right_center, right_circ1, right_circ2)
        return left, right
                
    # ---------------------------------------------------------------------
    def join(self, _joinCurve, _pt, _tol):
        if _joinCurve.getType() != 'CIRCLEARC':
            return False, None, 'Cannot join segments:\n A CIRCLEARC curve may be joined only with another CIRCLEARC.'

        curv1 = self
        curv2 = _joinCurve

        # check if the circle arcs have the same center point, according 
        # to a given tolerance
        tol = Pnt2D(_tol, _tol)
        if Pnt2D.equal(curv1.center, curv2.center, tol):
            curv_center = (curv1.center + curv2.center) / 2.0
        else:
            return False, None, 'Cannot join segments:\n Circle arcs must have the same center point.'

        # check if the circle arcs radius are equal, according to a given
        # tolerance
        if abs(curv1.radius - curv2.radius) <= _tol:
            curv_radius = (curv1.radius + curv2.radius) / 2.0
        else:
            return False, None, 'Cannot join segments:\n Circle arcs must have the same radius.'

        # check curves initial point
        if Pnt2D.equal(Pnt2D(curv1.nurbs.ctrlpts[0][0], curv1.nurbs.ctrlpts[0][1]), _pt, tol):
            init_pt1 = True
        else:
            init_pt1 = False

        if Pnt2D.equal(Pnt2D(curv2.nurbs.ctrlpts[0][0], curv2.nurbs.ctrlpts[0][1]), _pt, tol):
            init_pt2 = True
        else:
            init_pt2 = False

        # circle arc properties
        if init_pt1 and not init_pt2:
            curv_ang1 = curv2.ang1
            curv_ang2 = curv1.ang2

        elif not init_pt1 and init_pt2:
            curv_ang1 = curv1.ang1
            curv_ang2 = curv2.ang2

        curv_circ1 = Pnt2D.rotate(Pnt2D(curv_center.getX() + curv_radius, curv_center.getY()), curv_center, curv_ang1)
        curv_circ2 = Pnt2D.rotate(Pnt2D(curv_center.getX() + curv_radius, curv_center.getY()), curv_center, curv_ang2)

        curv = CircleArc(curv_center, curv_circ1, curv_circ2)
        return True, curv, None

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.005 * self.radius)
            self.eqPoly.append(self.circ2)
        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []

        if self.nPts == 1:
            self.circ1 = Pnt2D(_pt.x, _pt.y)

            # Compute radius
            drX1 = self.circ1.getX() - self.center.getX()
            drY1 = self.circ1.getY() - self.center.getY()
            self.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.radius > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 = 2.0 * math.pi + self.ang1  # 0 <= angle < +2PI
                tempEqPoly = [self.center, self.circ1]

        if self.nPts == 2:
            self.circ2 = Pnt2D(_pt.x, _pt.y)
            tempEqPoly = []

            drX2 = self.circ2.getX() - self.center.getX()
            drY2 = self.circ2.getY() - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
            if dist2 > 0.0:

                # Snap second arc point to circle
                tRadius = self.radius / dist2
                x2 = self.center.getX() + tRadius * drX2
                y2 = self.center.getY() + tRadius * drY2
                self.circ2.setCoords(x2, y2)

                # Compute angle for second arc point
                self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                if self.ang2 <= 0.0:
                    self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Quadrants and knot vector
                teta = self.ang2 - self.ang1
                if teta <= 0.0:
                    teta += 2.0 * math.pi  # 0 <= angle < +2PI

                if teta > 0.0 and teta <= (math.pi / 2.0 + Curve.COORD_TOL):
                    quad = 1
                    knotVector = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
                elif teta > (math.pi / 2.0 + Curve.COORD_TOL) and teta <= (math.pi + Curve.COORD_TOL):
                    quad = 2
                    knotVector = [0.0, 0.0, 0.0, 1/2, 1/2, 1.0, 1.0, 1.0]
                elif teta > (math.pi + Curve.COORD_TOL) and teta <= (3.0 / 2.0 * math.pi + Curve.COORD_TOL):
                    quad = 3
                    knotVector = [0.0, 0.0, 0.0, 1/3, 1/3, 2/3, 2/3, 1.0, 1.0, 1.0]
                else:
                    quad = 4
                    knotVector = [0.0, 0.0, 0.0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1.0, 1.0, 1.0]

                # Nurbs control points, weights and knot vector
                ctrlPts = []
                weights = []

                if quad >= 1:
                    if quad > 1:
                        tetaQ1 = teta / quad
                    else:
                        tetaQ1 = teta
                    r = self.radius
                    d = r / math.cos(tetaQ1 / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + tetaQ1 / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ1))
                    weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                if quad >= 2:
                    if quad > 2:
                        tetaQ2 = tetaQ1 + teta / quad
                    else:
                        tetaQ2 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = self.radius
                    d = r / math.cos((tetaQ4 - tetaQ3) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ4 + tetaQ3) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ4))
                    weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                ctrlPtsValues = []
                for Pt in ctrlPts:
                    ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                # Creating Nurbs circle
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 2
                self.nurbs.ctrlpts = ctrlPtsValues
                self.nurbs.weights = weights
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

                # Generating equivalent polyline
                tempEqPoly = Curve.genEquivPolyline(self, tempEqPoly, 0.005 * self.radius)
                tempEqPoly.append(self.circ2)
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
        if (t > - 10000 * Curve.PARAM_TOL) and (t < 10000 * Curve.PARAM_TOL):
            t = 0.0
            seg = 0
            clstPt = self.eqPoly[seg]
            tang = self.eqPoly[seg + 1] - self.eqPoly[seg]
            status = True
        elif (t > 1.0 - 10000 * Curve.PARAM_TOL) and (t < 1.0 + 10000 * Curve.PARAM_TOL):
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
        teta = self.ang2 - self.ang1
        if teta <= 0.0:
            teta += 2.0 * math.pi  # 0 <= angle < +2PI
        L = teta * self.radius
        return L
    
    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        data = {'center': [self.center.getX(), self.center.getY()],
                'circ1': [self.circ1.getX(), self.circ1.getY()],
                'circ2': [self.circ2.getX(), self.circ2.getY()]}
        return data
