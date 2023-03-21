from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import fitting
from geomdl import convert
from geomdl import operations
from geomdl import NURBS
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
                            d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
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
                            d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                            weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                        if quad >= 3:
                            if quad > 3:
                                tetaQ3 = tetaQ2 + teta / quad
                            else:
                                tetaQ3 = teta
                            r = self.radius
                            d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                            ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                            weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                        if quad == 4:
                            tetaQ4 = teta
                            r = self.radius
                            d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
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
                        self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.0001 * self.radius)
                        self.eqPoly.append(self.circ2)

    # ---------------------------------------------------------------------
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        if not _LenAndAng:
            pt = Pnt2D(_x, _y)
        else:
            len = _x
            ang = _y * (math.pi / 180.0)
            dX = len * math.cos(ang)
            dY = len * math.sin(ang)
            pt = Pnt2D(self.center.getX() + dX, self.center.getY() + dY)
            
        if self.nPts == 0:
            self.center = pt
            self.nPts += 1

        elif self.nPts == 1:
            closeToOther = False
            if Pnt2D.euclidiandistance(self.center, pt) <= 0.01:
                closeToOther = True
            if closeToOther:
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
            closeToOther = False
            if Pnt2D.euclidiandistance(self.center, pt) <= 0.01:
                closeToOther = True
            if Pnt2D.euclidiandistance(self.circ1, pt) <= 0.01:
                closeToOther = True
            if closeToOther:
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
                    d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
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
                    d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
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
                self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.0001 * self.radius)
                self.eqPoly.append(self.circ2)

    # ---------------------------------------------------------------------
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
    def evalPointCurvature(self, _t):
        pt = self.evalPoint(_t)
        CurvVec = 0.0
        return pt, CurvVec

    # ---------------------------------------------------------------------
    def isPossible(self):
        if self.nPts < 3:
            return False
        return True

    # ---------------------------------------------------------------------
    def isUnlimited(self):
        return False

    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        if self.nPts == 1:
            return [self.center, self.circ1]
        else:
            return [self.center, self.circ1, self.circ2]

    # ---------------------------------------------------------------------
    def setCtrlPoint(self, _id, _x, _y, _tol):
        if self.nPts != 2:
            return False
        pt = Pnt2D(_x, _y)

        if _id == 0:
            deltaX1 = _x - self.center.getX()
            deltaY1 = _y - self.center.getY()
            deltaX2 = _x - self.center.getX()
            deltaY2 = _x - self.center.getY()
            circ1X = self.circ1.getX()
            circ1Y = self.circ1.getY()
            circ2X = self.circ2.getX()
            circ2Y = self.circ2.getY()
            self.center = pt
            self.circ1 = Pnt2D(circ1X + deltaX1, circ1Y + deltaY1)
            self.circ2 = Pnt2D(circ2X + deltaX2, circ2Y + deltaY2)
            return True

        if _id == 1:
            if Pnt2D.euclidiandistance(pt, self.center) <= _tol:
                return False
            self.circ1 = pt

            # Compute radius
            drX1 = self.circ1.getX() - self.center.getX()
            drY1 = self.circ1.getY() - self.center.getY()
            self.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if self.radius > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 = 2.0 * math.pi + self.ang1  # 0 <= angle < +2PI

        if _id == 2:
            if Pnt2D.euclidiandistance(pt, self.circ1) <= _tol:
                return False
            self.circ2 = pt

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
                    d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
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
                    d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
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
                self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.0001 * self.radius)
                self.eqPoly.append(self.circ2)

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
        left = CircleArc()
        right = CircleArc()

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

        left.center = self.center
        left.circ1 = self.circ1
        left.circ2 = pt

        if left.center is not None:
            left.nPts += 1

        if left.circ1 is not None:
            # Compute radius
            drX1 = left.circ1.getX() - left.center.getX()
            drY1 = left.circ1.getY() - left.center.getY()
            left.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if left.radius > 0.0:

                # Compute angle for first arc point
                left.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if left.ang1 < 0.0:
                    left.ang1 = 2.0 * math.pi + left.ang1  # 0 <= angle < +2PI
                left.nPts += 1

                if left.circ2 is not None:
                    drX2 = left.circ2.getX() - left.center.getX()
                    drY2 = left.circ2.getY() - left.center.getY()
                    dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                    if dist2 > 0.0:

                        # Snap second arc point to circle
                        tRadius = left.radius / dist2
                        x2 = left.center.getX() + tRadius * drX2
                        y2 = left.center.getY() + tRadius * drY2
                        left.circ2.setCoords(x2, y2)

                        # Compute angle for second arc point
                        left.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                        if left.ang2 <= 0.0:
                            left.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI
                        left.nPts += 1

                        # Generating equivalent polyline
                        left.eqPoly = []
                        left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, 0.0001 * left.radius)
                        left.eqPoly.append(left.circ2)

        right.center = self.center
        right.circ1 = pt
        right.circ2 = self.circ2

        if right.center is not None:
            right.nPts += 1

        if right.circ1 is not None:
            # Compute radius
            drX1 = right.circ1.getX() - right.center.getX()
            drY1 = right.circ1.getY() - right.center.getY()
            right.radius = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if right.radius > 0.0:

                # Compute angle for first arc point
                right.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if right.ang1 < 0.0:
                    right.ang1 = 2.0 * math.pi + right.ang1  # 0 <= angle < +2PI
                right.nPts += 1

                if right.circ2 is not None:
                    drX2 = right.circ2.getX() - right.center.getX()
                    drY2 = right.circ2.getY() - right.center.getY()
                    dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                    if dist2 > 0.0:

                        # Snap second arc point to circle
                        tRadius = right.radius / dist2
                        x2 = right.center.getX() + tRadius * drX2
                        y2 = right.center.getY() + tRadius * drY2
                        right.circ2.setCoords(x2, y2)

                        # Compute angle for second arc point
                        right.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                        if right.ang2 <= 0.0:
                            right.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI
                        right.nPts += 1

                        # Generating equivalent polyline
                        right.eqPoly = []
                        right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, 0.0001 * right.radius)
                        right.eqPoly.append(right.circ2)

        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, _tol)
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
                    d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
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
                    d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.ang1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.ang1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = self.radius
                    d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
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
                tempEqPoly = Curve.genEquivPolyline(self, tempEqPoly, 0.0001 * self.radius)
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
    def length(self, _tInit, _tEnd):
        ptInit = self.evalPoint(_tInit)
        drXInit = ptInit.getX() - self.center.getX()
        drYInit = ptInit.getY() - self.center.getY()
        angInit = math.atan2(drYInit, drXInit) # between -pi and pi
        if angInit < 0.0:
            angInit += 2.0 * math.pi # between 0 and 2pi

        ptEnd = self.evalPoint(_tEnd)
        drXEnd = ptEnd.getX() - self.center.getX()
        drYEnd = ptEnd.getY() - self.center.getY()
        angEnd = math.atan2(drYEnd, drXEnd)  # between -pi and pi
        if angEnd < 0.0:
            angEnd += 2.0 * math.pi # between 0 and 2pi

        # Arc angle range
        angRange = angEnd - angInit
        if angRange <= 0:
            angRange += 2.0 * math.pi

        # Length
        length = angRange * self.radius

        return length

    # ---------------------------------------------------------------------
    def updateLineEditValues(self, _x, _y, _LenAndAng):
        if self.nPts == 1:
            if _LenAndAng:
                # Compute radius
                drX1 = _x - self.center.getX()
                drY1 = _y - self.center.getY()
                radius = math.sqrt(drX1 * drX1 + drY1 * drY1)

                # Compute angle for first arc point
                ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if ang1 < 0.0:
                    ang1 += 2.0 * math.pi  # 0 <= angle < +2PI
                ang1 *= (180.0 / math.pi)
                return radius, ang1

            else:
                return _x, _y

        elif self.nPts == 2:
            # Compute angle for second arc point
            drX2 = _x - self.center.getX()
            drY2 = _y - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)

            ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
            if ang2 < 0.0:
                ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

            if _LenAndAng:
                radius = self.radius
                ang2 *= (180.0 / math.pi)
                return radius, ang2

            else:
                # Snap second arc point to circle
                if dist2 > 0.0:
                    tRadius = self.radius / dist2
                    x2 = self.center.getX() + tRadius * drX2
                    y2 = self.center.getY() + tRadius * drY2
                    return x2, y2
                else:
                    return self.circ1.getX(), self.circ1.getY()
