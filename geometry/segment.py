from compgeom.pnt2d import Pnt2D
from geometry.curves.curve import Curve
from compgeom.compgeom import CompGeom
from geometry.curves.polyline import Polyline
from geometry.curves.cubicspline import CubicSpline
from geometry.curves.circlearc import CircleArc
from geometry.curves.ellipsearc import EllipseArc
import numpy as np
from geomdl import NURBS
from geomdl import operations
from geomdl import helpers
import copy


class Segment():
    def __init__(self, _polypts, _curve=None):
        self.polyline = _polypts  # segment equiv. polyline
        self.curve = _curve  # owning curve (can be empty [])
        self.edge = None
        self.attributes = []
        self.selected = False
        self.nsudv = None
        self.sdvPoints = None
        self.originalNurbs = copy.deepcopy(_curve.nurbs)
        self.directionView = False
        self.CtrlPolyView = False
        self.isReversed = False
        self.refinement = []

    # ---------------------------------------------------------------------
    def getCurve(self):
        return self.curve

    # ---------------------------------------------------------------------
    def setSelected(self, _status):
        self.selected = _status

    # ---------------------------------------------------------------------
    def isSelected(self):
        return self.selected

    # ---------------------------------------------------------------------
    def getPoints(self):
        return self.polyline

    # ---------------------------------------------------------------------
    def getInitTangent(self):
        pt, tan = self.curve.evalPointTangent(0.0)
        tan = Pnt2D.normalize(tan)
        return tan

    # ---------------------------------------------------------------------
    def getEndTangent(self):
        pt, tan = self.curve.evalPointTangent(1.0)
        tan = Pnt2D.normalize(tan)
        return tan

    # ---------------------------------------------------------------------
    # THIS WILL BE REMOVED
    def curvature(self, _t):
        return 0.0

    # ---------------------------------------------------------------------
    def intersectPoint(self, _pt, _tol):
        status, clstPt, dmin, t, tang = self.curve.closestPoint(_pt.getX(), _pt.getY())
        if dmin <= _tol:
            return True, t, clstPt
        else:
            return False, t, clstPt

    # ---------------------------------------------------------------------
    def split(self, _params, _pts):
        curv2 = self.curve
        segments = []

        for i in range(0, len(_pts)):
            status, clstPt, dmin, t, tangVec = curv2.closestPointParam(_pts[i].getX(), _pts[i].getY(), _params[i])
            curv1, curv2 = curv2.split(t)

            if curv1 is not None:
                seg1Pts = curv1.getEquivPolyline()
                seg1 = Segment(seg1Pts, curv1)
                segments.append(seg1)

            # update the remaining parameters
            for j in range(i+1, len(_params)):
                _params[j] = (_params[j] - _params[i])/(1-_params[i])

        if curv2 is not None:
            seg2Pts = curv2.getEquivPolyline()
            seg2 = Segment(seg2Pts, curv2)
            segments.append(seg2)
        return segments

    # ---------------------------------------------------------------------
    def length(self):
        L = self.curve.length()
        return L

    # ---------------------------------------------------------------------
    def isEqual(self, _segment, _tol):
        # # Check curves types:
        # if _segment.curve.type != self.curve.type:
        #     return False

        Maybe = False
        # Check knot vector:
        if len(_segment.curve.nurbs.knotvector) == len(self.curve.nurbs.knotvector):
            knotvector1 = copy.deepcopy(_segment.curve.nurbs.knotvector)
            knotvector2 = copy.deepcopy(self.curve.nurbs.knotvector)
            for i in range (len(knotvector1)):
                diff = knotvector1[i] - knotvector2[i]
                if abs(diff) > Curve.PARAM_TOL:
                    Maybe = True
        else:
            return False

        # Check ctrlpts
        if len(_segment.curve.nurbs.ctrlpts) == len(self.curve.nurbs.ctrlpts):
            ctrlpts1 = copy.deepcopy(_segment.curve.nurbs.ctrlpts)
            ctrlpts2 = copy.deepcopy(self.curve.nurbs.ctrlpts)
            for i in range (len(ctrlpts1)):
                Pt1 = Pnt2D(ctrlpts1[i][0], ctrlpts1[i][1])
                Pt2 = Pnt2D(ctrlpts2[i][0], ctrlpts2[i][1])
                tol = Pnt2D(_tol, _tol)
                if not Pnt2D.equal(Pt1, Pt2, tol):
                    Maybe = True
        else:
            return False

        # Check weights
        if len(_segment.curve.nurbs.weights) == len(self.curve.nurbs.weights):
            weights1 = copy.deepcopy(_segment.curve.nurbs.weights)
            weights2 = copy.deepcopy(self.curve.nurbs.weights)
            for i in range (len(weights1)):
                diff = weights1[i] - weights2[i]
                if abs(diff) > Curve.PARAM_TOL:
                    Maybe = True
        else:
            return False

        # Try inversed curve
        if Maybe:
            for i in range(len(knotvector1)):
                knotvector1[i] = 1.0 - knotvector1[i]
            knotvector1.reverse()
            # for i in range(len(knotvector1)):
            #     if knotvector1[i] != 1.0 and knotvector1[i] != 0.0:
            #         knotvector1[i] = 1.0 - knotvector1[i]
            ctrlpts1.reverse()
            weights1.reverse()

            # Check knot vector:
            if len(_segment.curve.nurbs.knotvector) == len(self.curve.nurbs.knotvector):
                for i in range (len(knotvector1)):
                    diff = knotvector1[i] - knotvector2[i]
                    if abs(diff) > Curve.PARAM_TOL:
                        return False
            else:
                return False

            # Check ctrlpts
            if len(_segment.curve.nurbs.ctrlpts) == len(self.curve.nurbs.ctrlpts):
                for i in range (len(_segment.curve.nurbs.ctrlpts)):
                    Pt1 = Pnt2D(ctrlpts1[i][0], ctrlpts1[i][1])
                    Pt2 = Pnt2D(ctrlpts2[i][0], ctrlpts2[i][1])
                    tol = Pnt2D(_tol, _tol)
                    if not Pnt2D.equal(Pt1, Pt2, tol):
                        return False
            else:
                return False

            # Check weights
            if len(_segment.curve.nurbs.weights) == len(self.curve.nurbs.weights):
                for i in range (len(weights1)):
                    diff = weights1[i] - weights2[i]
                    if abs(diff) > Curve.PARAM_TOL:
                        return False
            else:
                return False

        # If reached here return True
        return True

    # ---------------------------------------------------------------------
    def boundIntegral(self):
        area = 0
        for i in range(0, len(self.polyline)-1):
            pt0 = self.polyline[i]
            pt1 = self.polyline[i+1]
            area += (pt0.getX())*(pt1.getY()) - (pt1.getX())*(pt0.getY())
        return area*0.5

    # ---------------------------------------------------------------------
    def evalPoint(self, _t):
        pt = self.curve.evalPoint(_t)
        return pt

    # ---------------------------------------------------------------------
    def getXinit(self):
        pt = self.curve.getXinit()
        return pt

    # ---------------------------------------------------------------------
    def getYinit(self):
        pt = self.curve.getYinit()
        return pt

    # ---------------------------------------------------------------------
    def getXend(self):
        pt = self.curve.getXend()
        return pt

    # ---------------------------------------------------------------------
    def getYend(self):
        pt = self.curve.getYend()
        return pt
    
    # ---------------------------------------------------------------------
    def getPntInit(self):
        pt = self.curve.getPntInit()
        return pt
    
    # ---------------------------------------------------------------------
    def getPntEnd(self):
        pt = self.curve.getPntEnd()
        return pt

    # ---------------------------------------------------------------------
    def getType(self):
        return self.curve.getType()

    # ---------------------------------------------------------------------
    def ray(self, _pt):
        x = _pt.getX()
        y = _pt.getY()
        n = len(self.polyline)
        ni = 0

        for i in range(0, n-1):
            pt1 = self.polyline[i]
            pt2 = self.polyline[i+1]

            if pt1.getY() == pt2.getY():  # discard horizontal line
                continue

            if pt1.getY() > y and pt2.getY() > y:  # discard line above ray
                continue

            if pt1.getY() < y and pt2.getY() < y:  # Discard line below ray
                continue

            if pt1.getX() < x and pt2.getX() < x:  # discard line to the left of point
                continue

            if pt1.getY() == y:  # ray passes at first line point
                if pt1.getX() > x and pt2.getY() > y:
                    # Count intersection if first point is to the right of given point
                    # and second point is above.
                    ni += 1
            else:
                if pt2.getY() == y:  # ray passes at second point
                    if pt2.getX() > x and pt1.getY() > y:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                else:  # ray passes with first and second points
                    if pt1.getX() > x and pt2.getX() > x:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                    else:
                        # Compute x coordinate of intersection of ray with line segment
                        dx = pt1.getX() - pt2.getX()
                        xc = pt1.getX()

                        if dx != 0:
                            xc += (y - pt1.getY())*dx / \
                                (pt1.getY() - pt2.getY())

                        if xc > x:
                            # Count intersection if first point is to the right of given point
                            # and second point is above.
                            ni += 1
        return ni

    # ---------------------------------------------------------------------
    def setInitPoint(self, _pt):
        self.polyline[0].setX(_pt.getX())
        self.polyline[0].setY(_pt.getY())

    # ---------------------------------------------------------------------
    def setEndPoint(self, _pt):
        self.polyline[-1].setX(_pt.getX())
        self.polyline[-1].setY(_pt.getY())

    # ---------------------------------------------------------------------
    def setNumberSdv(self, _nsudv):
        # In case it is isogeometric, the number of subdivisions was not 
        # manually set by the user, and it must be determined. It is simply
        # given by the the number of knot spans
        if _nsudv['properties']['isIsogeometric']:
            knots = list(set(self.curve.nurbs.knotvector))
            _nsudv['properties']['Value'] = len(knots) - 1
            _nsudv['properties']['Ratio'] = 0.0
        self.nsudv = _nsudv

    # ---------------------------------------------------------------------
    def getNumberSdv(self):
        if self.nsudv is None:
            return 1
        return self.nsudv

    # ---------------------------------------------------------------------
    def setSdvPoints(self, _sdvPoints):
        self.nsudv = len(_sdvPoints) + 1
        self.sdvPoints = _sdvPoints

    # ---------------------------------------------------------------------
    def delSdvPoints(self):
        if self.sdvPoints is not []:
            del self.sdvPoints
            self.sdvPoints = []
        self.nsudv = None

    # ---------------------------------------------------------------------
    def getSdvPoints(self):
        if self.nsudv is None:
            return []
        return self.sdvPoints

    # ---------------------------------------------------------------------
    def closestPoint(self, _x, _y):
        if self.curve is not None:
            status, clstPt, dmin, t, tang = self.curve.closestPoint(_x, _y)
            xOn = clstPt.getX()
            yOn = clstPt.getY()
            if status:
                if (t < 0.0) or (t > 1.0):
                    return False, xOn, xOn, dmin
        else:
            status = True
            pt = Pnt2D(_x, _y)
            polypts = self.polyline
            d, clstPtSeg, t = CompGeom.getClosestPointSegment(polypts[0], polypts[1], pt)
            xOn = clstPtSeg.getX()
            yOn = clstPtSeg.getY()
            dmin = d
            for i in range(1, len(polypts) - 1):
                d, clstPtSeg, t = CompGeom.getClosestPointSegment(polypts[i], polypts[i + 1], pt)
                if d < dmin:
                    xOn = clstPtSeg.getX()
                    yOn = clstPtSeg.getY()
                    dmin = d
        return status, xOn, yOn, dmin

    # ---------------------------------------------------------------------
    def getBoundBox(self):
        # Compute segment bounding box based on segment polypoints
        x = []
        y = []
        for point in self.polyline:
            x.append(point.getX())
            y.append(point.getY())
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        return xmin, xmax, ymin, ymax

    # ---------------------------------------------------------------------
    def degreeElevation(self):
        crv = copy.deepcopy(self.curve.nurbs)

        # Knot insertion
        knots = list(set(crv.knotvector)) # Remove duplicates
        knots.sort()
        knots.pop()
        knots.pop(0)

        numb_insertions = []
        for knot in knots:
            knot_multiplicity = helpers.find_multiplicity(knot, crv.knotvector)
            numb_insertions.append(crv.degree - knot_multiplicity)
            if numb_insertions[-1] > 0:
                operations.insert_knot(crv, [knot], [numb_insertions[-1]])

        # Bezier decomposition
        beziers = operations.decompose_curve(crv)
        
        # Bezier degree elevation
        new_ctrlptsw = []
        for i in range(len(beziers)):
            bezier_new_ctrlptsw = helpers.degree_elevation(crv.degree, beziers[i].ctrlptsw)
            if i != (len(beziers) - 1):
                bezier_new_ctrlptsw.pop()
            new_ctrlptsw.extend(bezier_new_ctrlptsw)

        # New knot vector
        new_knot_vector = crv.knotvector
        new_knot_vector.extend(list(set(crv.knotvector)))
        new_knot_vector.sort()

        # New degree
        new_degree = crv.degree + 1

        # Create the curve instance #2
        crv2 = NURBS.Curve()

        # Set degree, control points and knot vector
        crv2.degree = new_degree
        crv2.ctrlptsw = new_ctrlptsw
        crv2.knotvector = new_knot_vector

        for i in range(len(knots)):
            operations.remove_knot(crv2, [knots[i]], [numb_insertions[i]])

        self.curve.nurbs = crv2

        # Add degreeElevation in self.refinement
        self.refinement.append("degreeElevation")

    # ---------------------------------------------------------------------
    def knotInsertion(self):
        knots = self.curve.nurbs.knotvector
        knots = list(set(knots)) # Remove duplicates
        knots.sort()

        knotsToBeInserted = []
        for i in range(len(knots) - 1):
            mediumKnot = (knots[i] + knots[i + 1]) / 2.0
            knotsToBeInserted.append(mediumKnot)

        for knot in knotsToBeInserted:
            operations.insert_knot(self.curve.nurbs, [knot], [1])

        # Add Knot Insertion in self.refinement
        self.refinement.append("knotInsertion")

    # ---------------------------------------------------------------------
    def rescueNurbsCurve(self):
        self.curve.nurbs = copy.deepcopy(self.originalNurbs)
        self.isReversed = False
        self.refinement = []

    # ---------------------------------------------------------------------
    def reverseNurbsCurve(self, load):
        degree = copy.deepcopy(self.curve.nurbs.degree)
        ctrlpts = copy.deepcopy(self.curve.nurbs.ctrlpts)
        weights = copy.deepcopy(self.curve.nurbs.weights)
        knotvector = copy.deepcopy(self.curve.nurbs.knotvector)

        # inverte NURBS direction
        for i in range(len(knotvector)):
            knotvector[i] = 1.0 - knotvector[i]
        knotvector.reverse()
        ctrlpts.reverse()
        weights.reverse()

        # Create the curve instance #2
        crv2 = NURBS.Curve()

        # Set degree, control points and knot vector
        crv2.degree = degree
        crv2.ctrlpts = ctrlpts
        crv2.weights = weights
        crv2.knotvector = knotvector

        self.curve.nurbs = crv2

        # Change self.isReversed flag
        if not load:
            if self.isReversed == False:
                self.isReversed = True
            else:
                self.isReversed = False

    # ---------------------------------------------------------------------
    def updateDirectionView(self, status):
        self.directionView = status

    # ---------------------------------------------------------------------
    def updateCtrlPolyView(self, status):
        self.CtrlPolyView = status
        
    # ---------------------------------------------------------------------
    def getNurbs(self):
        return self.curve.nurbs

    # ---------------------------------------------------------------------
    def getCtrlPts(self):
        return self.curve.nurbs.ctrlpts

    # ---------------------------------------------------------------------
    def getDataToInitCurve(self):
        data = self.curve.getDataToInitCurve()
        data['isReversed'] = self.isReversed
        data['refinement'] = self.refinement
        if self.attributes is not None and self.nsudv is not None:
            data['isSdvSet'] = True
        else:
            data['isSdvSet'] = False
        return data

    # ---------------------------------------------------------------------
    @staticmethod
    def joinTwoSegments(_seg1, _seg2, _pt, _tol):
 
        # Check whether the curves of the two segments may be joined, verifying
        # whether the types of curves are compatible for joining and performing
        # geometric verifications. The new curve resulting from the joining
        # operation is returned.
        status, curv, error_text = _seg1.curve.join(_seg2.curve, _pt, _tol)
        if not status:
            return None, error_text

        # If the two curves can be joined, create a new segments with the
        # joined curve.
        segPoly = curv.getEquivPolyline()
        seg = Segment(segPoly, curv)

        return seg, None

    # ---------------------------------------------------------------------
    @staticmethod
    def conformNurbsCurves(_seg_list):
        # check curves degree
        degrees_list = []
        for seg in _seg_list:
            degrees_list.append(seg.curve.nurbs.degree)

        if len(set(degrees_list)) != 1:
            error_text = "Curves must have the same degree"
            return False, error_text
        
        # find remaining knots
        insert_knots = []
        for i in range(len(_seg_list)):
            knots_already_have = copy.deepcopy(_seg_list[i].curve.nurbs.knotvector)
            seg_insert_knots = []
            for j in range(len(_seg_list)):
                next_knotvector = _seg_list[j].curve.nurbs.knotvector
                
                remaining_knots = []
                for k in next_knotvector:
                    if k not in knots_already_have:
                        remaining_knots.append(k)

                knots_already_have.extend(remaining_knots)
                seg_insert_knots.extend(remaining_knots)
            insert_knots.append(seg_insert_knots)

        # insert remaining knots in each curve
        for i in range(len(_seg_list)):
            seg = _seg_list[i]
            knots = insert_knots[i]
            for knot in knots:
                operations.insert_knot(seg.curve.nurbs, [knot], [1])

        return True, None