from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import fitting
from geomdl import convert
from geomdl import operations
from geomdl import NURBS
import numpy as np
import math


class EllipseArc(Curve):
    def __init__(self, _center=None, _ellip1=None, _ellip2=None, _arc1=None, _arc2=None):
        super(Curve, self).__init__()
        self.type = 'ELLIPSEARC'
        self.center = _center
        self.ellip1 = _ellip1
        self.ellip2 = _ellip2
        self.arc1 = _arc1
        self.arc2 = _arc2
        self.nPts = 0
        self.axis1 = 0.0
        self.axis2 = 0.0
        self.ang = 0.0  # Angle of first axis (0 <= angle < +2PI)
        self.ang1 = 0.0  # Angle of first arc point (0 <= angle < +2PI)
        self.ang2 = 0.0  # Angle of second arc point (0 <= angle < +2PI)
        self.TeoAng1 = 0.0
        self.TeoAng2 = 0.0
        self.nurbs = []
        self.eqPoly = []

        if self.center is not None:
            self.nPts += 1

            if self.ellip1 is not None:
                # Compute first axis
                drX = self.ellip1.getX() - self.center.getX()
                drY = self.ellip1.getY() - self.center.getY()
                self.axis1 = math.sqrt(drX * drX + drY * drY)
                if self.axis1 > 0.0:

                    # Compute angle for first axis
                    self.ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                    if self.ang < 0.0:
                        self.ang += 2.0 * math.pi  # 0 <= angle < +2PI
                    self.nPts += 1

                    if self.ellip2 is not None:
                        # Compute and snap second axis
                        axis1_vec = self.ellip1 - self.center
                        ellip2_vec = self.ellip2 - self.center
                        projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
                        self.axis2 = math.sqrt(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1)
                        self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang)
                        if self.axis2 > 0.0:
                            self.nPts += 1

                            # Compute first arc point
                            if self.arc1 is not None:
                                drX1 = self.arc1.getX() - self.center.getX()
                                drY1 = self.arc1.getY() - self.center.getY()
                                dist1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
                                if dist1 > 0.0:

                                    # Compute angle for first arc point
                                    self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                                    if self.ang1 < 0.0:
                                        self.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    # Snap first arc point to ellipse
                                    teta1 = self.ang1 - self.ang
                                    if teta1 < 0:
                                        teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    eta1 = self.theoreticalAngle(teta1)
                                    x1 = self.center.getX() + self.axis1 * math.cos(eta1) * math.cos(self.ang) - self.axis2 * math.sin(eta1) * math.sin(self.ang)
                                    y1 = self.center.getY() + self.axis1 * math.cos(eta1) * math.sin(self.ang) + self.axis2 * math.sin(eta1) * math.cos(self.ang)
                                    self.TeoAng1 = eta1 + self.ang
                                    self.arc1 = Pnt2D(x1, y1)
                                    self.nPts += 1

                                    # Compute second arc point
                                    if self.arc2 is not None:
                                        drX2 = self.arc2.getX() - self.center.getX()
                                        drY2 = self.arc2.getY() - self.center.getY()
                                        dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                                        if dist2 > 0.0:

                                            # Compute angle for second arc point
                                            self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                                            if self.ang2 < 0.0:
                                                self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            # Snap second arc point to ellipse
                                            teta2 = self.ang2 - self.ang
                                            if teta2 < 0:
                                                teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            eta2 = self.theoreticalAngle(teta2)
                                            x2 = self.center.getX() + self.axis1 * math.cos(eta2) * math.cos(self.ang) - self.axis2 * math.sin(eta2) * math.sin(self.ang)
                                            y2 = self.center.getY() + self.axis1 * math.cos(eta2) * math.sin(self.ang) + self.axis2 * math.sin(eta2) * math.cos(self.ang)
                                            self.TeoAng2 = eta2 + self.ang
                                            self.arc2 = Pnt2D(x2, y2)
                                            self.nPts += 1

                                            # Angle between arc points
                                            teta = self.TeoAng2 - self.TeoAng1
                                            if teta < 0:
                                                teta += 2.0 * math.pi  # 0 <= angle < +2PI

                                            # Quadrants and knot vector
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

                                            # Unit circle control points and weights
                                            ctrlPts = []
                                            weights = []

                                            if quad >= 1:
                                                if quad > 1:
                                                    tetaQ1 = teta / quad
                                                else:
                                                    tetaQ1 = teta
                                                r = 1.0
                                                d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1))
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + tetaQ1 / 2.0))
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ1))
                                                weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                                            if quad >= 2:
                                                if quad > 2:
                                                    tetaQ2 = tetaQ1 + teta / quad
                                                else:
                                                    tetaQ2 = teta
                                                r = 1.0
                                                d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ2 + tetaQ1) / 2.0))
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ2))
                                                weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                                            if quad >= 3:
                                                if quad > 3:
                                                    tetaQ3 = tetaQ2 + teta / quad
                                                else:
                                                    tetaQ3 = teta
                                                r = 1.0
                                                d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ3 + tetaQ2) / 2.0))
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ3))
                                                weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                                            if quad == 4:
                                                tetaQ4 = teta
                                                r = 1.0
                                                d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ4 + tetaQ3) / 2.0))
                                                ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ4))
                                                weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                                            # Unit circle to Ellipse
                                            ctrlPtsValues = []
                                            for Pt in ctrlPts:
                                                # Rotate unit circle control points
                                                Pt = Pnt2D.rotate(Pt, self.center, -self.ang)
                                                Pt = np.array([[Pt.getX()], [Pt.getY()], [1.0]])

                                                # Translate to origin, apply the ellipse transformation and translate back to original location
                                                T2 = np.array([[1.0, 0.0, self.center.getX()], [0.0, 1.0, self.center.getY()], [0.0, 0.0, 1.0]])
                                                CircToEllip = np.array([[self.axis1, 0.0, 0.0], [0.0, self.axis2, 0.0], [0.0, 0.0, 1.0]])
                                                T1 = np.array([[1.0, 0.0, -1.0 * self.center.getX()], [0.0, 1.0, -1.0 * self.center.getY()], [0.0, 0.0, 1.0]])
                                                Pt = T2@CircToEllip@T1@Pt

                                                # Rotate ellipse control points
                                                Pt = Pnt2D(Pt[0][0], Pt[1][0])
                                                Pt = Pnt2D.rotate(Pt, self.center, self.ang)
                                                ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                                            # Creating Nurbs ellipse arc
                                            self.nurbs = NURBS.Curve()
                                            self.nurbs.degree = 2
                                            self.nurbs.ctrlpts = ctrlPtsValues
                                            self.nurbs.weights = weights
                                            self.nurbs.knotvector = knotVector
                                            self.nurbs.sample_size = 10

                                            # Generating equivalent polyline
                                            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * self.axis1)
                                            self.eqPoly.append(self.arc2)

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
            self.ellip1 = pt

            # Compute first axis
            drX = self.ellip1.getX() - self.center.getX()
            drY = self.ellip1.getY() - self.center.getY()
            self.axis1 = math.sqrt(drX * drX + drY * drY)
            if self.axis1 > 0.0:

                # Compute angle for first axis
                self.ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                if self.ang < 0.0:
                    self.ang += 2.0 * math.pi  # 0 <= angle < +2PI
                self.nPts += 1

        elif self.nPts == 2:
            closeToOther = False
            if Pnt2D.euclidiandistance(self.center, pt) <= 0.01:
                closeToOther = True
            if Pnt2D.euclidiandistance(self.ellip1, pt) <= 0.01:
                closeToOther = True
            if closeToOther:
                return
            self.ellip2 = pt

            # Compute and snap second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = self.ellip2 - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            self.axis2 = math.sqrt(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1)
            self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang)
            if self.axis2 > 0.0:
                self.nPts += 1

        elif self.nPts == 3:
            closeToOther = False
            if Pnt2D.euclidiandistance(self.center, pt) <= 0.01:
                closeToOther = True
            if closeToOther:
                return
            self.arc1 = pt

            # Compute first arc point
            drX1 = self.arc1.getX() - self.center.getX()
            drY1 = self.arc1.getY() - self.center.getY()
            dist1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if dist1 > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Snap first arc point to ellipse
                teta1 = self.ang1 - self.ang
                if teta1 < 0:
                    teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

                eta1 = self.theoreticalAngle(teta1)
                x1 = self.center.getX() + self.axis1 * math.cos(eta1) * math.cos(self.ang) - self.axis2 * math.sin(eta1) * math.sin(self.ang)
                y1 = self.center.getY() + self.axis1 * math.cos(eta1) * math.sin(self.ang) + self.axis2 * math.sin(eta1) * math.cos(self.ang)
                self.TeoAng1 = eta1 + self.ang
                self.arc1 = Pnt2D(x1, y1)
                self.nPts += 1

        elif self.nPts == 4:
            closeToOther = False
            if Pnt2D.euclidiandistance(self.center, pt) <= 0.01:
                closeToOther = True
            if Pnt2D.euclidiandistance(self.arc1, pt) <= 0.01:
                closeToOther = True
            if closeToOther:
                return
            self.arc2 = pt

            # Compute second arc point
            drX2 = self.arc2.getX() - self.center.getX()
            drY2 = self.arc2.getY() - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
            if dist2 > 0.0:

                # Compute angle for second arc point
                self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                if self.ang2 < 0.0:
                    self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Snap second arc point to ellipse
                teta2 = self.ang2 - self.ang
                if teta2 < 0:
                    teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

                eta2 = self.theoreticalAngle(teta2)
                x2 = self.center.getX() + self.axis1 * math.cos(eta2) * math.cos(self.ang) - self.axis2 * math.sin(eta2) * math.sin(self.ang)
                y2 = self.center.getY() + self.axis1 * math.cos(eta2) * math.sin(self.ang) + self.axis2 * math.sin(eta2) * math.cos(self.ang)
                self.TeoAng2 = eta2 + self.ang
                self.arc2 = Pnt2D(x2, y2)
                self.nPts += 1

                # Angle between arc points
                teta = self.TeoAng2 - self.TeoAng1
                if teta < 0:
                    teta += 2.0 * math.pi  # 0 <= angle < +2PI

                # Quadrants and knot vector
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

                # Unit circle control points and weights
                ctrlPts = []
                weights = []

                if quad >= 1:
                    if quad > 1:
                        tetaQ1 = teta / quad
                    else:
                        tetaQ1 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + tetaQ1 / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ1))
                    weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                if quad >= 2:
                    if quad > 2:
                        tetaQ2 = tetaQ1 + teta / quad
                    else:
                        tetaQ2 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ4 + tetaQ3) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ4))
                    weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                # Unit circle to Ellipse
                ctrlPtsValues = []
                for Pt in ctrlPts:
                    # Rotate unit circle control points
                    Pt = Pnt2D.rotate(Pt, self.center, -self.ang)
                    Pt = np.array([[Pt.getX()], [Pt.getY()], [1.0]])

                    # Translate to origin, apply the ellipse transformation and translate back to original location
                    T2 = np.array([[1.0, 0.0, self.center.getX()], [0.0, 1.0, self.center.getY()], [0.0, 0.0, 1.0]])
                    CircToEllip = np.array([[self.axis1, 0.0, 0.0], [0.0, self.axis2, 0.0], [0.0, 0.0, 1.0]])
                    T1 = np.array([[1.0, 0.0, -1.0 * self.center.getX()], [0.0, 1.0, -1.0 * self.center.getY()], [0.0, 0.0, 1.0]])
                    Pt = T2@CircToEllip@T1@Pt

                    # Rotate ellipse control points
                    Pt = Pnt2D(Pt[0][0], Pt[1][0])
                    Pt = Pnt2D.rotate(Pt, self.center, self.ang)
                    ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                # Creating Nurbs ellipse arc
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 2
                self.nurbs.ctrlpts = ctrlPtsValues
                self.nurbs.weights = weights
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

                # Generating equivalent polyline
                self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * self.axis1)
                self.eqPoly.append(self.arc2)

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
        if self.nPts < 5:
            return False
        return True

    # ---------------------------------------------------------------------
    def isUnlimited(self):
        return False

    # ---------------------------------------------------------------------
    def getCtrlPoints(self):
        if self.nPts == 1:
            return [self.center, self.ellip1]
        elif self.nPts == 2:
            return [self.center, self.ellip1, self.ellip2]
        elif self.nPts == 3:
            return [self.center, self.ellip1, self.ellip2, self.arc1]
        else:
            return [self.center, self.ellip1, self.ellip2, self.arc1, self.arc2]

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
        left = EllipseArc()
        right = EllipseArc()

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
        left.ellip1 = self.ellip1
        left.ellip2 = self.ellip2
        left.arc1 = self.arc1
        left.arc2 = pt

        if left.center is not None:
            left.nPts += 1

            if left.ellip1 is not None:
                # Compute first axis
                drX = left.ellip1.getX() - left.center.getX()
                drY = left.ellip1.getY() - left.center.getY()
                left.axis1 = math.sqrt(drX * drX + drY * drY)
                if left.axis1 > 0.0:

                    # Compute angle for first axis
                    left.ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                    if left.ang < 0.0:
                        left.ang += 2.0 * math.pi  # 0 <= angle < +2PI
                    left.nPts += 1

                    if left.ellip2 is not None:
                        # Compute and snap second axis
                        axis1_vec = left.ellip1 - left.center
                        ellip2_vec = left.ellip2 - left.center
                        projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
                        left.axis2 = math.sqrt(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1)
                        left.ellip2 = Pnt2D.rotate(Pnt2D(left.center.getX(), left.center.getY() + left.axis2), left.center, left.ang)
                        if left.axis2 > 0.0:
                            left.nPts += 1

                            # Compute first arc point
                            if left.arc1 is not None:
                                drX1 = left.arc1.getX() - left.center.getX()
                                drY1 = left.arc1.getY() - left.center.getY()
                                dist1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
                                if dist1 > 0.0:

                                    # Compute angle for first arc point
                                    left.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                                    if left.ang1 < 0.0:
                                        left.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    # Snap first arc point to ellipse
                                    teta1 = left.ang1 - left.ang
                                    if teta1 < 0:
                                        teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    eta1 = left.theoreticalAngle(teta1)
                                    x1 = left.center.getX() + left.axis1 * math.cos(eta1) * math.cos(left.ang) - left.axis2 * math.sin(eta1) * math.sin(left.ang)
                                    y1 = left.center.getY() + left.axis1 * math.cos(eta1) * math.sin(left.ang) + left.axis2 * math.sin(eta1) * math.cos(left.ang)
                                    left.TeoAng1 = eta1 + left.ang
                                    left.arc1 = Pnt2D(x1, y1)
                                    left.nPts += 1

                                    # Compute second arc point
                                    if left.arc2 is not None:
                                        drX2 = left.arc2.getX() - left.center.getX()
                                        drY2 = left.arc2.getY() - left.center.getY()
                                        dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                                        if dist2 > 0.0:

                                            # Compute angle for second arc point
                                            left.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                                            if left.ang2 < 0.0:
                                                left.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            # Snap second arc point to ellipse
                                            teta2 = left.ang2 - left.ang
                                            if teta2 < 0:
                                                teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            eta2 = left.theoreticalAngle(teta2)
                                            x2 = left.center.getX() + left.axis1 * math.cos(eta2) * math.cos(left.ang) - left.axis2 * math.sin(eta2) * math.sin(left.ang)
                                            y2 = left.center.getY() + left.axis1 * math.cos(eta2) * math.sin(left.ang) + left.axis2 * math.sin(eta2) * math.cos(left.ang)
                                            left.TeoAng2 = eta2 + left.ang
                                            left.arc2 = Pnt2D(x2, y2)
                                            left.nPts += 1

                                            # Generating equivalent polyline
                                            left.eqPoly = []
                                            left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, 0.001 * left.axis1)
                                            left.eqPoly.append(left.arc2)

        right.center = self.center
        right.ellip1 = self.ellip1
        right.ellip2 = self.ellip2
        right.arc1 = pt
        right.arc2 = self.arc2

        if right.center is not None:
            right.nPts += 1

            if right.ellip1 is not None:
                # Compute first axis
                drX = right.ellip1.getX() - right.center.getX()
                drY = right.ellip1.getY() - right.center.getY()
                right.axis1 = math.sqrt(drX * drX + drY * drY)
                if right.axis1 > 0.0:

                    # Compute angle for first axis
                    right.ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                    if right.ang < 0.0:
                        right.ang += 2.0 * math.pi  # 0 <= angle < +2PI
                    right.nPts += 1

                    if right.ellip2 is not None:
                        # Compute and snap second axis
                        axis1_vec = right.ellip1 - right.center
                        ellip2_vec = right.ellip2 - right.center
                        projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
                        right.axis2 = math.sqrt(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1)
                        right.ellip2 = Pnt2D.rotate(Pnt2D(right.center.getX(), right.center.getY() + right.axis2), right.center, right.ang)
                        if right.axis2 > 0.0:
                            right.nPts += 1

                            # Compute first arc point
                            if right.arc1 is not None:
                                drX1 = right.arc1.getX() - right.center.getX()
                                drY1 = right.arc1.getY() - right.center.getY()
                                dist1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
                                if dist1 > 0.0:

                                    # Compute angle for first arc point
                                    right.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                                    if right.ang1 < 0.0:
                                        right.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    # Snap first arc point to ellipse
                                    teta1 = right.ang1 - right.ang
                                    if teta1 < 0:
                                        teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

                                    eta1 = right.theoreticalAngle(teta1)
                                    x1 = right.center.getX() + right.axis1 * math.cos(eta1) * math.cos(right.ang) - right.axis2 * math.sin(eta1) * math.sin(right.ang)
                                    y1 = right.center.getY() + right.axis1 * math.cos(eta1) * math.sin(right.ang) + right.axis2 * math.sin(eta1) * math.cos(right.ang)
                                    right.TeoAng1 = eta1 + right.ang
                                    right.arc1 = Pnt2D(x1, y1)
                                    right.nPts += 1

                                    # Compute second arc point
                                    if right.arc2 is not None:
                                        drX2 = right.arc2.getX() - right.center.getX()
                                        drY2 = right.arc2.getY() - right.center.getY()
                                        dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
                                        if dist2 > 0.0:

                                            # Compute angle for second arc point
                                            right.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                                            if right.ang2 < 0.0:
                                                right.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            # Snap second arc point to ellipse
                                            teta2 = right.ang2 - right.ang
                                            if teta2 < 0:
                                                teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

                                            eta2 = right.theoreticalAngle(teta2)
                                            x2 = right.center.getX() + right.axis1 * math.cos(eta2) * math.cos(right.ang) - right.axis2 * math.sin(eta2) * math.sin(right.ang)
                                            y2 = right.center.getY() + right.axis1 * math.cos(eta2) * math.sin(right.ang) + right.axis2 * math.sin(eta2) * math.cos(right.ang)
                                            right.TeoAng2 = eta2 + right.ang
                                            right.arc2 = Pnt2D(x2, y2)
                                            right.nPts += 1

                                            # Generating equivalent polyline
                                            right.eqPoly = []
                                            right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, 0.001 * right.axis1)
                                            right.eqPoly.append(right.arc2)

        return left, right

    # ---------------------------------------------------------------------
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, _tol)
            self.eqPoly.append(self.arc2)

        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []
        pt = Pnt2D(_pt.x, _pt.y)

        if self.nPts == 1:
            self.ellip1 = pt

            # Compute first axis
            drX = self.ellip1.getX() - self.center.getX()
            drY = self.ellip1.getY() - self.center.getY()
            self.axis1 = math.sqrt(drX * drX + drY * drY)
            if self.axis1 > 0.0:

                # Compute angle for first axis
                self.ang = math.atan2(drY, drX)  # -PI < angle <= +PI
                if self.ang < 0.0:
                    self.ang += 2.0 * math.pi  # 0 <= angle < +2PI
                tempEqPoly = [self.ellip1, Pnt2D.rotate(self.ellip1, self.center, math.pi)]

        if self.nPts == 2:
            self.ellip2 = pt
            tempEqPoly = []

            # Compute and snap second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = self.ellip2 - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            self.axis2 = math.sqrt(abs(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1))
            self.ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang)

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
                PtRotated = Pnt2D.rotate(Pt, self.center, self.ang)
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
            tempEqPoly = Curve.genEquivPolyline(self, tempEqPoly, 0.001 * self.axis1)
            tempEqPoly.append(self.ellip1)

        if self.nPts == 3:
            self.arc1 = pt
            tempEqPoly = []

            # Compute first arc point
            drX1 = self.arc1.getX() - self.center.getX()
            drY1 = self.arc1.getY() - self.center.getY()
            dist1 = math.sqrt(drX1 * drX1 + drY1 * drY1)
            if dist1 > 0.0:

                # Compute angle for first arc point
                self.ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if self.ang1 < 0.0:
                    self.ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Snap first arc point to ellipse
                teta1 = self.ang1 - self.ang
                if teta1 < 0:
                    teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

                eta1 = self.theoreticalAngle(teta1)
                x1 = self.center.getX() + self.axis1 * math.cos(eta1) * math.cos(self.ang) - self.axis2 * math.sin(eta1) * math.sin(self.ang)
                y1 = self.center.getY() + self.axis1 * math.cos(eta1) * math.sin(self.ang) + self.axis2 * math.sin(eta1) * math.cos(self.ang)
                self.TeoAng1 = eta1 + self.ang
                self.arc1 = Pnt2D(x1, y1)
                tempEqPoly = [self.center, self.arc1]

        if self.nPts == 4:
            self.arc2 = pt
            tempEqPoly = []

            # Compute second arc point
            drX2 = self.arc2.getX() - self.center.getX()
            drY2 = self.arc2.getY() - self.center.getY()
            dist2 = math.sqrt(drX2 * drX2 + drY2 * drY2)
            if dist2 > 0.0:

                # Compute angle for second arc point
                self.ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
                if self.ang2 < 0.0:
                    self.ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

                # Snap second arc point to ellipse
                teta2 = self.ang2 - self.ang
                if teta2 < 0:
                    teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

                eta2 = self.theoreticalAngle(teta2)
                x2 = self.center.getX() + self.axis1 * math.cos(eta2) * math.cos(self.ang) - self.axis2 * math.sin(eta2) * math.sin(self.ang)
                y2 = self.center.getY() + self.axis1 * math.cos(eta2) * math.sin(self.ang) + self.axis2 * math.sin(eta2) * math.cos(self.ang)
                self.TeoAng2 = eta2 + self.ang
                self.arc2 = Pnt2D(x2, y2)

                # Angle between arc points
                teta = self.TeoAng2 - self.TeoAng1
                if teta < 0:
                    teta += 2.0 * math.pi  # 0 <= angle < +2PI

                # Quadrants and knot vector
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

                # Unit circle control points and weights
                ctrlPts = []
                weights = []

                if quad >= 1:
                    if quad > 1:
                        tetaQ1 = teta / quad
                    else:
                        tetaQ1 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - tetaQ1 / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + tetaQ1 / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ1))
                    weights.extend([1.0, math.cos(tetaQ1 / 2.0), 1.0])

                if quad >= 2:
                    if quad > 2:
                        tetaQ2 = tetaQ1 + teta / quad
                    else:
                        tetaQ2 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ2 - tetaQ1) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ2 + tetaQ1) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ2))
                    weights.extend([math.cos((tetaQ2 - tetaQ1) / 2.0), 1.0])

                if quad >= 3:
                    if quad > 3:
                        tetaQ3 = tetaQ2 + teta / quad
                    else:
                        tetaQ3 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ3 - tetaQ2) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ3 + tetaQ2) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ3))
                    weights.extend([math.cos((tetaQ3 - tetaQ2) / 2.0), 1.0])

                if quad == 4:
                    tetaQ4 = teta
                    r = 1.0
                    d = r / math.sin(math.pi / 2.0 - (tetaQ4 - tetaQ3) / 2.0)
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + d, self.center.getY()), self.center, self.TeoAng1 + (tetaQ4 + tetaQ3) / 2.0))
                    ctrlPts.append(Pnt2D.rotate(Pnt2D(self.center.getX() + r, self.center.getY()), self.center, self.TeoAng1 + tetaQ4))
                    weights.extend([math.cos((tetaQ4 - tetaQ3) / 2.0), 1.0])

                # Unit circle to Ellipse
                ctrlPtsValues = []
                for Pt in ctrlPts:
                    # Rotate unit circle control points
                    Pt = Pnt2D.rotate(Pt, self.center, -self.ang)
                    Pt = np.array([[Pt.getX()], [Pt.getY()], [1.0]])

                    # Translate to origin, apply the ellipse transformation and translate back to original location
                    T2 = np.array([[1.0, 0.0, self.center.getX()], [0.0, 1.0, self.center.getY()], [0.0, 0.0, 1.0]])
                    CircToEllip = np.array([[self.axis1, 0.0, 0.0], [0.0, self.axis2, 0.0], [0.0, 0.0, 1.0]])
                    T1 = np.array([[1.0, 0.0, -1.0 * self.center.getX()], [0.0, 1.0, -1.0 * self.center.getY()], [0.0, 0.0, 1.0]])
                    Pt = T2@CircToEllip@T1@Pt

                    # Rotate ellipse control points
                    Pt = Pnt2D(Pt[0][0], Pt[1][0])
                    Pt = Pnt2D.rotate(Pt, self.center, self.ang)
                    ctrlPtsValues.append([Pt.getX(), Pt.getY()])

                # Creating Nurbs ellipse arc
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = 2
                self.nurbs.ctrlpts = ctrlPtsValues
                self.nurbs.weights = weights
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

                # Generating equivalent polyline
                tempEqPoly = Curve.genEquivPolyline(self, tempEqPoly, 0.001 * self.axis1)
                tempEqPoly.append(self.arc2)

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
    def length(self, _tInit, _tEnd):
        length = operations.length_curve(self.nurbs)
        return length

    # ---------------------------------------------------------------------
    def theoreticalAngle(self, ang):
        eta = math.atan2(math.sin(ang) / self.axis2, math.cos(ang) / self.axis1)
        return eta

    # ---------------------------------------------------------------------
    def LenCenterToPt(self, ang):
        # This method receives an angle in degrees and returns the distance
        # between the ellipse point and its center
        ang *= math.pi / 180.0
        teta1 = ang - self.ang
        if teta1 < 0:
            teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

        len = self.axis1 * self.axis2 / math.sqrt(self.axis1 ** 2 * math.sin(teta1) ** 2 + self.axis2 ** 2 * math.cos(teta1) ** 2)
        return len

    # ---------------------------------------------------------------------
    def updateLineEditValues(self, _x, _y, _LenAndAng):
        if self.nPts == 1:
            if _LenAndAng:
                # Compute first axis
                drX1 = _x - self.center.getX()
                drY1 = _y - self.center.getY()
                len_axis1 = math.sqrt(drX1 * drX1 + drY1 * drY1)

                # Compute angle for the first axis
                ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
                if ang1 < 0.0:
                    ang1 += 2.0 * math.pi  # 0 <= angle < +2PI
                ang1 *= (180.0 / math.pi)
                return len_axis1, ang1

            else:
                return _x, _y

        elif self.nPts == 2:
            # Compute second axis
            axis1_vec = self.ellip1 - self.center
            ellip2_vec = Pnt2D(_x, _y) - self.center
            projeInAxis1 = Pnt2D.dotprod(ellip2_vec, axis1_vec) / Pnt2D.size(axis1_vec)
            if _LenAndAng:
                len_axis2 = math.sqrt(Pnt2D.sizesquare(ellip2_vec) - projeInAxis1 * projeInAxis1)
                ang2 = self.ang * (180.0 / math.pi) + 90.0
                if ang2 > 360.0:
                    ang2 -= 360.0  # 0 <= angle < +2PI
                return len_axis2, ang2

            else:
                ellip2 = Pnt2D.rotate(Pnt2D(self.center.getX(), self.center.getY() + self.axis2), self.center, self.ang)
                return ellip2.getX(), ellip2.getY()

        elif self.nPts == 3:
            # Compute angle for the first arc point
            drX1 = _x - self.center.getX()
            drY1 = _y - self.center.getY()

            ang1 = math.atan2(drY1, drX1)  # -PI < angle <= +PI
            if ang1 < 0.0:
                ang1 += 2.0 * math.pi  # 0 <= angle < +2PI

            teta1 = ang1 - self.ang
            if teta1 < 0:
                teta1 += 2.0 * math.pi  # 0 <= angle < +2PI

            if _LenAndAng:
                # Compute length for the first arc point
                len1 = self.axis1 * self.axis2 / math.sqrt(self.axis1 ** 2 * math.sin(teta1) ** 2 + self.axis2 ** 2 * math.cos(teta1) ** 2)

                ang1 *= (180.0 / math.pi)
                return len1, ang1

            else:  
                # Snap first arc point to ellipse
                eta1 = self.theoreticalAngle(teta1)
                x1 = self.center.getX() + self.axis1 * math.cos(eta1) * math.cos(self.ang) - self.axis2 * math.sin(eta1) * math.sin(self.ang)
                y1 = self.center.getY() + self.axis1 * math.cos(eta1) * math.sin(self.ang) + self.axis2 * math.sin(eta1) * math.cos(self.ang)
                return x1, y1

        elif self.nPts == 4:
            # Compute angle for the second arc point
            drX2 = _x - self.center.getX()
            drY2 = _y - self.center.getY()

            ang2 = math.atan2(drY2, drX2)  # -PI < angle <= +PI
            if ang2 < 0.0:
                ang2 += 2.0 * math.pi  # 0 <= angle < +2PI

            teta2 = ang2 - self.ang
            if teta2 < 0:
                teta2 += 2.0 * math.pi  # 0 <= angle < +2PI

            if _LenAndAng:
                # Compute length for the second arc point
                len2 = self.axis1 * self.axis2 / math.sqrt(self.axis1 ** 2 * math.sin(teta2) ** 2 + self.axis2 ** 2 * math.cos(teta2) ** 2)

                ang2 *= (180.0 / math.pi)
                return len2, ang2

            else:  
                # Snap second arc point to ellipse
                eta2 = self.theoreticalAngle(teta2)
                x2 = self.center.getX() + self.axis1 * math.cos(eta2) * math.cos(self.ang) - self.axis2 * math.sin(eta2) * math.sin(self.ang)
                y2 = self.center.getY() + self.axis1 * math.cos(eta2) * math.sin(self.ang) + self.axis2 * math.sin(eta2) * math.cos(self.ang)
                return x2, y2
