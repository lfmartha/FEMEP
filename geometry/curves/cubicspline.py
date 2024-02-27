from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import NURBS
from geomdl import knotvector
from geomdl import operations
from geomdl import fitting
from geomdl import convert
import math


class CubicSpline(Curve):
    def __init__(self, degree=None, ctrlpts=None, weights=None, knotvector=None):
        super(Curve, self).__init__()
        self.type = 'CUBICSPLINE'
        self.pts = []
        self.nPts = 0
        self.nurbs = None
        self.eqPoly = []

        if (degree is not None and ctrlpts is not None and weights is not None and 
            knotvector is not None):

            # Creating Nurbs
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = degree
            self.nurbs.ctrlpts = ctrlpts
            self.nurbs.weights = weights
            self.nurbs.knotvector = knotvector
            self.nurbs.sample_size = 10

            # Generating equivalent polyline
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
            self.eqPoly.append(ptEnd)

    # ---------------------------------------------------------------------
    def isUnlimited(self):
        return True

    # ---------------------------------------------------------------------
    def updateCollectingPntInfo(self, _x, _y, _LenAndAng):
        if self.nPts == 0:
            refPtX = None
            refPtY = None
            v1 = _x
            v2 = _y

        else:
            refPtX = self.pts[-1].getX()
            refPtY = self.pts[-1].getY()
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
            self.pts = [pt]
            self.nPts += 1

        else:
            if not _LenAndAng:
                pt = Pnt2D(_v1, _v2)
            else:
                dist = _v1
                ang = _v2 * (math.pi / 180.0)
                dX = dist * math.cos(ang)
                dY = dist * math.sin(ang)
                pt = Pnt2D(self.pts[-1].getX() + dX, self.pts[-1].getY() + dY)
            for i in range(0, self.nPts):
                if Pnt2D.euclidiandistance(self.pts[i], pt) <= Curve.COORD_TOL:
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
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = degree
            self.nurbs.ctrlpts = ctrlPts
            self.nurbs.knotvector = knotvector.generate(self.nurbs.degree, self.nurbs.ctrlpts_size)
            # spline = fitting.interpolate_curve(ctrlPts, degree)
            # self.nurbs = convert.bspline_to_nurbs(spline)
            self.nurbs.sample_size = 10

            # Generating equivalent polyline
            self.eqPoly = []
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            self.eqPoly.append(self.pts[-1])

    # ---------------------------------------------------------------------
    def isPossible(self):
        if self.nPts < 2:
            return False
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
        L_left = left.lengthInerpPts()
        left.eqPoly = Curve.genEquivPolyline(left, left.eqPoly, 0.001 * L_left)
        ptLeftEnd = Pnt2D(left.nurbs.ctrlpts[-1][0], left.nurbs.ctrlpts[-1][1])
        left.eqPoly.append(ptLeftEnd)
        
        L_right = right.lengthInerpPts()
        right.eqPoly = Curve.genEquivPolyline(right, right.eqPoly, 0.001 * L_right)
        ptRightEnd = Pnt2D(right.nurbs.ctrlpts[-1][0], right.nurbs.ctrlpts[-1][1])
        right.eqPoly.append(ptRightEnd)
        return left, right

    # ---------------------------------------------------------------------
    def join(self, _joinCurve, _pt, _tol):
        if _joinCurve.getType() != 'CUBICSPLINE':
            return False, None, 'Cannot join segments:\n A CUBICSPLINE curve may be joined only with another CUBICSPLINE.'

        curv1 = self
        curv2 = _joinCurve

        if curv1.nurbs.degree == curv2.nurbs.degree:
            degree = curv1.nurbs.degree
        else:
            error_text = "Both CUBICSPLINE curves must have the same degree."
            return False, None, error_text

        curv1_ctrlpts = curv1.nurbs.ctrlpts
        curv2_ctrlpts = curv2.nurbs.ctrlpts
        curv1_knotvector = curv1.nurbs.knotvector
        curv2_knotvector = curv2.nurbs.knotvector
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
        
        L1 = curv1.length()
        L2 = curv2.length()
        L = (L1 + L2) / 2.0
        curv.eqPoly = Curve.genEquivPolyline(curv, curv.eqPoly, 0.001 * L)
        curv.eqPoly.append(Pnt2D(curv.nurbs.ctrlpts[-1][0], curv.nurbs.ctrlpts[-1][1]))

        return True, curv, None

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        # If current curve does not have yet an equivalent polyline,
        # generate it.
        if self.eqPoly == []:
            L = self.lengthInerpPts()
            self.eqPoly = Curve.genEquivPolyline(self, self.eqPoly, 0.001 * L)
            ptEnd = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
            self.eqPoly.append(ptEnd)
        return self.eqPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempEqPoly = []
        pt = Pnt2D(_pt.x, _pt.y)

        pts = []
        pts.extend(self.pts)
        if pt != self.pts[-1]:
            pts.append(pt)

        # Nurbs degree and control points
        if len(pts) == 1:
            return pts
        elif len(pts) == 2:
            return pts
        elif len(pts) == 3:
            degree = 2
        elif len(pts) > 3:
            degree = 3

        ctrlPts = []
        for p in pts:
            ctrlPts.append([p.getX(), p.getY()])

        # Creating Nurbs
        cubic_spline = CubicSpline()
        # spline = fitting.interpolate_curve(ctrlPts, degree)
        # cubic_spline.nurbs = convert.bspline_to_nurbs(spline)
        cubic_spline.nurbs = NURBS.Curve()
        cubic_spline.nurbs.degree = degree
        cubic_spline.nurbs.ctrlpts = ctrlPts
        cubic_spline.nurbs.knotvector = knotvector.generate(cubic_spline.nurbs.degree, cubic_spline.nurbs.ctrlpts_size)
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
    def getPntInit(self):
        pt = Pnt2D(self.nurbs.ctrlpts[0][0], self.nurbs.ctrlpts[0][1])
        return pt

    # ---------------------------------------------------------------------
    def getPntEnd(self):
        pt = Pnt2D(self.nurbs.ctrlpts[-1][0], self.nurbs.ctrlpts[-1][1])
        return pt

    # ---------------------------------------------------------------------
    def lengthInerpPts(self):
        L = 0.0
        for i in range(0, len(self.nurbs.ctrlpts) - 1):
            L += math.sqrt((self.nurbs.ctrlpts[i+1][0] - self.nurbs.ctrlpts[i][0]) *
                           (self.nurbs.ctrlpts[i+1][0] - self.nurbs.ctrlpts[i][0]) +
                           (self.nurbs.ctrlpts[i+1][1] - self.nurbs.ctrlpts[i][1]) *
                           (self.nurbs.ctrlpts[i+1][1] - self.nurbs.ctrlpts[i][1]))
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
    def getDataToInitCurve(self):
        data = {'degree': self.nurbs.degree,
                'ctrlpts': self.nurbs.ctrlpts,
                'weights': self.nurbs.weights,
                'knotvector': self.nurbs.knotvector}
        return data
