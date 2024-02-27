from geometry.point import Point
from geometry.curves.line import Line
from compgeom.compgeom import CompGeom
from mesh.mesh1d import Mesh1D
import math


class AttribSymbols:

    @staticmethod
    def getSymbol(_attribute, _scale, _pt=None, _seg=None, _patch=None):

        lines = []
        triangles = []
        squares = []
        points = []
        circles = []
        time = "before"  # determines whether the attribute will be drawn before or after

        if _attribute['symbol'] == 'Support':
            time = "before"
            if _pt is not None:
                lines, triangles, squares, circles = AttribSymbols.supportPoint(
                    _attribute, _pt, _scale)
            else:
                lines, triangles, squares, circles = AttribSymbols.supportSegment(
                    _attribute, _seg, _scale)

        elif _attribute['symbol'] == 'Arrow':

            if _attribute['type'] == "Concentrated Load":
                time = "after"
                if _pt is not None:
                    lines, triangles, circles = AttribSymbols.arrowPointCL(
                        _attribute, _pt, _scale)

            elif _attribute['type'] == "Uniform Load":
                time = "after"
                if _seg is not None:
                    lines, triangles = AttribSymbols.arrowSegmentUL(
                        _attribute, _seg, _scale)

            elif _attribute['type'] == "Pressure":
                if _patch is not None:
                    lines, triangles = AttribSymbols.arrowPressure(
                        _attribute, _patch, _scale)
                    
            elif _attribute['type'] == "Direction":
                time = "after"
                if _seg is not None:
                    lines, triangles = AttribSymbols.arrowSegmentDirec(
                        _seg, _scale)

        elif _attribute['symbol'] == 'Nsbdvs':
            time = "after"
            if _seg is not None:
                points = AttribSymbols.Nsbdvs(_attribute, _seg)

        elif _attribute['symbol'] == 'Temperature':
            time = "after"

            if _pt is not None:
                lines = AttribSymbols.temperaturePoint(_pt, _scale)
            elif _seg is not None:
                lines = AttribSymbols.temperatureSegment(_seg, _scale)
            else:
                lines = AttribSymbols.temperaturePatch(_patch, _scale)

        elif _attribute['symbol'] == 'Flux':
            time = "after"
            if _pt is not None:
                triangles, circles = AttribSymbols.fluxPoint(_pt, _scale)
            elif _seg is not None:
                triangles, circles = AttribSymbols.fluxSegment(_seg, _scale)
            else:
                triangles, circles = AttribSymbols.fluxPatch(_patch, _scale)

        # get the colors
        colors = []
        index = 0

        for att_type in _attribute['properties_type']:
            if att_type == "color":
                colors.append(list(_attribute['properties'].values())[index].copy())
            index += 1

        symbol = {
            "lines": lines,
            "triangles": triangles,
            "squares": squares,
            "circles": circles,
            "colors": colors,
            "points": points,
            "time": time
        }

        return symbol

    @ staticmethod
    def rotateCoord(_pt, _ang):
        pt = Point(_pt.getX(), _pt.getY())
        x = (pt.x*(math.cos(_ang))) + (pt.y*(math.sin(_ang)))
        y = (pt.y*(math.cos(_ang))) - (pt.x*(math.sin(_ang)))
        return Point(x, y)

    @ staticmethod
    def getAngWithXDirec(_v2):
        v1 = Point(1, 0)
        ang = math.acos(Point.dotprod(v1, _v2)/((Point.size(v1)) *
                                                (Point.size(_v2))))
        ang = ang*180/CompGeom.PI

        return ang

    @ staticmethod
    def triangleSymbol(_pt, _scale, _ang):

        _ang = _ang*CompGeom.PI/180
        x = AttribSymbols.rotateCoord(Point(1*_scale, 0), _ang)
        y = AttribSymbols.rotateCoord(Point(0, 1*_scale), _ang)

        pt_a = _pt - x*0.75
        pt_b = pt_a + (y/2)
        pt_c = pt_a - (y/2)

        return [_pt, pt_b, pt_c]

    def squareSymbol(_pt, _scale, _ang):

        _ang = _ang*CompGeom.PI/180
        x = AttribSymbols.rotateCoord(Point(1*_scale, 0), _ang)
        y = AttribSymbols.rotateCoord(Point(0, 1*_scale), _ang)

        pt_a = _pt - (x/4) + (y/4)
        pt_b = _pt + (x/4) + (y/4)
        pt_c = _pt + (x/4) - (y/4)
        pt_d = _pt - (x/4) - (y/4)

        return [pt_a, pt_b, pt_c, pt_d]

    def circleSymbol(_pt, _r):
        x = _pt.getX()
        y = _pt.getY()
        num = 30
        circ_points = []

        for i in range(0, num+1):
            theta = 2*CompGeom.PI*i/num
            pt = Point(x + _r*math.cos(theta), y + _r*math.sin(theta))
            circ_points.append(pt)

        return circ_points

    def arcCircleSymbol(_pt, _r, _ang):
        x = _pt.getX()
        y = _pt.getY()
        _ang = int((360-_ang)/10)
        num = 36
        arc_points = []

        for i in range(0, num-_ang+1):
            theta = 2*CompGeom.PI*i/num
            pt = Point(x + _r*math.cos(theta), y + _r*math.sin(theta))
            arc_points.append(pt)

        return arc_points

    @ staticmethod
    def arrowSymbol(_pt, _scale, _ang):

        _ang = _ang*CompGeom.PI/180
        x = AttribSymbols.rotateCoord(Point(3*_scale, 0), _ang)
        y = AttribSymbols.rotateCoord(Point(0, 3*_scale), _ang)

        pt = _pt + x*0.1
        pt_a = pt + x*0.1
        pt_b = pt_a + y*0.1
        pt_c = pt_a - y*0.1
        pt_d = pt + x

        return [pt, pt_d], [pt, pt_b, pt_c]

    @ staticmethod
    def arrowSymbol2(_pt, _scale, _ang):

        _ang = _ang*CompGeom.PI/180
        x = AttribSymbols.rotateCoord(Point(3*_scale, 0), _ang)
        y = AttribSymbols.rotateCoord(Point(0, 3*_scale), _ang)

        pt = _pt + x*0.2
        pt_a = pt + x*0.3
        pt_b = pt_a + y*0.3
        pt_c = pt_a - y*0.3
        pt_d = pt + x

        return [pt, pt_d], [pt, pt_b, pt_c]
    
    @ staticmethod
    def arrowSymbol3(_pt, _scale, _ang):

        _ang = _ang*CompGeom.PI/180
        x = AttribSymbols.rotateCoord(Point(3*_scale, 0), -_ang)
        y = AttribSymbols.rotateCoord(Point(0, 3*_scale), -_ang)

        pt = _pt + x*0.1
        pt_d = pt + x*0.6
        pt_a = pt_d - x*0.1
        pt_b = pt_a + y*0.1
        pt_c = pt_a - y*0.1

        return [pt, pt_d], [pt_d, pt_b, pt_c]

    def arrowSegmentDirec(_seg, _scale):
        point = Point(_seg.getXinit(), _seg.getYinit())
        tan = _seg.getInitTangent()

        # Compute angle
        ang = math.atan2(tan.getY(), tan.getX())  # -PI < angle <= +PI
        if ang <= 0.0:
            ang += 2.0 * math.pi  # 0 <= angle < +2PI

        ang_norm1 = ang + math.pi / 2.0
        if ang_norm1 <= 0.0:
            ang_norm1 += 2.0 * math.pi  # 0 <= angle < +2PI

        ang_norm2 = ang - math.pi / 2.0
        if ang_norm2 <= 0.0:
            ang_norm2 += 2.0 * math.pi  # 0 <= angle < +2PI

        pt1 = AttribSymbols.rotateCoord(Point(point.getX() + 0.3*_scale, point.getY()), -ang_norm1)
        pt1 = AttribSymbols.rotateCoord(Point(0.3*_scale, 0), -ang_norm1)
        pt1 = point + pt1

        # pt2 = AttribSymbols.rotateCoord(Point(point.getX() + 0.3*_scale, point.getY()), -ang_norm2)
        # pt2 = AttribSymbols.rotateCoord(Point(0.3*_scale, 0), -ang_norm2)
        # pt2 = point + pt2

        ang = ang * 180.0 / math.pi
        line1, tr1 = AttribSymbols.arrowSymbol3(pt1, _scale, ang)
        #line2, tr2 = AttribSymbols.arrowSymbol3(pt2, _scale, ang)
        # line, tr = AttribSymbols.arrowSymbol3(point, _scale, ang)

        lines = [line1]
        triangles = [tr1]
        # lines = [line]
        # triangles = [tr]

        return lines, triangles

    def arrowPointCL(_attribute, _pt, _scale):

        properties = _attribute['properties']
        lines = []
        triangles = []
        circles = []

        if properties['Fx'] != 0:
            if properties['Fx'] < 0:
                line, tr = AttribSymbols.arrowSymbol(_pt, _scale, 0)
            else:
                line, tr = AttribSymbols.arrowSymbol(_pt, _scale, 180)
            lines.append(line)
            triangles.append(tr)

        if properties['Fy'] != 0:
            if properties['Fy'] < 0:
                line, tr = AttribSymbols.arrowSymbol(_pt, _scale, 270)

            else:
                line, tr = AttribSymbols.arrowSymbol(_pt, _scale, 90)

            lines.append(line)
            triangles.append(tr)

        if properties['Mz'] != 0:
            if properties['Mz'] < 0:
                cr = AttribSymbols.arcCircleSymbol(_pt, _scale, 180)
                tr = AttribSymbols.triangleSymbol(
                    cr[0], _scale*0.5, 90)
                circles.append(cr)
                triangles.append(tr)
            else:
                cr = AttribSymbols.arcCircleSymbol(_pt, _scale, 180)
                tr = AttribSymbols.triangleSymbol(
                    cr[-1], _scale*0.5, 90)
                circles.append(cr)
                triangles.append(tr)

        return lines, triangles, circles

    def arrowSegmentUL(_attribute, _seg, _scale):
        properties = _attribute['properties']
        lines = []
        triangles = []
        disp = Point(0, 0)
        points = _seg.getPoints().copy()

        while len(points) >= 2:
            aux_line = Line(points[0], points[1])

            if properties['Direction']["index"] == 1:
                local = True
                v = points[1] - points[0]
            else:
                local = False

            if properties['Qx'] != 0:
                if properties['Qx'] > 0:
                    ang = 180
                    if local:
                        ang = AttribSymbols.getAngWithXDirec(v)
                        if points[1].getY() < points[0].getY():
                            ang = ang + 180
                        else:
                            ang = - ang + 180

                    l, tr = AttribSymbols.arrowSegment(
                        _scale*0.45, disp, 0.2, 0.1, 0.9, aux_line, ang, True)
                else:
                    ang = 0
                    if local:
                        ang = AttribSymbols.getAngWithXDirec(v)
                        if not points[1].getY() < points[0].getY():
                            ang = -ang

                    l, tr = AttribSymbols.arrowSegment(
                        _scale*0.45, disp, 0.2, 0.1, 0.9, aux_line, ang, False)

                lines.extend(l)
                triangles.extend(tr)

            if properties['Qy'] != 0:
                if properties['Qy'] > 0:
                    ang = 90
                    if local:
                        ang = AttribSymbols.getAngWithXDirec(v)
                        if points[1].getY() < points[0].getY():
                            ang = ang + 90
                        else:
                            ang = -ang + 90

                    l, tr = AttribSymbols.arrowSegment(
                        _scale*0.5, disp, 0.2, 0, 1, aux_line, ang, True)
                else:
                    ang = 270
                    if local:
                        ang = AttribSymbols.getAngWithXDirec(v)
                        if points[1].getY() < points[0].getY():
                            ang = ang + 270
                        else:
                            ang = -ang + 270

                    l, tr = AttribSymbols.arrowSegment(
                        _scale*0.5, disp, 0.2, 0, 1, aux_line, ang, False)

                lines.extend(l)
                triangles.extend(tr)

            points.pop(0)

        return lines, triangles

    def arrowSegment(_scale, _displc, _step, _init, _end, _seg, _ang, _orient):

        lines = []
        triangles = []
        step = _step
        cont = _init

        if _orient:
            displc = _displc
        else:
            displc = _displc*(-1)

        while cont <= _end:
            pt = _seg.evalPoint(cont)
            pt = pt - displc*0.2
            l, tr = AttribSymbols.arrowSymbol(
                pt, _scale, _ang)
            lines.append(l)
            triangles.append(tr)
            cont = cont + step

        return lines, triangles

    def arrowPressure(_attribute, _patch, _scale):
        lines = []
        triangles = []
        properties = _attribute['properties']
        scale = _scale*0.20

        if _patch.mesh is not None:
            mesh_points = _patch.mesh.model.getPoints()

            if properties['Px'] != 0:
                if properties['Px'] < 0:
                    for pt in mesh_points:
                        line, tr = AttribSymbols.arrowSymbol2(pt, scale, 0)
                        lines.append(line)
                        triangles.append(tr)
                else:
                    for pt in mesh_points:
                        line, tr = AttribSymbols.arrowSymbol2(pt, scale, 180)
                        lines.append(line)
                        triangles.append(tr)

            if properties['Py'] != 0:
                if properties['Py'] < 0:
                    for pt in mesh_points:
                        line, tr = AttribSymbols.arrowSymbol2(pt, scale, 270)
                        lines.append(line)
                        triangles.append(tr)
                else:
                    for pt in mesh_points:
                        line, tr = AttribSymbols.arrowSymbol2(pt, scale, 90)
                        lines.append(line)
                        triangles.append(tr)

        return lines, triangles

    @ staticmethod
    def supportPoint(_attribute, _pt, _scale):
        _scale = _scale*0.6
        properties = _attribute['properties']
        x = Point(1*_scale, 0)
        y = Point(0, 1*_scale)
        lines = []
        triangles = []
        squares = []
        circles = []

        if properties['Dx']:

            pt = Point(_pt.getX(), _pt.getY())
            displac = Point(x.getX(), x.getY())

            if properties['Dx pos']["index"] == 0:
                displac = displac*(-1)
                # Left
                if properties['Rz']:
                    pt = pt + displac/4

                tr = AttribSymbols.triangleSymbol(pt, _scale, 0)
                pt_d = tr[1] - x*0.1
                pt_e = tr[2] - x*0.1
            else:
                # Right
                if properties['Rz']:
                    pt = pt + displac/4

                tr = AttribSymbols.triangleSymbol(pt, _scale, 180)
                pt_d = tr[1] + x*0.1
                pt_e = tr[2] + x*0.1

            lines.append([pt_d, pt_e])
            triangles.append(tr)

            if properties['Dx value'] != 0:

                if properties['Dx value'] < 0:

                    if displac.getX() < 0:
                        pt_arrow = (pt_d+pt_e)/2 + displac*2
                    else:
                        pt_arrow = (pt_d+pt_e)/2 + displac/4

                    l, tr = AttribSymbols.arrowSymbol(
                        pt_arrow, _scale*0.5, 0)
                else:
                    if displac.getX() < 0:
                        pt_arrow = (pt_d+pt_e)/2 + displac/4
                    else:
                        pt_arrow = (pt_d+pt_e)/2 + displac*2

                    l, tr = AttribSymbols.arrowSymbol(
                        pt_arrow, _scale*0.5, 180)

                lines.append(l)
                triangles.append(tr)

        if properties['Dy']:

            pt = Point(_pt.getX(), _pt.getY())
            displac = Point(y.getX(), y.getY())

            if properties['Dy pos']["index"] == 0:
                displac = displac*(-1)
                # Down
                if properties['Rz']:
                    pt = pt + displac/4

                tr = AttribSymbols.triangleSymbol(pt, _scale, 270)
                pt_d = tr[1] - y*0.1
                pt_e = tr[2] - y*0.1
            else:
                # Up
                if properties['Rz']:
                    pt = pt + displac/4

                tr = AttribSymbols.triangleSymbol(pt, _scale, 90)
                pt_d = tr[1] + y*0.1
                pt_e = tr[2] + y*0.1

            lines.append([pt_d, pt_e])
            triangles.append(tr)

            if properties['Dy value'] != 0:

                if properties['Dy value'] < 0:

                    if displac.getY() < 0:
                        pt_arrow = (pt_d+pt_e)/2 + displac*2
                    else:
                        pt_arrow = (pt_d+pt_e)/2 + displac/4

                    l, tr = AttribSymbols.arrowSymbol(
                        pt_arrow, _scale*0.5, 270)
                else:
                    if displac.getY() < 0:
                        pt_arrow = (pt_d+pt_e)/2 + displac/4
                    else:
                        pt_arrow = (pt_d+pt_e)/2 + displac*2

                    l, tr = AttribSymbols.arrowSymbol(
                        pt_arrow, _scale*0.5, 90)

                lines.append(l)
                triangles.append(tr)

        if properties['Rz']:
            sq = AttribSymbols.squareSymbol(_pt, _scale, 0)
            squares.append(sq)

            if properties['Rz value'] != 0:
                if properties['Rz value'] < 0:
                    cr = AttribSymbols.arcCircleSymbol(_pt, _scale*1.4, 180)
                    tr = AttribSymbols.triangleSymbol(
                        cr[0], _scale*0.5, 90)

                else:
                    cr = AttribSymbols.arcCircleSymbol(_pt, _scale*1.4, 180)
                    tr = AttribSymbols.triangleSymbol(
                        cr[-1], _scale*0.5, 90)

                circles.append(cr)
                triangles.append(tr)

        return lines, triangles, squares, circles

    @ staticmethod
    def supportSegment(_attribute, _seg, _scale):

        lines = []
        triangles = []
        squares = []
        circles = []
        points = []
        seg_pts = _seg.getPoints()
        points.append(seg_pts[0])
        points.append(seg_pts[-1])
        points.append(_seg.evalPoint(0.5))

        for pt in points:
            l, tr, sq, circ = AttribSymbols.supportPoint(
                _attribute, pt, _scale)
            lines.extend(l)
            triangles.extend(tr)
            squares.extend(sq)
            circles.extend(circ)

        return lines, triangles, squares, circles

    def Nsbdvs(_attribute, _seg):
        points = []
        properties = _attribute['properties']
        nsudv = properties['Value']
        ratio = properties['Ratio']
        isIsogeometric = properties['isIsogeometric']
        points = Mesh1D.subdivideSegment(_seg, nsudv, ratio, False, isIsogeometric)

        return points

    @ staticmethod
    def temperaturePoint(_point, _scale):
        sq = AttribSymbols.squareSymbol(_point, _scale*1.0, 0)
        x = Point(0.35*_scale, 0)
        y = Point(0, 0.15*_scale)

        lines = []

        for i in range(1, len(sq)):
            lines.append([sq[i-1], sq[i]])
        lines.append([sq[-1], sq[0]])

        a = _point - y
        b = _point + y
        c = b - x/2
        d = b + x/2

        lines.append([a, b])
        lines.append([c, d])

        return lines

    def temperatureSegment(_seg, _scale):
        lines = []
        points = []
        seg_pts = _seg.getPoints()
        points.append(seg_pts[0])
        points.append(seg_pts[-1])
        points.append(_seg.evalPoint(0.5))

        for pt in points:
            l = AttribSymbols.temperaturePoint(pt, _scale)
            lines.extend(l)

        return lines

    def temperaturePatch(_patch, _scale):
        lines = []

        if _patch.mesh is not None:
            mesh_points = _patch.mesh.model.getPoints()
            for pt in mesh_points:
                l = AttribSymbols.temperaturePoint(pt, _scale)
                lines.extend(l)

        return lines

    def fluxPoint(_point, _scale):
        scale = _scale*0.25
        triangles = []
        circles = []

        c = AttribSymbols.circleSymbol(_point, scale)
        circles.append(c)
        t = AttribSymbols.triangleSymbol(c[6], scale, 0)
        triangles.append(t)

        return triangles, circles

    def fluxSegment(_seg, _scale):
        triangles = []
        circles = []
        points = []
        seg_pts = _seg.getPoints()
        points.append(seg_pts[0])
        points.append(_seg.evalPoint(0.25))
        points.append(_seg.evalPoint(0.5))
        points.append(_seg.evalPoint(0.75))
        points.append(seg_pts[-1])
        for pt in points:
            t, c = AttribSymbols.fluxPoint(pt, _scale)
            triangles.extend(t)
            circles.extend(c)

        return triangles, circles

    def fluxPatch(_patch, _scale):
        triangles = []
        circles = []

        if _patch.mesh is not None:
            mesh_points = _patch.mesh.model.getPoints()
            for pt in mesh_points:
                t, c = AttribSymbols.fluxPoint(pt, _scale)
                triangles.extend(t)
                circles.extend(c)

        return triangles, circles
