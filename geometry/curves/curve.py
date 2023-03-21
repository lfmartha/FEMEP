from compgeom.pnt2d import Pnt2D
import numpy as np


class Curve():
    PARAM_TOL = 1e-7
    COORD_TOL = 1e-5
    MIN_STEP_REDUCT = 0.005
    MAX_NUM_ITERAT = 100
    curveTypes = ['NONE', 'LINE', 'POLYLINE', 'CUBICSPLINE','CIRCLE', 'CIRCLEARC']

    def __init__(self):
        self.type = 'NONE'
        self.nPts = 0  # number of control points

    # ---------------------------------------------------------------------
    # Returns the type of a curve.
    def getType(self):
        return self.type

    # ---------------------------------------------------------------------
    # Returns the current number of curve control points collected so far.
    def getNumberOfCtrlPoints(self):
        return self.nPts

    # ---------------------------------------------------------------------
    # Inserts a new curve control point with the given coordinates.
    def addCtrlPoint(self, _x, _y, _LenAndAng):
        pass

    # ---------------------------------------------------------------------
    # Evaluates a curve point at the given parametric value.
    def evalPoint(self, _t):
        pass

    # ---------------------------------------------------------------------
    # Evaluates a curve point at the given parametric value.
    # Returns the evaluated point and the tangent vector at this point.
    def evalPointTangent(self, _t):
        pass

    # ---------------------------------------------------------------------
    # Returns a boolean value (True or False) stating whether the control
    # points collected so far can form a valid curve.
    def isPossible(self):
        return False

    # ---------------------------------------------------------------------
    # Returns a boolean value (True or False) stating whether the curve
    # can have a unlimited number of control points.
    def isUnlimited(self):
        return False

    # ---------------------------------------------------------------------
    # Returns a list of curve control points collected so far.
    def getCtrlPoints(self):
        pass

    # ---------------------------------------------------------------------
    # Returns the number of curve reshape control points.
    def getNumberOfReshapeCtrlPoints(self):
        return self.getNumberOfCtrlPoints()

    # ---------------------------------------------------------------------
    # Returns a list of curve reshape control points.
    def getReshapeCtrlPoints(self):
        return self.getCtrlPoints()

    # ---------------------------------------------------------------------
    # Changes the coordinates of a curve control point for reshaping,
    # identified by its index.
    def setCtrlPoint(self, _id, _x, _y):
        pass

    # ---------------------------------------------------------------------
    # Return a boolean value (True or False) stating whether a curve
    # can be considered a straight line (according to the given
    # tolerance value).
    def isStraight(self, _tol):
        pass

    # ---------------------------------------------------------------------
    # Return a boolean value (True or False) stating whether a curve
    # is closed, i.e., when the two end points have the same coordinates.
    def isClosed(self):
        pass

    # ---------------------------------------------------------------------
    # This method is used by the class method genEquivPolyline (see below)
    # to generate an equivalent polyline of a parametric curve.
    # It returns two new curves of the same type resulting from splitting
    # the current curve at a point given by its parametric value.
    # The difference between this method and the split method below is
    # that in here only the raw geometric properties of the curves
    # resulting from split are created. In the case of a parametric
    # curve no equivalente polyline is generated.
    def splitRaw(self, _t):
        pass

    # ---------------------------------------------------------------------
    # Returns two new curves of the same type resulting from splitting
    # the current curve at a point given by its parametric value.
    def split(self, _t):
        pass

    # ---------------------------------------------------------------------
    # Returns equivalent polygonal of given curve from _tInit to _tEnd
    # parametric values. The polyline is returned as a list of points.
    def getEquivPolyline(self, _tInit, _tEnd, _tol):
        pass

    # ---------------------------------------------------------------------
    # Returns equivalent polygonal of given curve while collecting a
    # given candidate (_pt) for next control point.
    # The polyline is returned as a list of points.
    # It handles the generation of equivalent polyline for partial
    # collection of control points.
    def getEquivPolylineCollecting(self, _pt):
        pass

    # ---------------------------------------------------------------------
    # Gets the point on a curve that is closest to a given point.
    # It also returns the distance between the given point and the closest
    # point, and the parametric value of the closest point on the curve.
    # The closest point is found such that the distance between the
    # given point and the curve is minimum.
    # It it is not possible to find the closest point for any reason
    # it returns a false status. Otherwise it returns a true status.
    def closestPoint(self, _x, _y):
        pass

    # ---------------------------------------------------------------------
    # Gets the point on a curve that is closest to a given point.
    # The difference between this method and closestPoint is that in
    # this a starting parametric value to find the closest point is also
    # given.
    def closestPointParam(self, _x, _y, _tStart):
        pass

    # ---------------------------------------------------------------------
    # Returns the bounding box (minimum and maximum x and y coordinates)
    # of a curve.
    def getBoundBox(self):
        pass

    # ---------------------------------------------------------------------
    # Returns the x coordinate of the curve initial point.
    def getXinit(self):
        pass

    # ---------------------------------------------------------------------
    # Returns the y coordinate of the curve initial point.
    def getYinit(self):
        pass

    # ---------------------------------------------------------------------
    # Returns the x coordinate of the curve end point.
    def getXend(self):
        pass

    # ---------------------------------------------------------------------
    # Returns the y coordinate of the curve end point.
    def getYend(self):
        pass

    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # --------------------------- CLASS METHODS ---------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Returns the inverse of a 2x2 matrix.
    @staticmethod
    def invert2x2(mtx):
        det = (mtx[0][0] * mtx[1][1]) - (mtx[0][1] * mtx[1][0])

        mtxInv = np.array([[0.0, 0.0], 
                           [0.0, 0.0]])  # jacobian matrix at evaluation point
        if det == 0.0:
            return False, mtxInv

        mtxInv[0][0] = mtx[1][1] / det
        mtxInv[0][1] = - mtx[0][1] / det
        mtxInv[1][0] = - mtx[1][0] / det
        mtxInv[1][1] = mtx[0][0] / det
        return True, mtxInv

    # ---------------------------------------------------------------------
    # This class method, recursevely generates an equivalent polygonal for
    # a given curve. The polyline generation is adaptative to the curve
    # curvature.
    # The algorithm first checks to see whether the curve can be considered
    # a straight line based on given tolerance value. If that is the case,
    # it appends the initial curve point to a list os polyline points.
    # Otherwise, it splits the curve into two halfs (left and right) and
    # recursively calls the class method for each half.
    # At the end of the recursive process, the curve end point needs to
    # be appended to the list of polyline points.
    @staticmethod
    def genEquivPolyline(crv, _pts, _tol):
        if crv.isStraight(_tol):
            pt0 = Pnt2D(crv.getXinit(), crv.getYinit())
            _pts.append(pt0)
        else:
            left, right = crv.splitRaw(0.5)
            Curve.genEquivPolyline(left, _pts, _tol)
            Curve.genEquivPolyline(right, _pts, _tol)
        return _pts

    # ---------------------------------------------------------------------
    # ParamCurveClosestPt - gets the point on a given parametric curve
    # which is closest to a given point (given by its coordinates _x
    # and _y).  It also returns the parametric value of the closest
    # point on the curve and the tangent vector at the closest point.
    # The closest point is found such that the distance between the
    # given point and the curve is minimum, that is, the difference
    # vector between the given point and the closest point is normal
    # to the curve.
    # The iterative Newton-Raphson method is used to find the parametric
    # value on the curve, which is the root of the polynominal that
    # results from the dot product of the difference vector between
    # the given point and a point on curve and the curve tangent
    # vector.  At the closest point this dot product is null.
    # The iterative method starts with a given parametric value (_tStart).
    @staticmethod
    def ParamCurveClosestPt(crv, _x, _y, _tStart):
        jac = np.array([[0.0, 0.0], 
                        [0.0, 0.0]])  # jacobian matrix at evaluation point

        # Iterate until each current and new parametric values are close
        # or we exceed the maximum number of iterations

        direction = 1.0
        numIterat = 0            # current number of iterations
        tNew = _tStart           # new parametric values on curve
        while True:
            tPar = tNew          # update current parametric value

            # Evaluate the curve and get the tangent at the current
            # evaluation point
            clstPt, tang = crv.evalPointTangent(tPar)

            # Normal vector is perpendicular to tangent vector.
            # Jacobian matrix is formed by rows: tangent and normal.
            jac[0][0] = tang.getX()
            jac[0][1] = tang.getY()
            jac[1][0] = -tang.getY()
            jac[1][1] = tang.getX()

            # Invert the Jacobian matrix.
            status, invJac = Curve.invert2x2(jac)
            if not status:
                return False, clstPt, tPar, tang

            # Compute the new guess of tPar.
            deltaX = clstPt.getX() - _x
            deltaY = clstPt.getY() - _y
            deltaPar = invJac[0][0] * deltaX + invJac[1][0] * deltaY

            # Adicionado
            # if (np.abs(deltaX) >= Curve.COORD_TOL or np.abs(deltaY) >= Curve.COORD_TOL) and (np.abs(deltaPar) <= Curve.PARAM_TOL):
            #     deltaPar = invJac[0][0] * deltaX - invJac[1][0] * deltaY
            # Adicionado

            # Modificado
            tNew = tPar - direction * deltaPar
            # Modificado

            # Adicionado
            # clstPt, tang = crv.evalPointTangent(tNew)
            # deltaX2 = clstPt.getX() - _x
            # deltaY2 = clstPt.getY() - _y
            # if np.abs(deltaX2) > np.abs(deltaX) or np.abs(deltaY2) > np.abs(deltaY):
            #     tNew = tPar + direction * deltaPar
            # Adicionado

            # Check to see if new parametric value is close to minimum
            # or maximum parametric values. In this case snap the value
            # to the minimum or maximum value.
            if (tNew > -Curve.PARAM_TOL) and (tNew < Curve.PARAM_TOL):
                tNew = 0.0
            if (tNew > 1.0 - Curve.PARAM_TOL) and (tNew < 1.0 + Curve.PARAM_TOL):
                tNew = 1.0

            # Check to see if new parametric value is outside the curve.
            # If the parametric value is outside the range, we backup the
            # step on parametric space using the same guessed direction
            # until the new parametric value is inside the curve or the step
            # reduction is too small.  In the latter case, we return a false
            # status, since the given point is not close to the curve.
            fac = 1.0
            while (tNew < 0.0) or (tNew > 1.0):
                fac *= 0.5
                if fac < Curve.MIN_STEP_REDUCT:
                # Modificado
                    direction *= -1.0
                    fac = 1.0
                tNew = tPar - fac * direction * deltaPar
                # Modificado

            # Increment number of iterations and check to see if it exceeds
            # the maximum allowed.  In that case return a false status.
            numIterat += 1
            if numIterat > Curve.MAX_NUM_ITERAT:
                return False, clstPt, tPar, tang

            # Check for convergence.
            if np.abs(tNew - tPar) <= Curve.PARAM_TOL:
                # if np.abs(deltaX) <= Curve.COORD_TOL and np.abs(deltaY) <= Curve.COORD_TOL:
                #     direction *= -1.0
                # else: 
                    break

        # The returned point coordinates is set as the last point
        # on the curve. Also returns the last parametric value and
        # the tangent vector
        tPar = tNew
        clstPt, tang = crv.evalPointTangent(tPar)
        return True, clstPt, tPar, tang

    # ---------------------------------------------------------------------
    # paramCurvesIntersection - Computes the intersection point of two
    # given curves. The parametric values of the intersection point on
    # both curves are also returned.
    # The algorithm starts evaluating one point on each curve based on the
    # given starting parametric values. These are the starting closest
    # points on the given curves. Then it starts an iterative process.
    # In each step, it evaluates the mid point between the closest points
    # and finds new closest points to the mid point on each curve. It 
    # iterates until the closest points on each curve are close within
    # a tolerance or the number of iteration exceeds a maximum values.
    @staticmethod
    def paramCurvesIntersection(crvA, crvB, _tStartA, _tStartB):
        numIterat = 0            # current number of iterations
        tParA = _tStartA         # new parametric values on curve A
        tParB = _tStartB         # new parametric values on curve B
        currPtA = crvA.evalPoint(tParA)
        currPtB = crvB.evalPoint(tParB)

        while ((abs(currPtA.getX() - currPtB.getX()) > Curve.COORD_TOL) or
               (abs(currPtA.getY() - currPtB.getY()) > Curve.COORD_TOL)):

            # Find closest point of the mid point between the evaluated points
            # on each curve
            midPt = (currPtA + currPtB) * 0.5
            status, nextPtA, dmin, tParA, tangA = crvA.closestPointParam(
                                        midPt.getX(), midPt.getY(), tParA)
            if not status:
                return False, currPtA, tParA, tParB
            status, nextPtB, dmin, tParB, tangB = crvB.closestPointParam(
                                        midPt.getX(), midPt.getY(), tParB)
            if not status:
                return False, currPtA, tParA, tParB

            # Update current points on curves
            currPtA = nextPtA
            currPtB = nextPtB
 
            # Increment number of iterations and check to see if it exceeds
            # the maximum allowed.  In that case return a true status any way.
            numIterat += 1
            if numIterat > Curve.MAX_NUM_ITERAT:
                return True, currPtA, tParA, tParB

        # The returned intersection point coordinates is set as the last point
        # on the curve A. Also returns the last parametric values on both curves
        return True, currPtA, tParA, tParB

    # ---------------------------------------------------------------------
    # @staticmethod
    # def joinTwoCurves(_curv1, _curv2, pt):
    #     if _curv1.nurbs.degree == _curv2.nurbs.degree:
    #         deg = _curv1.nurbs.degree
    #     else:
    #         error_text = "Both curves must have the same degree"
    #         return None, error_text

    #     curv1_ctrlpts = _curv1.nurbs.ctrlpts
    #     curv2_ctrlpts = _curv2.nurbs.ctrlpts
    #     curv1_knotvector = _curv1.nurbs.knotvector
    #     curv2_knotvector = _curv2.nurbs.knotvector
    #     tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)

    #     if Pnt2D.equal(Pnt2D(curv1_ctrlpts[0][0], curv1_ctrlpts[0][1]), pt, tol):
    #         init_pt1 = True
    #     else:
    #         init_pt1 = False

    #     if Pnt2D.equal(Pnt2D(curv2_ctrlpts[0][0], curv2_ctrlpts[0][1]), pt, tol):
    #         init_pt2 = True
    #     else:
    #         init_pt2 = False

    #     if init_pt1 and init_pt2:
    #         # Control Points
    #         curv1_ctrlpts.reverse()

    #         # Knot vector
    #         curv1_knotvector.reverse()
    #         for i in range(len(curv1_knotvector)):
    #             curv1_knotvector[i] = 1.0 - curv1_knotvector[i]

    #         curv1_knotvector = np.asarray(curv1_knotvector)
    #         curv1_ctrlpts = np.asarray(curv1_ctrlpts)

    #         curv2_knotvector = np.asarray(curv2_knotvector)
    #         curv2_ctrlpts = np.asarray(curv2_ctrlpts)

    #         curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
    #         curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
    #         curv = curv1.attach_nurbs(curv2)

    #     elif not init_pt1 and not init_pt2:
    #         # Control Points
    #         curv2_ctrlpts.reverse()

    #         # Knot vector
    #         curv2_knotvector.reverse()
    #         for i in range(len(curv2_knotvector)):
    #             curv2_knotvector[i] = 1.0 - curv2_knotvector[i]

    #         curv1_knotvector = np.asarray(curv1_knotvector)
    #         curv1_ctrlpts = np.asarray(curv1_ctrlpts)

    #         curv2_knotvector = np.asarray(curv2_knotvector)
    #         curv2_ctrlpts = np.asarray(curv2_ctrlpts)

    #         curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
    #         curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
    #         curv = curv1.attach_nurbs(curv2)

    #     elif init_pt1 and not init_pt2:

    #         curv1_knotvector = np.asarray(curv1_knotvector)
    #         curv1_ctrlpts = np.asarray(curv1_ctrlpts)

    #         curv2_knotvector = np.asarray(curv2_knotvector)
    #         curv2_ctrlpts = np.asarray(curv2_ctrlpts)

    #         curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
    #         curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
    #         curv = curv2.attach_nurbs(curv1)

    #     elif not init_pt1 and init_pt2:

    #         curv1_knotvector = np.asarray(curv1_knotvector)
    #         curv1_ctrlpts = np.asarray(curv1_ctrlpts)

    #         curv2_knotvector = np.asarray(curv2_knotvector)
    #         curv2_ctrlpts = np.asarray(curv2_ctrlpts)

    #         curv1 = nrb.NurbsCurve(control_points=curv1_ctrlpts, degree=deg, knots=curv1_knotvector)
    #         curv2 = nrb.NurbsCurve(control_points=curv2_ctrlpts, degree=deg, knots=curv2_knotvector)
    #         curv = curv1.attach_nurbs(curv2)

    #     curv_geomdl = CubicSpline()
    #     curv_geomdl.nurbs = NURBS.Curve()
    #     curv_geomdl.nurbs.degree = curv.degree
    #     curv_geomdl.nurbs.ctrlpts = curv.control_points
    #     curv_geomdl.nurbs.knotvector = curv.knots
    #     curv_geomdl.nurbs.sample_size = 10

    #     L1 = _curv1.length(0.0, 1.0)
    #     L2 = _curv2.length(0.0, 1.0)
    #     L = (L1 + L2) / 2.0
    #     curv_geomdl.eqPoly = Curve.genEquivPolyline(curv_geomdl, curv_geomdl.eqPoly, 0.001 * L)
    #     curv_geomdl.eqPoly.append(Pnt2D(curv_geomdl.nurbs.ctrlpts[-1][0], curv_geomdl.nurbs.ctrlpts[-1][1]))

    #     return curv_geomdl, None
