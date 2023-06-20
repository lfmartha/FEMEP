from compgeom.pnt2d import Pnt2D
from compgeom.compgeom import CompGeom
from geometry.curves.curve import Curve
from geometry.curves.line import Line
from geomdl import NURBS
from geomdl import operations
from geomdl import knotvector
import copy
import math


class Polyline(Curve):
    def __init__(self, _pts=None):
        super(Curve, self).__init__()
        self.type = 'POLYLINE'
        self.pts = _pts
        self.nPts = 0
        self.nurbs = []

        if self.pts is not None:
            self.nPts = len(self.pts)

            if self.nPts >= 2:
                # Nurbs degree and control points
                degree = 1
                ctrlPts = []
                for pt in self.pts:
                    ctrlPts.append([pt.getX(), pt.getY()])

                # NURBS knotvector
                knotVector = knotvector.generate(degree, len(ctrlPts))

                # Creating Nurbs polyline
                self.nurbs = NURBS.Curve()
                self.nurbs.degree = degree
                self.nurbs.ctrlpts = ctrlPts
                self.nurbs.knotvector = knotVector
                self.nurbs.sample_size = 10

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
    def addCtrlPoint(self, _v1, _v2, _LenAndAng):
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
            degree = 1
            ctrlPts = []
            for pt in self.pts:
                ctrlPts.append([pt.getX(), pt.getY()])

            # NURBS knotvector
            knotVector = knotvector.generate(degree, len(ctrlPts))

            # Creating Nurbs polyline
            self.nurbs = NURBS.Curve()
            self.nurbs.degree = degree
            self.nurbs.ctrlpts = ctrlPts
            self.nurbs.knotvector = knotVector
            self.nurbs.sample_size = 10

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
        for i in range(1, len(self.pts) - 1):
            if not CompGeom.pickLine(self.pts[0], self.pts[-1], self.pts[i], _tol):
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
    def findPointLocation(self, _t):
        if _t <= 0.0:
            return 0, 0.0
        elif _t >= 1.0:
            return (self.nPts - 1), 1.0

        prev_id = 0
        loc_t = 0.0

        knots = self.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()

        for i in range(1, len(knots)):
            prev_id = i - 1
            next_id = i
            if _t >= knots[prev_id] and _t < knots[next_id]:
                loc_t = _t - knots[prev_id]
                break
        return prev_id, loc_t

    # ---------------------------------------------------------------------
    def findPointLocationSeg(self, _t):
        if _t <= 0.0:
            return 0, 0.0
        elif _t >= 1.0:
            return (self.nPts - 1), 1.0

        length = self.length()
        s = _t * length

        prev_id = 0
        loc_t = 1.0
        lenToSeg = 0.0

        for i in range(1, len(self.pts)):
            prev_id = i - 1
            next_id = i
            dist = math.sqrt((self.pts[i].getX() - self.pts[i - 1].getX()) *
                             (self.pts[i].getX() - self.pts[i - 1].getX()) +
                             (self.pts[i].getY() - self.pts[i - 1].getY()) *
                             (self.pts[i].getY() - self.pts[i - 1].getY()))

            if (lenToSeg + dist) >= s:
                loc_t = (s - lenToSeg) / dist
                break

            lenToSeg += dist

        x = self.pts[prev_id].getX() + loc_t * \
            (self.pts[next_id].getX() - self.pts[prev_id].getX())
        y = self.pts[prev_id].getY() + loc_t * \
            (self.pts[next_id].getY() - self.pts[prev_id].getY())
        return prev_id, loc_t

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        if _t <= 0.0:
            return self.pts[0]
        elif _t >= 1.0:
            return self.pts[-1]

        pt = self.nurbs.evaluate_single(_t)
        return Pnt2D(pt[0], pt[1])
    
    # ---------------------------------------------------------------------
    def evalPointSeg(self, _t):
        if _t <= 0.0:
            return self.pts[0]
        elif _t >= 1.0:
            return self.pts[-1]
        
        prev_id, loc_t = self.findPointLocationSeg(_t)

        x = self.pts[prev_id].getX() + loc_t * \
            (self.pts[prev_id + 1].getX() - self.pts[prev_id].getX())
        y = self.pts[prev_id].getY() + loc_t * \
            (self.pts[prev_id + 1].getY() - self.pts[prev_id].getY())
        return Pnt2D(x,y)

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
        left = Polyline()
        right = Polyline()
            
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
        prev_id, loc_t = self.findPointLocation(_t)

        # Left curve properties
        left_pts = []
        for i in range(0, prev_id):
            left_pts.append(self.pts[i])

        # check whether the split point is one of the points of the polyline itself
        if loc_t > Curve.PARAM_TOL:
            left_pts.append(self.pts[prev_id])

        left_pts.append(pt)

        # Right curve properties
        right_pts = []
        right_pts.append(pt)
        # check whether the split point is one of the points of the polyline itself
        if 1.0 - loc_t > Curve.PARAM_TOL:
            right_pts.append(self.pts[prev_id + 1])

        for j in range(prev_id + 2, self.nPts):
            right_pts.append(self.pts[j])

        # Create curve objects resulting from splitting
        left = Polyline(left_pts)
        right = Polyline(right_pts)
        return left, right

    # ---------------------------------------------------------------------
    def join(self, _joinCurve, _pt, _tol):
        if (_joinCurve.getType() != 'LINE') and (_joinCurve.getType() != 'POLYLINE'):
            return False, None, 'Cannot join segments:\n A POLYLINE curve may be joined only with a LINE or a POLYLINE.'

        curv1 = self
        if _joinCurve.type == "LINE":
            curv2 = Polyline([_joinCurve.pt0, _joinCurve.pt1])
        else:
            curv2 = _joinCurve

        tol = Pnt2D(_tol, _tol)

        # check curves initial point
        if Pnt2D.equal(curv1.pts[0], _pt, tol):
            init_pt1 = True
        else:
            init_pt1 = False

        if Pnt2D.equal(curv2.pts[0], _pt, tol):
            init_pt2 = True
        else:
            init_pt2 = False

        # polyline points
        curv1_pts = curv1.getEquivPolyline()
        curv2_pts = curv2.getEquivPolyline()

        joinned_pts = []
        if init_pt1 and init_pt2:
            curv1_pts.reverse()
            curv1_pts.pop()
            joinned_pts.extend(curv1_pts)
            joinned_pts.extend(curv2_pts)

        elif not init_pt1 and not init_pt2:
            curv1_pts.pop()
            joinned_pts.extend(curv1_pts)
            curv2_pts.reverse()
            joinned_pts.extend(curv2_pts)

        elif init_pt1 and not init_pt2:
            joinned_pts.extend(curv2_pts)
            joinned_pts.pop()
            joinned_pts.extend(curv1_pts)

        elif not init_pt1 and init_pt2:
            joinned_pts.extend(curv1_pts)
            joinned_pts.pop()
            joinned_pts.extend(curv2_pts)

        curv = Polyline(joinned_pts)
        return True, curv, None

    # ---------------------------------------------------------------------
    def getEquivPolyline(self):
        equivPoly = []
        if self.nPts < 2:
            return equivPoly
        for i in range(0, self.nPts):
            equivPoly.append(self.pts[i])
        return equivPoly

    # ---------------------------------------------------------------------
    def getEquivPolylineCollecting(self, _pt):
        tempPts = []
        for i in range(0, self.nPts):
            tempPts.append(self.pts[i])
        tempPts.append(_pt)
        return tempPts

    # ---------------------------------------------------------------------
    def closestPointSeg(self, _x, _y):
        if self.pts is []:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        if len(self.pts) < 2:
            return False, Pnt2D(0,0), 0, 0, Pnt2D(0,0)

        aux = Line(self.pts[0], self.pts[1])
        status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
        xOn = clstPtSeg.getX()
        yOn = clstPtSeg.getY()
        dmin = d
        seg = 0

        for i in range(1, len(self.pts) - 1):
            aux = Line(self.pts[i], self.pts[i + 1])
            status, clstPtSeg, d, t, tang = aux.closestPoint(_x, _y)
            if d < dmin:
                xOn = clstPtSeg.getX()
                yOn = clstPtSeg.getY()
                dmin = d
                seg = i

        arcLen = 0.0
        for i in range(0, seg):
            arcLen += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
                                (self.pts[i + 1].getX() - self.pts[i].getX()) +
                                (self.pts[i + 1].getY() - self.pts[i].getY()) *
                                (self.pts[i + 1].getY() - self.pts[i].getY()))
        arcLen += math.sqrt((xOn - self.pts[seg].getX()) *
                            (xOn - self.pts[seg].getX()) +
                            (yOn - self.pts[seg].getY()) *
                            (yOn - self.pts[seg].getY()))

        clstPt = Pnt2D(xOn, yOn)
        return status, clstPt, dmin, seg, arcLen

    # ---------------------------------------------------------------------
    def updateParametricValue(self, _t):
        if _t >= 1.0:
            return 1.0
        elif _t <= 0.0:
            return 0.0

        knots = self.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()

        prev_id, loc_t = self.findPointLocationSeg(_t)
        t = knots[prev_id] + loc_t * (knots[prev_id + 1] - knots[prev_id])
        return t

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        status, clstPt, dmin, seg, arcLen = self.closestPointSeg(_x, _y)
        if not status:
            return status, clstPt, dmin, 0.0, Pnt2D(0,0)

        tolLen = self.length()
        t = arcLen / tolLen
        t = self.updateParametricValue(t)
        if t <= 0.0:
            t = 0.0
            seg = 0
            clstPt = self.pts[seg]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        elif t >= 1.0:
            t = 1.0
            seg = len(self.pts) - 2
            clstPt = self.pts[seg + 1]
            tang = self.pts[seg + 1] - self.pts[seg]
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
        t = self.updateParametricValue(t)
        if t < Curve.PARAM_TOL:
            t = 0.0
            seg = 0
            clstPt = self.pts[seg]
            tang = self.pts[seg + 1] - self.pts[seg]
            status = True
        elif t > 1.0 - Curve.PARAM_TOL:
            t = 1.0
            seg = len(self.pts) - 2
            clstPt = self.pts[seg + 1]
            tang = self.pts[seg + 1] - self.pts[seg]
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
        for point in self.pts:
            x.append(point.getX())
            y.append(point.getY())
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        return xmin, xmax, ymin, ymax

    # ---------------------------------------------------------------------
    def getXinit(self):
        return self.pts[0].getX()

    # ---------------------------------------------------------------------
    def getYinit(self):
        return self.pts[0].getY()

    # ---------------------------------------------------------------------
    def getXend(self):
        return self.pts[-1].getX()

    # ---------------------------------------------------------------------
    def getYend(self):
        return self.pts[-1].getY()

    # ---------------------------------------------------------------------
    def getPntInit(self):
        pt = Pnt2D(self.pts[0].getX(), self.pts[0].getY())
        return pt

    # ---------------------------------------------------------------------
    def getPntEnd(self):
        pt = Pnt2D(self.pts[-1].getX(), self.pts[-1].getY())
        return pt

    # ---------------------------------------------------------------------
    def length(self):
        L = 0.0
        for i in range(0, self.nPts - 1):
            L += math.sqrt((self.pts[i + 1].getX() - self.pts[i].getX()) *
                           (self.pts[i + 1].getX() - self.pts[i].getX()) +
                           (self.pts[i + 1].getY() - self.pts[i].getY()) *
                           (self.pts[i + 1].getY() - self.pts[i].getY()))
        return L
        
    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        pts = []
        for i in range (self.nPts):
            pts.append([self.pts[i].getX(), self.pts[i].getY()])
        data = {'pts': pts}
        return data
