from compgeom.compgeom import CompGeom


class Tesselation:
    @staticmethod
    def triangleParing(_p):
        triangs = []
        pn = len(_p)
        left = []  # left neighbor indices
        right = []  # right neighbor indices
        isPolyPt = []

        for i in range(0, pn):
            # initialization
            left.append(((i-1) + pn) % pn)
            right.append(((i+1) + pn) % pn)
            isPolyPt.append(True)

        i = pn-1  # counter

        while len(triangs) < (pn-2):

            i = right[i]
            if (Tesselation.ear_Q(left[i], i, right[i], _p, isPolyPt)):
                # Original implementation (SKIENA & REVILLA, 2002):
                # add_triangle(t,l[i],i,r[i],p);
                tri = [None, None, None]

                tri[0] = left[i]
                tri[1] = i
                tri[2] = right[i]
                triangs.append(tri)
                isPolyPt[i] = False

                # update left and right neighbor lists
                left[right[i]] = left[i]
                right[left[i]] = right[i]

        del right
        del left
        del isPolyPt

        return triangs

    # Original implementation (SKIENA & REVILLA, 2002)
    # creates a ear for the hull
    @staticmethod
    def ear_Q(_i,  _j,  _k,  _p, _isPolyPt):
        t = [None, None, None]  # coordinates for points i,j,k
        t[0] = _p[_i]
        t[1] = _p[_j]
        t[2] = _p[_k]

        # Check for angle ijk (centered in j) greater then 180 degrees
        if Tesselation.cw(t[0], t[1], t[2]):
            return False

        for m in range(0, len(_p)):
            if _isPolyPt[m]:
                if _p[m] != t[0] and _p[m] != t[1] and _p[m] != t[2]:
                    if Tesselation.point_in_triangle(_p[m], t):
                        return False

        return True

    # verifies if the order of the triangle connectivity
    @staticmethod
    def cw(_a,  _b, _c):
        return not (CompGeom.isLeftSide(_a, _b, _c))

    # computes the area of a triangle keeping the sign of orientation
    @staticmethod
    def signed_triangle_area(_a,  _b,  _c):
        return((_a.getX()*_b.getY() - _a.getY()*_b.getX()
                + _a.getY()*_c.getX() - _a.getX()*_c.getY()
                + _b.getX()*_c.getY() - _c.getX()*_b.getY()) / 2.0)

    # verifies if the point _p is inside the triangle _t7
    @staticmethod
    def point_in_triangle(_p,  _t):

        for i in range(0, 3):
            if(CompGeom.isRightSide(_t[i], _t[(i+1) % 3], _p)):
                return False
        return True

    @staticmethod
    def tessellate(_polygon):
        counter = 0
        triangs = []
        pn = len(_polygon)
        left = []  # left neighbor indices
        right = []  # right neighbor indices
        isPolyPt = []

        for i in range(0, pn):
            # initialization
            left.append(((i-1) + pn) % pn)
            right.append(((i+1) + pn) % pn)
            isPolyPt.append(True)

        i = pn-1  # counter

        # Check for endless loop
        currSize = pn
        loopCount = 0

        while len(triangs) < (pn-2):
            i = right[i]
            if (Tesselation.ear_Q(left[i], i, right[i], _polygon, isPolyPt)):
                # Original implementation (SKIENA & REVILLA, 2002):
                # add_triangle(t,l[i],i,r[i],p);
                tri = [None, None, None]

                tri[0] = left[i]
                tri[1] = i
                tri[2] = right[i]
                triangs.append(tri)
                isPolyPt[i] = False

                # update left and right neighbor lists
                left[right[i]] = left[i]
                right[left[i]] = right[i]

                currSize -= 1
                loopCount = 0

            else:
                loopCount += 1

            if loopCount >= currSize:
                triangs.clear()
                return triangs

        del right
        del left
        del isPolyPt

        return triangs
