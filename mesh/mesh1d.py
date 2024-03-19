from compgeom.pnt2d import Pnt2D


class Mesh1D():

    @staticmethod
    def subdivideLine(_p1, _p2, _nsudv, _quad, _ratio):
        coords = []
        n_pts = _nsudv-1
        if _quad:
            n_pts = (_nsudv*2) - 1

        for i in range(0, n_pts):
            coords.insert(i, Pnt2D())

        # find the edge endpoint coordinates and get the vertices coordinates
        x0 = _p1.x
        y0 = _p1.y
        x1 = _p2.x
        y1 = _p2.y

        _ratio = 1.0 / _ratio
        a = (2.0 * _ratio) / ((_ratio + 1.0) * _nsudv)
        b = (a * (1.0 - _ratio)) / (2.0 * _ratio * (_nsudv - 1.0))

        if _quad:
            # --------------- subdivision for quadratic type elements -------------
            # get the coordinates at the segment ends
            j = 1
            for i in range(1, _nsudv):
                v = a * i + b * i * (i - 1.0)
                u = 1.0 - v
                coords[j].x = u * x0 + v * x1
                coords[j].y = u * y0 + v * y1
                j += 2

            #  --------- get the coordinates at the mid segment points ------------
            # first point on the first segment
            coords[0].x = (x0 + coords[1].x) * 0.5
            coords[0].y = (y0 + coords[1].y) * 0.5

            # now the points on the center segments
            j = 2
            for i in range(1, _nsudv-1):
                coords[j].x = (coords[j-1].x + coords[j+1].x) * 0.5
                coords[j].y = (coords[j-1].y + coords[j+1].y) * 0.5
                j += 2

            # now the point on the last segment
            coords[2*_nsudv-2].x = (coords[2*_nsudv-3].x + x1) * 0.5
            coords[2*_nsudv-2].y = (coords[2*_nsudv-3].y + y1) * 0.5
        else:
            #  ---------- subdivision for non-quadratic type elements ------------
            # get the coordinates at the segment ends
            for i in range(1, _nsudv):
                v = a * i + b * i * (i - 1.0)
                u = 1.0 - v
                coords[i-1].x = u * x0 + v * x1
                coords[i-1].y = u * y0 + v * y1

        return coords

    @staticmethod
    def subdivideSegment(_segment, _nsbdv, _ratio, _isQuadratic, _isIsogeometric):
        coords = []
        pts = []

        if not _isIsogeometric:

            if _nsbdv == 0 or _ratio == 0:
                return coords
            elif _nsbdv == 1:
                if _isQuadratic:
                    coords.append(_segment.evalPoint(0.5))
                return coords

            # calculates as if it were straight to find interpolation parameters
            length = _segment.length()
            r1 = Pnt2D(0.0, 0.0)
            r2 = Pnt2D(length, 0.0)
            coords = Mesh1D.subdivideLine(r1, r2, _nsbdv, _isQuadratic, _ratio)

            # calculates the coordinates of the real points on the segment
            for coord in coords:
                t = coord.x / length
                pts.append(_segment.evalPoint(t))

            return pts

        elif _isIsogeometric:
            # Check if knotvector contains a knot different from 0 or 1
            # if so, segment has more than one subdivision
            knots = _segment.curve.nurbs.knotvector
            # one_sdv = True
            # for i in knots:
            #     if i != 0.0 or i != 1.0:
            #         one_sdv = False
            #         break

            # if one_sdv is True:
            #     if _quad:
            #         coords.append(_segment.evalPoint(0.5))
            #     return coords

            knots = list(set(knots)) # Remove duplicates
            knots.sort()
            knots.pop()
            knots.pop(0)
            for t in knots:
                pts.append(_segment.evalPoint(t))

            return pts
        
