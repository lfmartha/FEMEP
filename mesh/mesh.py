# from compgeom.compgeom import CompGeom
from PyQt5.QtWidgets import QMessageBox
from mesh.mesh1d import Mesh1D
import mesh.mesh2d.msh2d as msh2d
from he.hemodel import HeModel
from geometry.curves.curve import Curve
import mesh.auxmodule.auxmodule as aux
from geometry.curves.line import Line
from geometry.curves.genericnurbs import GenericNurbs
from geometry.segment import Segment
from geometry.point import Point
from compgeom.pnt2d import Pnt2D
import numpy as np
import nurbspy as nrb
from geomdl import operations
from geomdl import NURBS


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

        if _mesh_type == 'Isogeometric':

            # Check if the patch has four segments
            if len(segments) != 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 4')
                msg.exec()
                return False, None, None, None, None, None

            # # Find west segment
            # west_SegmentIndex = 0
            # xInit_seg_W = segments[0].getXinit()
            # xEnd_seg_W = segments[0].getXend()
            # for i in range(1,4):
            #     xInit_seg_i = segments[i].getXinit()
            #     xEnd_seg_i = segments[i].getXend()

            #     # Consider tolerance
            #     if xInit_seg_i >= xInit_seg_W - Curve.COORD_TOL and xInit_seg_i <= xInit_seg_W + Curve.COORD_TOL:
            #         xInit_seg_i = xInit_seg_W
            #     if xEnd_seg_i >= xEnd_seg_W - Curve.COORD_TOL and xEnd_seg_i <= xEnd_seg_W + Curve.COORD_TOL:
            #         xEnd_seg_i = xEnd_seg_W

            #     # Check if index i corresponds to the west segment
            #     if xInit_seg_i <= xInit_seg_W and xEnd_seg_i <= xEnd_seg_W:
            #         west_SegmentIndex = i
            #         xInit_seg_W = xInit_seg_i
            #         xEnd_seg_W = xEnd_seg_i

            # Find west segment
            west_SegmentIndex = 0
            cornersPtsX = [segments[0].getXinit(), segments[0].getXend(), segments[2].getXinit(), segments[2].getXend()]
            cornersPtsX.remove(max(cornersPtsX))
            cornersPtsX.remove(max(cornersPtsX))
            
            for i in range(4):
                xInit_seg_i = segments[i].getXinit()
                xEnd_seg_i = segments[i].getXend()

                # Check if index i corresponds to the west segment
                if ((xInit_seg_i >= cornersPtsX[0] - Curve.COORD_TOL and xInit_seg_i <= cornersPtsX[0] + Curve.COORD_TOL) or 
                    (xInit_seg_i >= cornersPtsX[1] - Curve.COORD_TOL and xInit_seg_i <= cornersPtsX[1] + Curve.COORD_TOL)):

                    if ((xEnd_seg_i >= cornersPtsX[0] - Curve.COORD_TOL and xEnd_seg_i <= cornersPtsX[0] + Curve.COORD_TOL) or 
                        (xEnd_seg_i >= cornersPtsX[1] - Curve.COORD_TOL and xEnd_seg_i <= cornersPtsX[1] + Curve.COORD_TOL)):

                        west_SegmentIndex = i

            # Get Nurbs
            nurbs_west_geomdl = segments[west_SegmentIndex].getNurbs()
            nurbs_south_geomdl = segments[west_SegmentIndex - 3].getNurbs()
            nurbs_east_geomdl = segments[west_SegmentIndex - 2].getNurbs()
            nurbs_north_geomdl = segments[west_SegmentIndex - 1].getNurbs()

            # Inverse nurbs
            # vecW = []
            # vecIndexW = []
            # if nurbs_west_geomdl.ctrlpts[0][1] >  nurbs_west_geomdl.ctrlpts[-1][1]:
            #     for i in range(len(nurbs_west_geomdl.knotvector)):
            #         if nurbs_west_geomdl.knotvector[i] != 1.0 and nurbs_west_geomdl.knotvector[i] != 0.0:
            #             vecW.append(1.0 - nurbs_west_geomdl.knotvector[i])
            #             vecIndexW.append(i)
            #     vecW.reverse()
            #     vecIndexW.reverse()
            #     for j in vecIndexW:
            #         del nurbs_west_geomdl.knotvector[j]
            #     index = min(vecIndexW)
            #     nurbs_west_geomdl.knotvector[index:index] = vecW
            #     nurbs_west_geomdl.ctrlpts.reverse()
            #     nurbs_west_geomdl.weights.reverse()

            knotvector_west = list(nurbs_west_geomdl.knotvector)
            if nurbs_west_geomdl.ctrlpts[0][1] >  nurbs_west_geomdl.ctrlpts[-1][1]:
                for i in range(len(knotvector_west)):
                    if knotvector_west[i] != 1.0 and knotvector_west[i] != 0.0:
                        nurbs_west_geomdl.knotvector[len(knotvector_west) - 1 - i] = 1.0 - knotvector_west[i]
                nurbs_west_geomdl.ctrlpts.reverse()
                nurbs_west_geomdl.weights.reverse()

            knotvector_south = list(nurbs_south_geomdl.knotvector)
            if nurbs_south_geomdl.ctrlpts[0][0] >  nurbs_south_geomdl.ctrlpts[-1][0]:
                for i in range(len(knotvector_south)):
                    if knotvector_south[i] != 1.0 and knotvector_south[i] != 0.0:
                        nurbs_south_geomdl.knotvector[len(knotvector_south) - 1 - i] = 1.0 - knotvector_south[i]
                nurbs_south_geomdl.ctrlpts.reverse()
                nurbs_south_geomdl.weights.reverse()

            knotvector_east = list(nurbs_east_geomdl.knotvector)
            if nurbs_east_geomdl.ctrlpts[0][1] >  nurbs_east_geomdl.ctrlpts[-1][1]:
                for i in range(len(knotvector_east)):
                    if knotvector_east[i] != 1.0 and knotvector_east[i] != 0.0:
                        nurbs_east_geomdl.knotvector[len(knotvector_east) - 1 - i] = 1.0 - knotvector_east[i]
                nurbs_east_geomdl.ctrlpts.reverse()
                nurbs_east_geomdl.weights.reverse()

            knotvector_north = list(nurbs_north_geomdl.knotvector)
            if nurbs_north_geomdl.ctrlpts[0][0] >  nurbs_north_geomdl.ctrlpts[-1][0]:
                for i in range(len(knotvector_north)):
                    if knotvector_north[i] != 1.0 and knotvector_north[i] != 0.0:
                        nurbs_north_geomdl.knotvector[len(knotvector_north) - 1 - i] = 1.0 - knotvector_north[i]
                nurbs_north_geomdl.ctrlpts.reverse()
                nurbs_north_geomdl.weights.reverse()

            # Check if opposite segments have the same degree
            if nurbs_west_geomdl.degree != nurbs_east_geomdl.degree or nurbs_south_geomdl.degree != nurbs_north_geomdl.degree:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('Opposite segments must have the same degree')
                msg.exec()
                return False, None, None, None, None, None

            # # Check if opposite segments have the same number of control points
            # if len(nurbs_west_geomdl.ctrlpts) != len(nurbs_east_geomdl.ctrlpts) or len(nurbs_south_geomdl.ctrlpts) != len(nurbs_north_geomdl.ctrlpts):
            #     msg = QMessageBox(MeshGeneration.App)
            #     msg.setWindowTitle('Warning')
            #     msg.setText('Opposite segments must have the same number of control points')
            #     msg.exec()
            #     return False, None, None, None, None, None

            # Insert remaining knots
            nurbs_west_knots = nurbs_west_geomdl.knotvector
            nurbs_west_knots = list(set(nurbs_west_knots)) # Remove duplicates
            nurbs_west_knots.sort()
            nurbs_west_knots.pop()
            nurbs_west_knots.pop(0)

            nurbs_south_knots = nurbs_south_geomdl.knotvector
            nurbs_south_knots = list(set(nurbs_south_knots)) # Remove duplicates
            nurbs_south_knots.sort()
            nurbs_south_knots.pop()
            nurbs_south_knots.pop(0)

            nurbs_east_knots = nurbs_east_geomdl.knotvector
            nurbs_east_knots = list(set(nurbs_east_knots)) # Remove duplicates
            nurbs_east_knots.sort()
            nurbs_east_knots.pop()
            nurbs_east_knots.pop(0)

            nurbs_north_knots = nurbs_north_geomdl.knotvector
            nurbs_north_knots = list(set(nurbs_north_knots)) # Remove duplicates
            nurbs_north_knots.sort()
            nurbs_north_knots.pop()
            nurbs_north_knots.pop(0)

            west_not_east = set(nurbs_west_knots) - set(nurbs_east_knots)
            east_not_west = set(nurbs_east_knots) - set(nurbs_west_knots)
            north_not_south = set(nurbs_north_knots) - set(nurbs_south_knots)
            south_not_north = set(nurbs_south_knots) - set(nurbs_north_knots)

            for knot in west_not_east:
                operations.insert_knot(nurbs_east_geomdl, [knot], [1])
            
            for knot in east_not_west:
                operations.insert_knot(nurbs_west_geomdl, [knot], [1])

            for knot in north_not_south:
                operations.insert_knot(nurbs_south_geomdl, [knot], [1])

            for knot in south_not_north:
                operations.insert_knot(nurbs_north_geomdl, [knot], [1])

            # Generate coons surface
            nurbs_west_nurbspy = MeshGeneration.geomdlToNurbsPy(nurbs_west_geomdl)
            nurbs_south_nurbspy = MeshGeneration.geomdlToNurbsPy(nurbs_south_geomdl)
            nurbs_east_nurbspy = MeshGeneration.geomdlToNurbsPy(nurbs_east_geomdl)
            nurbs_north_nurbspy = MeshGeneration.geomdlToNurbsPy(nurbs_north_geomdl)

            # Force corner control points to be equal
            nurbs_south_nurbspy.P[:, 0] = nurbs_west_nurbspy.P[:, 0]
            nurbs_south_nurbspy.P[:, -1] = nurbs_east_nurbspy.P[:, 0]
            nurbs_north_nurbspy.P[:, -1] = nurbs_east_nurbspy.P[:, -1]
            nurbs_north_nurbspy.P[:, 0] = nurbs_west_nurbspy.P[:, -1]
            coonsNurbsSurface = nrb.NurbsSurfaceCoons(nurbs_south_nurbspy, nurbs_north_nurbspy, nurbs_west_nurbspy, nurbs_east_nurbspy).NurbsSurface

            return MeshGeneration.isogeometricMesh(coonsNurbsSurface)

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
        pts = Mesh1D.subdivideSegment(_seg, number, ratio, quad)
        pts.insert(0, _seg.evalPoint(0))
        pts.append(_seg.evalPoint(1))

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
                poly_line = line.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
                segment_line = Segment(poly_line, line)
                lines.append(segment_line)

            line = Line(points[conn_copy[number-1]], points[conn_copy[0]])
            poly_line = line.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
            segment_line = Segment(poly_line, line)
            lines.append(segment_line)

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

    def geomdlToNurbsPy(nurbs_geomdl):
        nurbs_ctrlpts = np.transpose(np.array(nurbs_geomdl.ctrlpts))
        nurbs_degree = nurbs_geomdl.degree
        nurbs_knotvector = np.array(nurbs_geomdl.knotvector)
        nurbs_weights = np.array(nurbs_geomdl.weights)
        nurbs_nurbspy = nrb.NurbsCurve(control_points=nurbs_ctrlpts, degree=nurbs_degree, knots=nurbs_knotvector, weights = nurbs_weights)
        return nurbs_nurbspy

    def nurbsPyToGeomdl(nurbs_nurbspy):
        nurbs_geomdl = NURBS.Curve()
        nurbs_geomdl.degree = nurbs_nurbspy.p
        nurbs_geomdl.ctrlpts = np.transpose(nurbs_nurbspy.P).tolist()
        nurbs_geomdl.knotvector = nurbs_nurbspy.U.tolist()
        nurbs_geomdl.sample_size = 10
        return nurbs_geomdl

    def isogeometricMesh(coonsNurbsSurface):
        nurbs_west = coonsNurbsSurface.get_isocurve_u(u0 = 0.0)
        nurbs_west = MeshGeneration.nurbsPyToGeomdl(nurbs_west)
        nurbs_south = coonsNurbsSurface.get_isocurve_v(v0 = 0.0)
        nurbs_south = MeshGeneration.nurbsPyToGeomdl(nurbs_south)
        nurbs_east = coonsNurbsSurface.get_isocurve_u(u0 = 1.0)
        nurbs_east = MeshGeneration.nurbsPyToGeomdl(nurbs_east)
        nurbs_north = coonsNurbsSurface.get_isocurve_v(v0 = 1.0)
        nurbs_north = MeshGeneration.nurbsPyToGeomdl(nurbs_north)

        nurbs_west_knots = nurbs_west.knotvector
        nurbs_west_knots = list(set(nurbs_west_knots)) # Remove duplicates
        nurbs_west_knots.sort()

        nurbs_south_knots = nurbs_south.knotvector
        nurbs_south_knots = list(set(nurbs_south_knots)) # Remove duplicates
        nurbs_south_knots.sort()

        nel = (len(nurbs_west_knots) - 1) * (len(nurbs_south_knots) - 1)

        MeshCurves = []
        for i in range(len(nurbs_west_knots) - 1, 0, -1):
        # for i in range(len(nurbs_west_knots) - 1):
            #i = len(nurbs_west_knots) - i
            for j in range(len(nurbs_south_knots) - 1):
                nurbs_west = MeshGeneration.nurbsPyToGeomdl(coonsNurbsSurface.get_isocurve_u(u0 = (nurbs_south_knots[j])))
                nurbs_south = MeshGeneration.nurbsPyToGeomdl(coonsNurbsSurface.get_isocurve_v(v0 = (nurbs_west_knots[i - 1])))
                nurbs_east = MeshGeneration.nurbsPyToGeomdl(coonsNurbsSurface.get_isocurve_u(u0 = (nurbs_south_knots[j + 1])))
                nurbs_north = MeshGeneration.nurbsPyToGeomdl(coonsNurbsSurface.get_isocurve_v(v0 = (nurbs_west_knots[i])))

                curve_west = GenericNurbs(nurbs_west)
                curve_south = GenericNurbs(nurbs_south)
                curve_east = GenericNurbs(nurbs_east)
                curve_north = GenericNurbs(nurbs_north)

                poly_west = curve_west.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
                segment_west = Segment(poly_west, curve_west)
                poly_south = curve_south.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
                segment_south = Segment(poly_south, curve_south)
                poly_east = curve_east.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
                segment_east = Segment(poly_east, curve_east)
                poly_north = curve_north.getEquivPolyline(0.0, 1.0, Curve.COORD_TOL)
                segment_north = Segment(poly_north, curve_north)

                # Get splited segments
                selv = None
                status, pt_west_north, param_west, param_north = HeModel.intersectSegments(selv, segment_west, segment_north, Curve.COORD_TOL)

                segments_west = segment_west.split(param_west, pt_west_north)
                segment_west = segments_west[0]

                segments_north = segment_north.split(param_north, pt_west_north)
                if len(segments_north) > 1:
                    segment_north = segments_north[1]
                else:
                    segment_north = segments_north[0]

                status, pt_west_south, param_west, param_south = HeModel.intersectSegments(selv, segment_west, segment_south, Curve.COORD_TOL)

                segments_west = segment_west.split(param_west, pt_west_south)
                if len(segments_west) > 1:
                    segment_west = segments_west[1]
                else:
                    segment_west = segments_west[0]

                segments_south = segment_south.split(param_south, pt_west_south)
                if len(segments_south) > 1:
                    segment_south = segments_south[1]
                else:
                    segment_south = segments_south[0]

                status, pt_south_east, param_south, param_east = HeModel.intersectSegments(selv, segment_south, segment_east, Curve.COORD_TOL)

                segments_south = segment_south.split(param_south, pt_south_east)
                segment_south = segments_south[0]

                segments_east = segment_east.split(param_east, pt_south_east)
                if len(segments_east) > 1:
                    segment_east = segments_east[1]
                else:
                    segment_east = segments_east[0]

                status, pt_east_north, param_east, param_north = HeModel.intersectSegments(selv, segment_east, segment_north, Curve.COORD_TOL)

                segments_east = segment_east.split(param_east, pt_east_north)
                segment_east = segments_east[0]

                segments_north = segment_north.split(param_north, pt_east_north)
                segment_north = segments_north[0]

                knotvector_W = segment_west.curve.nurbs.knotvector
                for x in range(len(knotvector_W)):
                    if knotvector_W[x] != 1.0 and knotvector_W[x] != 0.0:
                        knotvector_W[x] = 1.0 - knotvector_W[x]

                ctrlpts_W = segment_west.curve.nurbs.ctrlpts
                ctrlpts_W.reverse()

                weights_W = segment_west.curve.nurbs.weights
                weights_W.reverse()

                EqPoly_W = segment_west.curve.eqPoly
                EqPoly_W.reverse()

                segment_west.curve.pt0, segment_west.curve.pt1 = segment_west.curve.pt1, segment_west.curve.pt0

                knotvector_N = segment_north.curve.nurbs.knotvector
                for y in range(len(knotvector_N)):
                    if knotvector_N[y] != 1.0 and knotvector_N[y] != 0.0:
                        knotvector_N[y] = 1.0 - knotvector_N[y]

                ctrlpts_N = segment_north.curve.nurbs.ctrlpts
                ctrlpts_N.reverse()

                weights_N = segment_north.curve.nurbs.weights
                weights_N.reverse()

                EqPoly_N = segment_north.curve.eqPoly
                EqPoly_N.reverse()

                segment_north.curve.pt0, segment_north.curve.pt1 = segment_north.curve.pt1, segment_north.curve.pt0

                segment_south.curve.pt0 = segment_west.curve.pt1
                segment_south.curve.pt1 = segment_east.curve.pt0
                segment_north.curve.pt0 = segment_east.curve.pt1
                segment_north.curve.pt1 = segment_west.curve.pt0
                
                MeshCurves.extend([segment_west, segment_south, segment_east, segment_north])
        
        return True, MeshCurves, [], [], 0.0, nel