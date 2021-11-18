from compgeom.compgeom import CompGeom
from PyQt5.QtWidgets import QMessageBox
import mesh.mesh2d.msh2d as msh2d
import mesh.auxmodule.auxmodule as aux
from geometry.segments.line import Line
from geometry.point import Point


class Mesh:
    def __init__(self, _model, _hecontroller, _mesh_dict=None):
        self.hecontroller = _hecontroller
        self.model = _model
        self.mesh_dict = _mesh_dict


class MeshGeneration:
    App = None

    def generation(_face, _mesh_type, _elem_type, _diag_type, _bc_flag):

        # get points
        segments = _face.patch.segments
        segmentOrients = _face.patch.segmentOrients

        polygon = []
        side_pts = []

        for i in range(0, len(segments)):
            segmentPol = segments[i].getPoints().copy()

            check, pts = MeshGeneration.getSubDvPts(segments[i], _elem_type)
            if check:
                segmentPol = pts

            side_pts.append(len(segmentPol))

            if segmentOrients[i]:
                for j in range(0, len(segmentPol)-1):
                    polygon.append(segmentPol[j])
            else:
                for j in range(len(segmentPol)-1, 0, -1):
                    polygon.append(segmentPol[j])

        if _mesh_type == 'Bilinear Transfinite':

            if _diag_type == "Right":
                diag_type = 1
            elif _diag_type == "Left":
                diag_type = 2
            elif _diag_type == "Union Jack":
                diag_type = 3
            else:
                diag_type = 4

            if len(segments) != 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 4')
                msg.exec()
                return False, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None

            m = side_pts[0]
            n = side_pts[1]

            genMesh = True
            for i in range(0, len(side_pts)):

                if i % 2 == 0:
                    if side_pts[i] != m:
                        genMesh = False
                        break
                elif side_pts[i] != n:
                    genMesh = False
                    break

            if genMesh:
                return MeshGeneration.Msh2DBilinear(polygon, _elem_type, diag_type, len(polygon))
            else:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'Opposite sides must have an equal number of subdivisions')
                msg.exec()
                return False, None, None, None, None, None

        elif _mesh_type == 'Trilinear Transfinite':

            if len(segments) != 3:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 3')
                msg.exec()
                return False, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None

            m = side_pts[0]
            for number in side_pts:
                if number != m:
                    msg = QMessageBox(MeshGeneration.App)
                    msg.setWindowTitle('Warning')
                    msg.setText(
                        'All sides must have the same number of subdivisions')
                    msg.exec()
                    return False, None, None, None, None, None
            return MeshGeneration.Msh2DTrilinear(polygon, _elem_type, m)

        elif _mesh_type == 'Quadrilateral Template':
            num_seg = len(segments)

            if num_seg > 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'The number of segments must be between 2 and 4')
                msg.exec()
                return False, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None

            subv = []
            for pts in side_pts:
                subv.append(pts - 1)

            return MeshGeneration.Msh2DTemplate(polygon, _elem_type, num_seg, subv)

        else:

            polygon.reverse()
            polygon.insert(0, polygon.pop(-1))
            num_seg = []
            num_seg.append(len(polygon))

            holes = _face.patch.holes
            holesOrients = _face.patch.holesOrients
            for i in range(0, len(holes)):
                hole_polygon = []
                for j in range(0, len(holes[i])):
                    segmentpol = holes[i][j].getPoints()
                    check, pts = MeshGeneration.getSubDvPts(
                        holes[i][j], _elem_type)
                    if check:
                        segmentpol = pts

                    if holesOrients[i][j]:
                        for m in range(0, len(segmentpol)-1):
                            hole_polygon.append(segmentpol[m])
                    else:
                        for m in range(len(segmentpol)-1, 0, -1):
                            hole_polygon.append(segmentpol[m])

                hole_polygon.reverse()
                hole_polygon.insert(0, hole_polygon.pop(-1))
                num_seg.append(len(hole_polygon))
                polygon.extend(hole_polygon)

            internalSegments = _face.patch.internalSegments
            internalSegmentsOrients = _face.patch.internalSegmentsOrients
            for i in range(0, len(internalSegments)):
                intSeg_polygon = []
                for j in range(0, len(internalSegments[i])):
                    segmentpol = internalSegments[i][j].getPoints()
                    check, pts = MeshGeneration.getSubDvPts(
                        internalSegments[i][j], _elem_type)
                    if check:
                        segmentpol = pts

                    if internalSegmentsOrients[i][j]:
                        for m in range(0, len(segmentpol)-1):
                            intSeg_polygon.append(segmentpol[m])
                    else:
                        for m in range(len(segmentpol)-1, 0, -1):
                            intSeg_polygon.append(segmentpol[m])

                intSeg_polygon.reverse()
                intSeg_polygon.insert(0, intSeg_polygon.pop(-1))
                num_seg.append(len(intSeg_polygon))
                polygon.extend(intSeg_polygon)

            num_loops = len(_face.intLoops) + 1

            if _mesh_type == 'Quadrilateral Seam':

                for number in side_pts:
                    if (number - 1) % 2 != 0:
                        msg = QMessageBox(MeshGeneration.App)
                        msg.setWindowTitle('Warning')
                        msg.setText(
                            'The number of edge subdvisions cannot be odd')
                        msg.exec()
                        return False, None, None, None, None, None

                return MeshGeneration.Msh2DQuadSeam(polygon, _elem_type, num_loops, num_seg)

            elif _mesh_type == 'Triangular Boundary Contraction':

                if _bc_flag == "Optimal":
                    return MeshGeneration.Msh2DShape(polygon, _elem_type, num_loops, num_seg)
                elif _bc_flag == "Regular Grid":
                    bc_flag = 0
                else:
                    bc_flag = 1

                return MeshGeneration.Msh2DBoundContraction(polygon, _elem_type, num_loops, num_seg, bc_flag)

    def getSubDvPts(_seg, _elem_type):

        if _seg.nsudv is not None:
            properties = _seg.nsudv['properties']
            number = properties['Value']
            ratio = properties['Ratio']
        else:
            number = 1.0
            ratio = 1.0

        if _elem_type == 6 or _elem_type == 8:
            quad = True
        else:
            quad = False

        if number == 0:
            number = 1

        pts = []
        pts = CompGeom.getNumberOfSudvisions(_seg, number, ratio, quad)
        pts.insert(0, _seg.getPoint(0))
        pts.append(_seg.getPoint(1))

        if len(pts) > 2:
            return True, pts
        else:
            return False, None

    def meshLines(_coords, _conn):

        points = []
        coords_copy = _coords.copy()
        while len(coords_copy) > 0:
            points.append(Point(coords_copy[0], coords_copy[1]))
            coords_copy.pop(0)
            coords_copy.pop(0)

        lines = []
        conn_copy = _conn.copy()
        while len(conn_copy) > 0:
            number = conn_copy.pop(0)

            for i in range(1, number):
                line = Line(points[conn_copy[i-1]], points[conn_copy[i]])
                lines.append(line)

            line = Line(points[conn_copy[number-1]], points[conn_copy[0]])
            lines.append(line)

            for i in range(0, number):
                conn_copy.pop(0)

        return lines

    def Msh2DBilinear(_pts, _elem_type, _diag_type, _np):
        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)
        msh2d.Msh2DTryBilinear(bry, _np, _elem_type, _diag_type, nno_output,
                               nel_output, coords_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel

    def Msh2DTrilinear(_pts, _elem_type, _np):
        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DTrilinear(bry, _np, _elem_type, nno_output,
                             nel_output, coords_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines,  coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel

    def Msh2DBoundContraction(_pts, _elem_type, _num_loops, _num_seg, _bc_flag):

        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)
        add_coords = aux.doublePointerWithValue(0.0, 1)
        num_seg = aux.intPointerWithValue(0, len(_num_seg))

        for i in range(0, len(_num_seg)):
            aux.setIntValue(num_seg, i, _num_seg[i])

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DBoundContraction(_num_loops, num_seg, bry, 1, 0, _bc_flag, _elem_type, add_coords,
                                    nno_output, coords_output, nel_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(num_seg)
        aux.freePointer(add_coords)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel

    def Msh2DShape(_pts, _elem_type, _num_loops, _num_seg):

        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)
        num_seg = aux.intPointerWithValue(0, len(_num_seg))

        for i in range(0, len(_num_seg)):
            aux.setIntValue(num_seg, i, _num_seg[i])

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DShape(_num_loops, num_seg, bry, _elem_type,
                         nno_output, coords_output, nel_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(num_seg)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel

    def Msh2DQuadSeam(_pts, _elem_type, _num_loops, _num_seg):

        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)
        num_seg = aux.intPointerWithValue(0, len(_num_seg))

        for i in range(0, len(_num_seg)):
            aux.setIntValue(num_seg, i, _num_seg[i])

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DQuadSeam(_num_loops, num_seg, bry, _elem_type,
                            nno_output, coords_output, nel_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(num_seg)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel

    def Msh2DTemplate(_pts, _elem_type, _num_seg, _subdv):

        bry = aux.doublePointerWithValue(0.0, len(_pts)*2)
        subdv = aux.intPointerWithValue(0, _num_seg)

        for i in range(0, len(_subdv)):
            aux.setIntValue(subdv, i, _subdv[i])

        index = 0
        for pt in _pts:
            aux.setDoubleValue(bry, index, float(pt.getX()))
            aux.setDoubleValue(bry, index + 1, float(pt.getY()))
            index += 2

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DTemplate(_num_seg, subdv, 2, _elem_type, 1,
                            bry, nno_output, coords_output, nel_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        for i in range(0, nno*2):
            item = aux.getDoubleValue(pts_pointer, i)
            coords.append(item)

        for i in range(0, nel*(_elem_type+1)):
            item = aux.getIntValue(conn_pointer, i)
            conn.append(item)

        aux.freePointer(bry)
        aux.freePointer(subdv)
        aux.freePointer(nel_output)
        aux.freePointer(nno_output)
        aux.freePointer(pts_pointer)
        aux.freePointer(conn_pointer)
        aux.freePointer(coords_output)
        aux.freePointer(conn_output)

        lines = MeshGeneration.meshLines(coords, conn)

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel
