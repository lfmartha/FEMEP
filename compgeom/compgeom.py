from compgeom.pnt2d import Pnt2D


class CompGeom:

    ABSTOL = 1e-7  # Absolute tolerance value
    PI = 3.1415926535897932384626433832975028841971693993751058

    # ---------------------------------------------------------------------
    # pickLine: check to see if given point 'pt' touches given line
    # 'pt0-pt1' based on given tolerance. Uses auxiliary method
    # pickCode. The algorithm is based on an incomplete version of the
    # algorithm for clipping a line against a rectangle. The advantage is
    # that it descarts rapidly non-trivial picks. The 'clipping' area
    # is a square with side equal to two 'tol' values around the given
    # point.
    @staticmethod
    def pickCode(_x, _y, _xmin, _xmax, _ymin, _ymax):
        cod = [_x < _xmin, _x > _xmax, _y < _ymin, _y > _ymax]
        return cod

    @staticmethod
    def pickLine(_pt0, _pt1, _pt, _tol):
        x0 = _pt0.getX()
        y0 = _pt0.getY()
        x1 = _pt1.getX()
        y1 = _pt1.getY()
        x = _pt.getX()
        y = _pt.getY()
        # Define atraction window.
        xmin = x - _tol
        xmax = x + _tol
        ymin = y - _tol
        ymax = y + _tol

        cod1 = CompGeom.pickCode(x1, y1, xmin, xmax, ymin, ymax)
        while True:
            cod0 = CompGeom.pickCode(x0, y0, xmin, xmax, ymin, ymax)

            count = 0
            for i in range(0, 4):
                if cod0[i] and cod1[i]:  # Test no-trivial pick
                    break
                else:
                    count += 1
            if count != 4:
                break

            # Move point 0 to window limit.
            if cod0[0]:
                y0 += (xmin - x0) * (y1 - y0) / (x1 - x0)
                x0 = xmin
            elif cod0[1]:
                y0 += (xmax - x0) * (y1 - y0) / (x1 - x0)
                x0 = xmax
            elif cod0[2]:
                x0 += (ymin - y0) * (x1 - x0) / (y1 - y0)
                y0 = ymin
            elif cod0[3]:
                x0 += (ymax - y0) * (x1 - x0) / (y1 - y0)
                y0 = ymax
            else:
                return True

        return False

    # ---------------------------------------------------------------------
    # Get closest point on line segment 'p1'-'p2'.
    # Returns the distance between given point and closest point.
    # Also returns parametric value (between 0 and 1) of closest point
    # along the line.
    # A closest point outside the limits of segment 'p1-p2' is
    # snapped to one of the segment end points.
    @staticmethod
    def getClosestPointSegment(_p1, _p2, _p):
        # **** COMPLETE HERE: COMPGEOM_01 ****
        v12 = _p2 - _p1
        v1p = _p - _p1

        t = Pnt2D.dotprod(v12, v1p) / Pnt2D.sizesquare(v12)

        if abs(t) < CompGeom.ABSTOL or t < 0.0:
            pC = _p1
            t = 0.0
        elif abs(t-1.0) < CompGeom.ABSTOL or t > 1.0:
            pC = _p2
            t = 1.0
        else:
            pC = _p1 + v12 * t

        dist = Pnt2D.euclidiandistance(pC, _p)
        # **** COMPLETE HERE: COMPGEOM_01 ****
        return dist, pC, t

    # ---------------------------------------------------------------------
    @staticmethod
    def orient2d(pa, pb, pc):
        acx = pa[0] - pc[0]
        bcx = pb[0] - pc[0]
        acy = pa[1] - pc[1]
        bcy = pb[1] - pc[1]
        return acx * bcy - acy * bcx

    # ---------------------------------------------------------------------
    # Return the sign (NEGATIVE, ZERO, or POSITIVE) of the oriented
    # twice area formed by three given points.
    @staticmethod
    def signOrient2d(_p1, _p2, _p3):

        det = 0.0
        pa = [_p1.getX(), _p1.getY()]
        pb = [_p2.getX(), _p2.getY()]
        pc = [_p3.getX(), _p3.getY()]

        det = CompGeom.orient2d(pa, pb, pc)
        if(det != 0.0):
            if(det > 0.0):
                return 'POSITIVE'
            else:
                return 'NEGATIVE'

        return 'ZERO'

    # ---------------------------------------------------------------------
    # Return the signed value of the oriented twice area formed by
    # three given points.
    @staticmethod
    def valOrient2d(_p1, _p2, _p3):
        pa = [_p1.getX(), _p1.getY()]
        pb = [_p2.getX(), _p2.getY()]
        pc = [_p3.getX(), _p3.getY()]

        det = CompGeom.orient2d(pa, pb, pc)
        return det

     # ---------------------------------------------------------------------
   # Return a flag (true or false) stating whether the three given
    # points are collinear.
    @staticmethod
    def areCollinear(_p1,  _p2, _p3):
        return CompGeom.signOrient2d(_p1, _p2, _p3) == 'ZERO'

    # ---------------------------------------------------------------------
    # Return a flag (true or false) stating whether the third given
    # point is on the left side of oriented segment formed by the
    # first given points.
    @staticmethod
    def isLeftSide(_p1, _p2, _p3):
        return CompGeom.signOrient2d(_p1, _p2, _p3) == 'POSITIVE'

     # ---------------------------------------------------------------------
   # Return a flag (true or false) stating whether the third given
    # point is on the right side of oriented segment formed by the
    # first given points.
    @staticmethod
    def isRightSide(_p1, _p2, _p3):
        return CompGeom.signOrient2d(_p1, _p2, _p3) == 'NEGATIVE'

    # ---------------------------------------------------------------------
    # Return the sign (NEGATIVE, ZERO, or POSITIVE) of the oriented
    # twice area formed by three given points.
    # This function uses conventional floating-point operations to
    # compute the area and compares the area result with a hard-coded
    # very small tolerance value (ABSTOL).
    @staticmethod
    def signArea2d(_p1, _p2, _p3):
        det = Pnt2D.area2d(_p1, _p2, _p3)
        if abs(det) < CompGeom.ABSTOL:
            return 'ZERO'
        if det > 0.0:
            return 'POSITIVE'
        return 'NEGATIVE'

    # ---------------------------------------------------------------------
    # Return the signed value of the oriented twice area formed by
    # three given points.
    # This function uses conventional floating-point operations to
    # compute the signed area.
    @staticmethod
    def valArea2d(_p1,  _p2, _p3):
        return Pnt2D.area2d(_p1, _p2, _p3)

     # ---------------------------------------------------------------------
   # Check for collinear segments 'p1'-'p2' and 'p3'-'p4'.
    @staticmethod
    def checkCollinearSegments(_p1, _p2, _p3, _p4):
        sign123 = CompGeom.signArea2d(_p1, _p2, _p3)
        sign124 = CompGeom.signArea2d(_p1, _p2, _p4)

        # Check for collinear segments
        if sign123 == 'ZERO' and sign124 == 'ZERO':
            return True
        return False

    # ---------------------------------------------------------------------
    # Checks for two line segments intersection:
    # Checks whether segment 'p1'-'p2' intercepts segment 'p3'-'p4'.
    # Returns an integer intersection type value.
    # In case there is intersection, outputs the result in 'pi' parameter
    # and returns parametric values ('t12' and 't34' between 0 and 1) along
    # the two segments.
    # Ref.:
    # M. Gavrilova & J.G. Rokne - Reliable line segment intersection testing,
    # Computer-Aided Design, Vol. 32, Issue 12, pp. 737-745, 2000.
    @staticmethod
    def computeSegmentSegmentIntersection(_p1, _p2, _p3, _p4):
        # Discard intersection if second segment is located to the left (_l) or
        # to the right (_r) of horizontal bounding box limits of first segment.
        x12_l = min(_p1.getX(), _p2.getX())
        x12_r = max(_p1.getX(), _p2.getX())
        x34_l = min(_p3.getX(), _p4.getX())
        x34_r = max(_p3.getX(), _p4.getX())

        if (x12_r + CompGeom.ABSTOL) < x34_l or x34_r < (x12_l - CompGeom.ABSTOL):
            return 'DO_NOT_INTERSECT', None, None, None

        # Discard intersection if second segment is located below
        # bottom (_b) or above top (_t) of bounding box of first segment.
        y12_b = min(_p1.getY(), _p2.getY())
        y12_t = max(_p1.getY(), _p2.getY())
        y34_b = min(_p3.getY(), _p4.getY())
        y34_t = max(_p3.getY(), _p4.getY())

        if (y12_t + CompGeom.ABSTOL) < y34_b or y34_t < (y12_b - CompGeom.ABSTOL):
            return 'DO_NOT_INTERSECT', None, None, None

        # Get signs of oriented twice area for points p1-p2-p3 and for points p1-p2-p4
        sign123 = CompGeom.signArea2d(_p1, _p2, _p3)
        sign124 = CompGeom.signArea2d(_p1, _p2, _p4)

        # Check for collinear segments
        # **** COMPLETE HERE: COMPGEOM_02 ****
        if sign123 == 'ZERO' and sign124 == 'ZERO':
            return 'COLLINEAR', None, None, None
        # **** COMPLETE HERE: COMPGEOM_02 ****

        # Check for second segment on the same side of first segment
        # **** COMPLETE HERE: COMPGEOM_03 ****
        if ((sign123 == 'POSITIVE' and sign124 == 'POSITIVE') or
            (sign123 == 'NEGATIVE' and sign124 == 'NEGATIVE')):
            return 'DO_NOT_INTERSECT', None, None, None
        # **** COMPLETE HERE: COMPGEOM_03 ****

        # Get signs of oriented twice area for points p3-p4-p1 and for points p3-p4-p2
        sign341 = CompGeom.signArea2d(_p3, _p4, _p1)
        sign342 = CompGeom.signArea2d(_p3, _p4, _p2)

        # Check for first segment on the same side of second segment
        # **** COMPLETE HERE: COMPGEOM_04 ****
        if ((sign341 == 'POSITIVE') and (sign342 == 'POSITIVE') or
            (sign341 == 'NEGATIVE' and sign342 == 'NEGATIVE')):
            return 'DO_NOT_INTERSECT', None, None, None
        # **** COMPLETE HERE: COMPGEOM_04 ****

        # Check for one point of second segment touching first segment.
        # Also compute the intersection point and the parametric values
        # ('t12' and 't34' between 0 and 1) along the two segments.
        # In this case, 't34' is either equal to 0 or equal to 1.
        # **** COMPLETE HERE: COMPGEOM_05 ****
        if sign123 == 'ZERO' or sign124 == 'ZERO':
            if sign123 == 'ZERO':
                t34 = 0.0
                pi = _p3
            elif sign124 == 'ZERO':
                t34 = 1.0
                pi = _p4
            if sign341 == 'ZERO':
                t12 = 0.0
                pi = _p1
            elif sign342 == 'ZERO':
                t12 = 1.0
                pi = _p2
            else:
                area341 = CompGeom.valArea2d(_p3, _p4, _p1)
                area342 = CompGeom.valArea2d(_p3, _p4, _p2)
                t12 = area341 / (area341 - area342)

            return 'TOUCH', pi, t12, t34
        # **** COMPLETE HERE: COMPGEOM_05 ****

        # Check for one point of first segment touching second segment
        # Also compute the intersection point and the parametric values
        # ('t12' and 't34' between 0 and 1) along the two segments.
        # In this case, 't12' is either equal to 0 or equal to 1.
        # **** COMPLETE HERE: COMPGEOM_06 ****
        if sign341 == 'ZERO' or sign342 == 'ZERO':
            if sign341 == 'ZERO':
                t12 = 0.0
                pi = _p1
            elif sign342 == 'ZERO':
                t12 = 1.0
                pi = _p2
            if sign123 == 'ZERO':
                t34 = 0.0
                pi = _p3
            elif sign124 == 'ZERO':
                t34 = 1.0
                pi = _p4
            else:
                area123 = CompGeom.valArea2d(_p1, _p2, _p3)
                area124 = CompGeom.valArea2d(_p1, _p2, _p4)
                t34 = area123 / (area123 - area124)

            return 'TOUCH', pi, t12, t34
        # **** COMPLETE HERE: COMPGEOM_06 ****

        # When get to this point, there is an intersection point of the
        # two segments. Compute parametric values of intersection point
        # along each segment.
        # **** COMPLETE HERE: COMPGEOM_07 ****
        area341 = CompGeom.valArea2d(_p3, _p4, _p1)
        area342 = CompGeom.valArea2d(_p3, _p4, _p2)
        area123 = CompGeom.valArea2d(_p1, _p2, _p3)
        area124 = CompGeom.valArea2d(_p1, _p2, _p4)
        t12 = area341 / (area341 - area342)
        t34 = area123 / (area123 - area124)
        # **** COMPLETE HERE: COMPGEOM_07 ****

        # Compute intersection point (there are two equivalent options)
        v34 = _p4 - _p3
        _pi = _p3 + v34*t34
        return 'DO_INTERSECT', _pi, t12, t34

    # ---------------------------------------------------------------------
    # This function classifies the projection of a given 'p' point w.r.t. a
    # given segment 'p1-p2'.
    # It returns the classified position of the projection of a point
    # along the infinite line that contains a given segment.
    # It also returns the parametric value of the project point along segment.
    # Its main use is to classify the points of two collinear segments,
    # but it may be used to classify points projected on the infinite line
    # that contains a segment.
    @staticmethod
    def getPtPosWrtSegment(_p1, _p2, _p):
        v12 = _p2 - _p1
        v1p = _p - _p1
        # Get parametric value of project point on segment line
        _t = Pnt2D.dotprod(v12, v1p) / Pnt2D.sizesquare(v12)

        if abs(_t) < CompGeom.ABSTOL:
            return 'START_SEG', _t  # At start point of segment
        elif abs(_t-1.0) < CompGeom.ABSTOL:
            return 'END_SEG', _t   # At end point of segment
        elif _t < 0.0:
            return 'BEFORE_SEG', _t   # Outside and before segment
        elif _t > 1.0:
            return 'AFTER_SEG', _t   # Outside and after segment
        return 'INSIDE_SEG', _t   # Inside segment

    # ---------------------------------------------------------------------
    @staticmethod
    def computeLineLineIntersection(_p1, _p2, _p3, _p4):

        pts = []
        paramA = []
        paramB = []

        status, pi, t12, t34 = CompGeom.computeSegmentSegmentIntersection(
            _p1, _p2, _p3, _p4)

        if status == 'DO_NOT_INTERSECT':
            return False, pts, paramA, paramB

        elif status == 'DO_INTERSECT':
            pts.append(pi)
            paramA.append(t12)
            paramB.append(t34)
            return True, pts, paramA, paramB

        elif status == 'COLLINEAR':
            pos3_12, t3_12 = CompGeom.getPtPosWrtSegment(_p1, _p2, _p3)
            pos4_12, t4_12 = CompGeom.getPtPosWrtSegment(_p1, _p2, _p4)
            pos1_34, t1_34 = CompGeom.getPtPosWrtSegment(_p3, _p4, _p1)
            pos2_34, t2_34 = CompGeom.getPtPosWrtSegment(_p3, _p4, _p2)

            if ((pos3_12 == 'BEFORE_SEG' and pos4_12 == 'BEFORE_SEG') or
                (pos3_12 == 'AFTER_SEG' and pos4_12 == 'AFTER_SEG')):
                # The two segments do not intercept
                return False, pts, paramA, paramB

            elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'START_SEG':
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'START_SEG' and pos4_12 == 'BEFORE_SEG':
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'END_SEG' and pos4_12 == 'AFTER_SEG':
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'END_SEG':
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'START_SEG' and pos4_12 == 'END_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(0.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'END_SEG1' and pos4_12 == 'START_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(1.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'INSIDE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p4)
                paramA.append(t4_12)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'BEFORE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p3)
                paramA.append(t3_12)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'END_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'END_SEG' and pos4_12 == 'BEFORE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'START_SEG' and pos4_12 == 'INSIDE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(0.0)

                # Store second pair of intersection parameters
                pts.append(_p4)
                paramA.append(t4_12)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'START_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(1.0)

                # Store second pair of intersection parameters
                pts.append(_p3)
                paramA.append(t3_12)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'INSIDE_SEG':

                if t3_12 < t4_12:
                    # Store fisrt pair of intersection parameters
                    pts.append(_p3)
                    paramA.append(t3_12)
                    paramB.append(0.0)

                    # Store second pair of intersection parameters
                    pts.append(_p4)
                    paramA.append(t4_12)
                    paramB.append(1.0)

                else:
                    # Store fisrt pair of intersection parameters
                    pts.append(_p4)
                    paramA.append(t4_12)
                    paramB.append(1.0)

                    # Store second pair of intersection parameters
                    pts.append(_p3)
                    paramA.append(t3_12)
                    paramB.append(0.0)

                return True, pts, paramA, paramB

            elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'AFTER_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

            elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'BEFORE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(t1_34)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

            elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'END_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p3)
                paramA.append(t3_12)
                paramB.append(0.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(1.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'END_SEG' and pos4_12 == 'INSIDE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p4)
                paramA.append(t4_12)
                paramB.append(1.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(0.0)
                return True, pts, paramA, paramB

            elif pos3_12 == 'START_SEG' and pos4_12 == 'AFTER_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(0.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

            elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'START_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p1)
                paramA.append(0.0)
                paramB.append(1.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

            elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'AFTER_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p3)
                paramA.append(t3_12)
                paramB.append(0.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

            elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'INSIDE_SEG':
                # Store fisrt pair of intersection parameters
                pts.append(_p4)
                paramA.append(t4_12)
                paramB.append(1.0)

                # Store second pair of intersection parameters
                pts.append(_p2)
                paramA.append(1.0)
                paramB.append(t2_34)
                return True, pts, paramA, paramB

        elif status == 'TOUCH':
            # one segments touches the other, in the middle or extremity!
            # checks if the curves are not consecutive segments
            # checks if the polygons touch at the extremities
            pts.append(pi)
            paramA.append(t12)
            paramB.append(t34)
            return True, pts, paramA, paramB

        return False, pts, paramA, paramB

    # ---------------------------------------------------------------------
    @staticmethod
    def splitSelfIntersected(_poly):

        # verifies for each pair of possible segments if they intersect, and
        # stores for both segments the parametric coordinate where intersection occurs
        iStatus = False
        segA_TotalLength = 0.0
        segB_TotalLength = 0.0
        intersecParams = []
        params = []
        pts = []
        for i in range(0, len(_poly)-1):
            segA_PartialLength = Pnt2D.euclidiandistance(
                _poly[i], _poly[i + 1])
            segB_TotalLength = segA_TotalLength + segA_PartialLength
            segB_PartialLength = 0.0

            for j in range(i+1, len(_poly)-1):
                segB_PartialLength = Pnt2D.euclidiandistance(
                    _poly[j], _poly[j + 1])
                status, pi, t12, t34 = CompGeom.computeSegmentSegmentIntersection(_poly[i], _poly[i + 1],
                                                                                  _poly[j], _poly[j + 1])

                if status == 'DO_NOT_INTERSECT':
                    # do nothing, continue the checking!
                    pass
                elif status == 'DO_INTERSECT':
                    # the straight segments intersect in the middle!
                    intersecParams.append([
                        segA_TotalLength + t12*segA_PartialLength, pi])
                    intersecParams.append([
                        segB_TotalLength + t34*segB_PartialLength, pi])
                    iStatus = True
                elif status == 'COLLINEAR':
                    # the straight segments are collinear !
                    pos3_12, t3_12 = CompGeom.getPtPosWrtSegment(
                        _poly[i], _poly[i + 1], _poly[j])
                    pos4_12, t4_12 = CompGeom.getPtPosWrtSegment(
                        _poly[i], _poly[i + 1], _poly[j + 1])
                    pos1_34, t1_34 = CompGeom.getPtPosWrtSegment(
                        _poly[j], _poly[j + 1], _poly[i])
                    pos2_34, t2_34 = CompGeom.getPtPosWrtSegment(
                        _poly[j], _poly[j + 1], _poly[i + 1])

                    if(pos3_12 == 'BEFORE_SEG' and pos4_12 == 'BEFORE_SEG' or
                       pos3_12 == 'AFTER_SEG' and pos4_12 == 'AFTER_SEG'):
                        # The two segments do not intercept
                        pass
                    elif((pos3_12 == 'BEFORE_SEG' and pos4_12 == 'START_SEG') or
                         (pos3_12 == 'START_SEG' and pos4_12 == 'BEFORE_SEG') or
                         (pos3_12 == 'END_SEG' and pos4_12 == 'AFTER_SEG') or
                         (pos3_12 == 'AFTER_SEG' and pos4_12 == 'END_SEG')):

                        # Segments simply touch at one end without overlapping
                        if i == 0 and j == len(_poly)-2:
                            segA_InterAtParam = segA_TotalLength
                            segB_InterAtParam = segB_TotalLength + segB_PartialLength
                            intersecParams.append(
                                [segA_InterAtParam, _poly[i]])
                            intersecParams.append(
                                [segB_InterAtParam, _poly[j + 1]])
                            iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'END_SEG':
                        # Segments have common end points: just delete second segment.
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, _poly[i + 1]])
                        intersecParams.append(
                            [segB_InterAtParam, _poly[i + 1]])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'START_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength
                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])
                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'INSIDE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34*segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + t4_12*segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j+1]])
                        intersecParams.append([segB_InterAtParam, _poly[j+1]])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'BEFORE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])
                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'END_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'BEFORE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'INSIDE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j+1]])
                        intersecParams.append([segB_InterAtParam, _poly[j+1]])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'START_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'INSIDE_SEG':
                        if t3_12 < t4_12:
                            segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength

                            # Store fisrt pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, _poly[j]])
                            intersecParams.append(
                                [segB_InterAtParam, _poly[j]])

                            segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength + segB_PartialLength

                            # Store second pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, _poly[j+1]])
                            intersecParams.append(
                                [segB_InterAtParam, _poly[j+1]])

                        else:
                            segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength + segB_PartialLength

                            # Store fisrt pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, _poly[j+1]])
                            intersecParams.append(
                                [segB_InterAtParam, _poly[j+1]])

                            segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength

                            # Store second pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, _poly[j]])
                            intersecParams.append(
                                [segB_InterAtParam, _poly[j]])

                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'AFTER_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'BEFORE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'END_SEG':
                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'INSIDE_SEG':
                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j+1]])
                        intersecParams.append([segB_InterAtParam, _poly[j+1]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'AFTER_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'START_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i]])
                        intersecParams.append([segB_InterAtParam, _poly[i]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'AFTER_SEG':
                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j]])
                        intersecParams.append([segB_InterAtParam, _poly[j]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'INSIDE_SEG':
                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[j+1]])
                        intersecParams.append([segB_InterAtParam, _poly[j+1]])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append([segA_InterAtParam, _poly[i+1]])
                        intersecParams.append([segB_InterAtParam, _poly[i+1]])
                        iStatus = True
                elif status == 'TOUCH':
                    # one segments touches the other

                    # avoid consecutive segments
                    if j != (i+1):
                        intersecParams.append(
                            [segA_TotalLength + t12*segA_PartialLength, pi])
                        intersecParams.append(
                            [segB_TotalLength + t34*segB_PartialLength, pi])
                        iStatus = True

                segB_TotalLength += segB_PartialLength

            segA_TotalLength += segA_PartialLength

        # removes duplicate elements
        unique_intersecParams = []
        for item in intersecParams:
            if item not in unique_intersecParams:
                unique_intersecParams.append(item)

        unique_intersecParams.sort()

        # Calculate the parameters based on its partial length
        for it in unique_intersecParams:
            params.append(it[0]/segA_TotalLength)
            pts.append(it[1])

        return iStatus, pts, params

    # ---------------------------------------------------------------------
    @staticmethod
    def computePolyPolyIntersection(_poly1, _poly2):

        # verifies for each pair of possible segments if they intersect, and
        # stores for both segments the parametric coordinate where intersection occurs
        segA_TotalLength = 0.0
        iStatus = False
        intersecParams = []
        paramA = []
        paramB = []
        pts = []
        overlap = []

        for i in range(0, len(_poly1)-1):
            segA_PartialLength = Pnt2D.euclidiandistance(
                _poly1[i], _poly1[i + 1])
            segB_PartialLength = 0.0
            segB_TotalLength = 0.0

            for j in range(0, len(_poly2)-1):

                segB_PartialLength = Pnt2D.euclidiandistance(
                    _poly2[j], _poly2[j + 1])
                status, pi, t12, t34 = CompGeom.computeSegmentSegmentIntersection(
                    _poly1[i], _poly1[i+1], _poly2[j], _poly2[j + 1])

                if status == 'DO_NOT_INTERSECT':
                    # do nothing, continue the checking
                    pass
                elif status == 'DO_INTERSECT':
                    # the straight segments intersect in the middle!
                    segA_InterAtParam = segA_TotalLength + t12 * segA_PartialLength
                    segB_InterAtParam = segB_TotalLength + t34 * segB_PartialLength
                    intersecParams.append(
                        [segA_InterAtParam, segB_InterAtParam, pi, False])
                    iStatus = True

                elif status == 'COLLINEAR':
                    pos3_12, t3_12 = CompGeom.getPtPosWrtSegment(
                        _poly1[i], _poly1[i + 1], _poly2[j])
                    pos4_12, t4_12 = CompGeom.getPtPosWrtSegment(
                        _poly1[i], _poly1[i + 1], _poly2[j + 1])
                    pos1_34, t1_34 = CompGeom.getPtPosWrtSegment(
                        _poly2[j], _poly2[j + 1], _poly1[i])
                    pos2_34, t2_34 = CompGeom.getPtPosWrtSegment(
                        _poly2[j], _poly2[j + 1], _poly1[i + 1])

                    if ((pos3_12 == 'BEFORE_SEG' and pos4_12 == 'BEFORE_SEG') or
                        (pos3_12 == 'AFTER_SEG' and pos4_12 == 'AFTER_SEG')):
                        # The two segments do not intercept
                        pass

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'START_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'BEFORE_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'AFTER_SEG':
                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i+1], False])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'END_SEG':
                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'END_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'START_SEG':
                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'INSIDE_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], True])

                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'BEFORE_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])
                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'END_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'BEFORE_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'INSIDE_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], True])

                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'START_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'INSIDE_SEG':

                        if t3_12 < t4_12:

                            segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength

                            # Store fisrt pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])

                            segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength + segB_PartialLength

                            # Store second pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])

                        else:

                            segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength + segB_PartialLength

                            # Store fisrt pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])

                            segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                            segB_InterAtParam = segB_TotalLength

                            # Store second pair of intersection parameters
                            intersecParams.append(
                                [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])

                        iStatus = True

                    elif pos3_12 == 'BEFORE_SEG' and pos4_12 == 'AFTER_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], True])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'BEFORE_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + t1_34 * segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], True])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'END_SEG':

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], True])
                        iStatus = True

                    elif pos3_12 == 'END_SEG' and pos4_12 == 'INSIDE_SEG':

                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], True])
                        iStatus = True

                    elif pos3_12 == 'START_SEG' and pos4_12 == 'AFTER_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'START_SEG':

                        segA_InterAtParam = segA_TotalLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i], False])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'INSIDE_SEG' and pos4_12 == 'AFTER_SEG':

                        segA_InterAtParam = segA_TotalLength + t3_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j], True])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], False])
                        iStatus = True

                    elif pos3_12 == 'AFTER_SEG' and pos4_12 == 'INSIDE_SEG':

                        segA_InterAtParam = segA_TotalLength + t4_12 * segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + segB_PartialLength

                        # Store fisrt pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly2[j + 1], True])

                        segA_InterAtParam = segA_TotalLength + segA_PartialLength
                        segB_InterAtParam = segB_TotalLength + t2_34 * segB_PartialLength

                        # Store second pair of intersection parameters
                        intersecParams.append(
                            [segA_InterAtParam, segB_InterAtParam, _poly1[i + 1], True])
                        iStatus = True

                elif status == 'TOUCH':

                    # one segments touches the other, in the middle or extremity!
                    # checks if the curves are not consecutive segments
                    # checks if the polygons touch at the extremities

                    segA_InterAtParam = segA_TotalLength + t12 * segA_PartialLength
                    segB_InterAtParam = segB_TotalLength + t34 * segB_PartialLength
                    intersecParams.append(
                        [segA_InterAtParam, segB_InterAtParam, pi, False])
                    iStatus = True

                segB_TotalLength += segB_PartialLength

            segA_TotalLength += segA_PartialLength

        if iStatus:
            # removes repeated consecutive parametric values
            unrepeated_intersecParams = []
            prev = intersecParams[0]
            unrepeated_intersecParams.append(prev)
            for i in range(1, len(intersecParams)):
                curr = intersecParams[i]
                if((abs(curr[0] - prev[0]) > CompGeom.ABSTOL) and
                (abs(curr[1] - prev[1]) > CompGeom.ABSTOL)):
                    unrepeated_intersecParams.append(curr)
                prev = curr

            # removes duplicate elements
            unique_intersecParams = []
            for item in unrepeated_intersecParams:
                if item not in unique_intersecParams:
                    unique_intersecParams.append(item)

            # sorts the pairs of params by the _poly1 parametric order
            unique_intersecParams.sort()

            for it in unique_intersecParams:
                paramA.append(it[0]/segA_TotalLength)
                paramB.append(it[1]/segB_TotalLength)
                pts.append(it[2])
                overlap.append(it[3])

        return iStatus, pts, paramA, paramB, overlap

    # ---------------------------------------------------------------------
    # This function returns a flag indicating whether the vertices
    # of a polygon are in counter-clockwise order.
    # The algorithm is as follows:
    # Traverse the loop of coordinates, assuming that it is in counter-
    # clockwise order, computing the components of the 'area' of the
    # enclosed polygon.  The total 'area' components are computed by
    # adding 'area' components (cross product components) of
    # triangles sides formed by the first, previous, and current
    # vertices.  If the loop is not convex, some of the triangle
    # areas might be negative, but those will be compensated by other
    # positive triangle areas so that the final area is positive.
    # (area here is actually twice the area).
    # (positive here means in the direction of the face normal).
    @staticmethod
    def isCounterClockwisePolygon(_poly):
        area = 0.0  # twice the enclosed polygon area

        # Compute area assuming that polygon is in counter-clockwise order
        for i in range(2, len(_poly)):
            area += Pnt2D.area2d(_poly[0], _poly[i-1], _poly[i])

        # If area is greater than zero, then polygon is in counter-clockwise
        # order, otherwise it is in clockwise order.
        if area > 0.0:
            return True
        return False

    # ---------------------------------------------------------------------
    # This function returns a flag indicating whether the given point 'p'
    # is inside a polygon 'poly'.
    # The algorithm counts the number of intersections that a horizontal
    # line emanating at the point 'p' in positive x direction makes with
    # the boundary lines of the polygon. If the number of intersections
    # is odd, the point is inside de polygon. Otherwise, it is outside
    # the polygon.
    # If ray passes at an horizontal segment on polygon boundary, do not
    # count any intersection.
    # If ray passes at a vertex of the polygon, only consider intersection
    # if boundary segment is above ray.
    @staticmethod
    def isPointInPolygon(_poly, _p):
        x = _p.getX()
        y = _p.getY()
        n = len(_poly)  # number of polygon points
        ni = 0  # number of intersections

        for i in range(0, n):
            p1 = _poly[i]  # first point of current line segment
            p2 = _poly[(i+1) % n]  # second point of current line segment

        # **** COMPLETE HERE: COMPGEOM_08 ****
            if (p1.getY() == p2.getY()):  # discard horizontal line
                continue

            if p1.getY() > y and p2.getY() > y:  # discard line above ray
                continue

            if p1.getX() < x and p2.getX() < x:  # discard line to the left of point
                continue

            if p1.getY() < y and p2.getY() < y:  # Discard line below ray
                continue

            if p1.getY() == y:  # ray passes at first line point
                if p1.getX() > x and p2.getY() > y:
                    # Count intersection if first point is to the right of given point
                    # and second point is above.
                    ni += 1
            else:
                if p2.getY() == y:  # ray passes at second point
                    if p2.getX() > x and p1.getY() > y:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                else:  # ray passes with first and second points
                    if p1.getX() > x and p2.getX() > x:
                        # Count intersection if first point is to the right of given point
                        # and second point is above.
                        ni += 1
                    else:
                        # Compute x coordinate of intersection of ray with line segment
                        dx = p1.getX() - p2.getX()
                        xc = p1.getX()

                        if dx != 0.0:
                            xc += (y - p1.getY()) * dx / (p1.getY() - p2.getY())

                        if xc > x:
                            # Count intersection if first point is to the right of given point
                            # and second point is above.
                            ni += 1
        # **** COMPLETE HERE: COMPGEOM_08 ****

        # If number of intersections is odd, point is inside polygon.
        if (ni % 2) > 0:
            return True

        # If number of intersections if even, point is outside polygon.
        return False

    # ---------------------------------------------------------------------
    # @staticmethod
    # def computeLine_offset(_line, _offset, _t1, _t2, _orient):

    #     pts = _line.getPoints()
    #     v1 = pts[0] - pts[1]
    #     Pa_b = _line.evalPoint(_t1)
    #     Pc_d = _line.evalPoint(_t2)
    #     a = Pa_b.getX()
    #     b = Pa_b.getY()
    #     d = _offset*_offset
    #     e = v1.getX()
    #     f = v1.getY()

    #     if _orient:
    #         root = 2 * math.sqrt(d*((f*f)+(e*e)))
    #         if abs(f) <= CompGeom.ABSTOL and v1.getX() > 0:
    #             _offset = -_offset
    #     else:
    #         root = - 2 * math.sqrt(d*((f*f)+(e*e)))
    #         if abs(f) <= CompGeom.ABSTOL and v1.getX() < 0:
    #             _offset = -_offset

    #     if abs(f) <= CompGeom.ABSTOL:
    #         p1_x = a
    #         p1_y = b + _offset
    #     else:
    #         p1_x = f*((2*a*f)+(2*e*e*a/(f)) + root) / ((2*f*f)+(2*e*e))
    #         p1_y = (((a-p1_x)*e)/f) + b

    #     a = Pc_d.getX()
    #     b = Pc_d.getY()

    #     if abs(f) <= CompGeom.ABSTOL:
    #         p2_x = a
    #         p2_y = b + _offset
    #     else:
    #         p2_x = f*((2*a*f)+(2*e*e*a/(f)) + root)/((2*f*f)+(2*e*e))
    #         p2_y = (((a-p2_x)*e)/f) + b

    #     return Pnt2D(p1_x, p1_y), Pnt2D(p2_x, p2_y)
