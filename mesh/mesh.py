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
from geometry.curves.polyline import Polyline
import numpy as np
import copy
from geomdl import operations
from geomdl import NURBS
from geomdl import helpers

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
            nurbs_west = copy.deepcopy(segments[west_SegmentIndex].getNurbs())
            nurbs_south = copy.deepcopy(segments[west_SegmentIndex - 3].getNurbs())
            nurbs_east = copy.deepcopy(segments[west_SegmentIndex - 2].getNurbs())
            nurbs_north = copy.deepcopy(segments[west_SegmentIndex - 1].getNurbs())

            # Check if opposite segments have the same degree
            if nurbs_west.degree != nurbs_east.degree or nurbs_south.degree != nurbs_north.degree:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('Opposite segments must have the same degree')
                msg.exec()
                return False, None, None, None, None, None
 
            # Check if opposite segments have conforming knot vectors
            if nurbs_west.knotvector != nurbs_east.knotvector or nurbs_south.knotvector != nurbs_north.knotvector:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('Opposite segments must have conforming knotvectors')
                msg.exec()
                return False, None, None, None, None, None

            check, coonsSurf = MeshGeneration.getCoonsSurface(nurbs_north, nurbs_south, nurbs_west, nurbs_east)
            if check:
                _face.patch.nurbs = coonsSurf
                return MeshGeneration.isogeometricMesh(coonsSurf)
            else:
                return False, None, None, None, None, None


        



        elif _mesh_type == 'Isogeometric Template':

            # Check if the patch has four segments
            if len(segments) != 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 4')
                msg.exec()
                return False, None, None, None, None, None
        
            return 0





        elif _mesh_type == 'Bilinear Transfinite':

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
                poly_line = line.getEquivPolyline()
                segment_line = Segment(poly_line, line)
                lines.append(segment_line)

            line = Line(points[conn_copy[number-1]], points[conn_copy[0]])
            poly_line = line.getEquivPolyline()
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
        
    # Based on nurbspy package developed by Roberto Agromayor PhD 
    # at Norwegian University of Science and Technology (NTNU) 
    # https://github.com/RoberAgro/nurbspy
    # Adapted to work with geomdl package

    def getCoonsSurface(nurbs_north, nurbs_south, nurbs_west, nurbs_east):
        # Check the that the NURBS curves are conforming

        # Check the number of control points
        if len(nurbs_north.ctrlpts) != len(nurbs_south.ctrlpts):
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves north and south must have conforming arrays of control points")
            msg.exec()
            return False, None

        if len(nurbs_west.ctrlpts) != len(nurbs_east.ctrlpts):
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves north and south must have conforming arrays of control points")
            msg.exec()
            return False, None

        # Check the number of weights
        if len(nurbs_north.weights) != len(nurbs_south.weights):
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves north and south must have conforming arrays of weights")
            msg.exec()
            return False, None

        if len(nurbs_west.weights) != len(nurbs_east.weights):
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves west and east must have conforming arrays of weights")
            msg.exec()
            return False, None

        # Check the curve degrees
        if nurbs_north.degree != nurbs_south.degree:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves north and south must have the same degree")
            msg.exec()
            return False, None

        if nurbs_west.degree != nurbs_east.degree:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves west and east must have the same degree")
            msg.exec()
            return False, None

        # Check the knot vectors
        if nurbs_north.knotvector != nurbs_south.knotvector:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves north and south must have the same knotvector")
            msg.exec()
            return False, None

        if nurbs_west.knotvector != nurbs_east.knotvector:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("Curves west and east must have the same knotvector")
            msg.exec()
            return False, None

        # Check corner control point compatibility
        if ((nurbs_north.ctrlpts[0][0] - nurbs_west.ctrlpts[-1][0] <= Curve.COORD_TOL) and
            (nurbs_north.ctrlpts[0][1] - nurbs_west.ctrlpts[-1][1] <= Curve.COORD_TOL)):

            nurbs_north.ctrlpts[0][0] = (nurbs_north.ctrlpts[0][0] + nurbs_west.ctrlpts[-1][0]) / 2.0
            nurbs_west.ctrlpts[-1][0] = nurbs_north.ctrlpts[0][0]
            nurbs_north.ctrlpts[0][1] = (nurbs_north.ctrlpts[0][1] + nurbs_west.ctrlpts[-1][1]) / 2.0
            nurbs_west.ctrlpts[-1][1] = nurbs_north.ctrlpts[0][1]

            P_nw = np.array([nurbs_north.ctrlpts[0][0], nurbs_north.ctrlpts[0][1]])
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The north-west corner is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_south.ctrlpts[0][0] - nurbs_west.ctrlpts[0][0] <= Curve.COORD_TOL) and
            (nurbs_south.ctrlpts[0][1] - nurbs_west.ctrlpts[0][1] <= Curve.COORD_TOL)):

            nurbs_south.ctrlpts[0][0] = (nurbs_south.ctrlpts[0][0] + nurbs_west.ctrlpts[0][0]) / 2.0
            nurbs_west.ctrlpts[0][0] = nurbs_south.ctrlpts[0][0]
            nurbs_south.ctrlpts[0][1] = (nurbs_south.ctrlpts[0][1] + nurbs_west.ctrlpts[0][1]) / 2.0
            nurbs_west.ctrlpts[0][1] = nurbs_south.ctrlpts[0][1]

            P_sw = np.array([nurbs_south.ctrlpts[0][0], nurbs_south.ctrlpts[0][1]])
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-west corner is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_south.ctrlpts[-1][0] - nurbs_east.ctrlpts[0][0] <= Curve.COORD_TOL) and
            (nurbs_south.ctrlpts[-1][1] - nurbs_east.ctrlpts[0][1] <= Curve.COORD_TOL)):

            nurbs_south.ctrlpts[-1][0] = (nurbs_south.ctrlpts[-1][0] + nurbs_east.ctrlpts[0][0]) / 2.0
            nurbs_east.ctrlpts[0][0] = nurbs_south.ctrlpts[-1][0]
            nurbs_south.ctrlpts[-1][1] = (nurbs_south.ctrlpts[-1][1] + nurbs_east.ctrlpts[0][1]) / 2.0
            nurbs_east.ctrlpts[0][1] = nurbs_south.ctrlpts[-1][1]

            P_se = np.array([nurbs_south.ctrlpts[-1][0], nurbs_south.ctrlpts[-1][1]])
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-east corner is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_north.ctrlpts[-1][0] - nurbs_east.ctrlpts[-1][0] <= Curve.COORD_TOL) and
            (nurbs_north.ctrlpts[-1][1] - nurbs_east.ctrlpts[-1][1] <= Curve.COORD_TOL)):

            nurbs_north.ctrlpts[-1][0] = (nurbs_north.ctrlpts[-1][0] + nurbs_east.ctrlpts[-1][0]) / 2.0
            nurbs_east.ctrlpts[-1][0] = nurbs_north.ctrlpts[-1][0]
            nurbs_north.ctrlpts[-1][1] = (nurbs_north.ctrlpts[-1][1] + nurbs_east.ctrlpts[-1][1]) / 2.0
            nurbs_east.ctrlpts[-1][1] = nurbs_north.ctrlpts[-1][1]

            P_ne = np.array([nurbs_north.ctrlpts[-1][0], nurbs_north.ctrlpts[-1][1]])
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-east corner is not compatible")
            msg.exec()
            return False, None

        # Check corner weight compatibility
        if ((nurbs_north.weights[0] - nurbs_west.weights[-1] <= Curve.PARAM_TOL) and
            (nurbs_north.weights[0] - nurbs_west.weights[-1] <= Curve.PARAM_TOL)):

            nurbs_north.weights[0] = (nurbs_north.weights[0] + nurbs_west.weights[-1]) / 2.0
            nurbs_west.weights[-1] = nurbs_north.weights[0]

            W_nw = np.array(nurbs_north.weights)[0]
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The north-west weight is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_south.weights[0] - nurbs_west.weights[0] <= Curve.PARAM_TOL) and
            (nurbs_south.weights[0] - nurbs_west.weights[0] <= Curve.PARAM_TOL)):

            nurbs_south.weights[0] = (nurbs_south.weights[0] + nurbs_west.weights[0]) / 2.0
            nurbs_west.weights[0] = nurbs_south.weights[0]

            W_sw = np.array(nurbs_south.weights)[0]
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-west weight is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_south.weights[-1] - nurbs_east.weights[0] <= Curve.PARAM_TOL) and
            (nurbs_south.weights[-1] - nurbs_east.weights[0] <= Curve.PARAM_TOL)):

            nurbs_south.weights[-1] = (nurbs_south.weights[-1] + nurbs_east.weights[0]) / 2.0
            nurbs_east.weights[0] = nurbs_south.weights[-1]

            W_se = np.array(nurbs_south.weights)[-1]
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-east weight is not compatible")
            msg.exec()
            return False, None

        if ((nurbs_north.weights[-1] - nurbs_east.weights[-1] <= Curve.PARAM_TOL) and
            (nurbs_north.weights[-1] - nurbs_east.weights[-1] <= Curve.PARAM_TOL)):

            nurbs_north.weights[-1] = (nurbs_north.weights[-1] + nurbs_east.weights[-1]) / 2.0
            nurbs_east.weights[-1] = nurbs_north.weights[-1]

            W_ne = np.array(nurbs_north.weights)[-1]
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle("Warning")
            msg.setText("The sourth-east weight is not compatible")
            msg.exec()
            return False, None

        # Make the Coons surface NURBS representation

        # Size of the array of control points (use broadcasting to get the right shapes)
        Nu = len(nurbs_south.ctrlpts)
        Nv = len(nurbs_west.ctrlpts)

        # Curves control points
        P_north = np.transpose(np.array(nurbs_north.ctrlpts))
        P_south = np.transpose(np.array(nurbs_south.ctrlpts))
        P_west = np.transpose(np.array(nurbs_west.ctrlpts))
        P_east = np.transpose(np.array(nurbs_east.ctrlpts))

        # Curves weights
        W_north = np.array(nurbs_north.weights)
        W_ne = W_north[-1]
        W_south = np.array(nurbs_south.weights)
        W_west = np.array(nurbs_west.weights)
        W_east = np.array(nurbs_east.weights)

        # Map the boundary control points to homogeneous space and set the right number of dimensions for broadcasting
        Pw_north = np.concatenate((P_north*W_north[np.newaxis, :], W_north[np.newaxis, :]), axis=0)[:, :, np.newaxis]
        Pw_south = np.concatenate((P_south*W_south[np.newaxis, :], W_south[np.newaxis, :]), axis=0)[:, :, np.newaxis]
        Pw_west  = np.concatenate((P_west *W_west [np.newaxis, :], W_west [np.newaxis, :]), axis=0)[:, np.newaxis, :]
        Pw_east  = np.concatenate((P_east *W_east [np.newaxis, :], W_east [np.newaxis, :]), axis=0)[:, np.newaxis, :]

        # Map the corner control points to homogeneous space and set the right number of dimensions for broadcasting
        Pw_sw = np.concatenate((P_sw*W_sw[np.newaxis], W_sw[np.newaxis]), axis=0)[:, np.newaxis, np.newaxis]
        Pw_se = np.concatenate((P_se*W_se[np.newaxis], W_se[np.newaxis]), axis=0)[:, np.newaxis, np.newaxis]
        Pw_ne = np.concatenate((P_ne*W_ne[np.newaxis], W_ne[np.newaxis]), axis=0)[:, np.newaxis, np.newaxis]
        Pw_nw = np.concatenate((P_nw*W_nw[np.newaxis], W_nw[np.newaxis]), axis=0)[:, np.newaxis, np.newaxis]

        # Compute the array of control points by transfinite interpolation
        u = np.linspace(0, 1, Nu)[np.newaxis, :, np.newaxis]
        v = np.linspace(0, 1, Nv)[np.newaxis, np.newaxis, :]
        term_1a = (1 - v) * Pw_south + v * Pw_north
        term_1b = (1 - u) * Pw_west + u * Pw_east
        term_2 = (1 - u) * (1 - v) * Pw_sw + u * v * Pw_ne + (1 - u) * v * Pw_nw + u * (1 - v) * Pw_se
        Pw = term_1a + term_1b - term_2

        # Compute the array of control points in ordinary space and the array of control point weights (inverse map)
        ctrlPts = np.transpose(Pw[0:-1, :, :]/Pw[[-1], :, :])
        ctrlPts = np.reshape(ctrlPts, (Nu*Nv,2), order='F').tolist()
        weights = np.transpose(Pw[-1, :, :])
        weights = np.reshape(weights, (Nu*Nv), order='F').tolist()

        # Define the order of the basis polynomials
        degreeU = nurbs_south.degree
        degreeV = nurbs_west.degree

        # Definite the knot vectors
        knotvectorU = nurbs_south.knotvector
        knotvectorV = nurbs_west.knotvector

        # Create the NURBS surface
        coonsSurf = NURBS.Surface()
        coonsSurf.degree_u = degreeU
        coonsSurf.degree_v = degreeV
        coonsSurf.ctrlpts_size_u = Nu
        coonsSurf.ctrlpts_size_v = Nv
        coonsSurf.ctrlpts = ctrlPts
        coonsSurf.weights = weights
        coonsSurf.knotvector_u = knotvectorU
        coonsSurf.knotvector_v = knotvectorV
        coonsSurf.sample_size = 10
        return True, coonsSurf
    
    def isogeometricMesh(coonsSurf):
        MeshCurves = []
        for i in set(coonsSurf.knotvector_u):
            if i == 0.0 or i == 1.0:
                pass
            else:
                isoCurveNurbs = MeshGeneration.getIsocurveU(coonsSurf, i)
                isoCurve = GenericNurbs(isoCurveNurbs)
                isoCurvePoly = isoCurve.getEquivPolyline(0.01)
                isoCurveSeg = Segment(isoCurvePoly, isoCurve)
                MeshCurves.append(isoCurveSeg)

        for j in set(coonsSurf.knotvector_v):
            if j == 0.0 or j == 1.0:
                pass
            else:
                isoCurveNurbs = MeshGeneration.getIsocurveV(coonsSurf, j)
                isoCurve = GenericNurbs(isoCurveNurbs)
                isoCurvePoly = isoCurve.getEquivPolyline(0.01)
                isoCurveSeg = Segment(isoCurvePoly, isoCurve)
                MeshCurves.append(isoCurveSeg)

        nel = (len(set(coonsSurf.knotvector_u)) - 1) * (len(set(coonsSurf.knotvector_v)) - 1)
        nno = coonsSurf.ctrlpts_size_u * coonsSurf.ctrlpts_size_v
        return True, MeshCurves, [], [], nno, nel

    def getIsocurveU(coonsSurf, u0):
        # Surface properties
        degreeU = coonsSurf.degree_u
        degreeV = coonsSurf.degree_v
        Nu = coonsSurf.ctrlpts_size_u
        Nv = coonsSurf.ctrlpts_size_v
        knotvectorU = coonsSurf.knotvector_u
        knotvectorV = coonsSurf.knotvector_v
        ctrlNet = np.transpose(coonsSurf.ctrlpts)
        ctrlNet = np.reshape(ctrlNet, (2,Nu,Nv), order='C')
        SurfWeights = np.transpose(coonsSurf.weights)
        SurfWeights = np.reshape(SurfWeights, (Nu,Nv), order='C')

        # Map the control points to homogeneous space | P_w = (x*w,y*w,z*w,w)
        ctrlNet_W = np.concatenate((ctrlNet * SurfWeights[np.newaxis, :], SurfWeights[np.newaxis, :]), axis=0)

        # Compute the array of control points in homogeneous space
        N_basis_u = MeshGeneration.compute_basis_polynomials(Nu - 1, degreeU, knotvectorU, float(u0)).flatten()   # use float() to avoid problem with numba and integers
        N_basis_u = N_basis_u[np.newaxis, :, np.newaxis]
        ctrlPts_W = np.sum(ctrlNet_W * N_basis_u, axis=1)

        # Compute the array of control points in ordinary space and the array of control point weights (inverse map)
        ctrlPts = np.transpose(ctrlPts_W[0:-1, :]/ctrlPts_W[-1, :]).tolist()
        weights = ctrlPts_W[-1, :].tolist()

        # Create the NURBS isoparametric curve in the u direction
        isocurveUNurbs = NURBS.Curve()
        isocurveUNurbs.degree = degreeV
        isocurveUNurbs.ctrlpts = ctrlPts
        isocurveUNurbs.weights = weights
        isocurveUNurbs.knotvector = knotvectorV
        isocurveUNurbs.sample_size = 10
        return isocurveUNurbs
    
    def getIsocurveV(coonsSurf, v0):
        # Surface properties
        degreeU = coonsSurf.degree_u
        degreeV = coonsSurf.degree_v
        Nu = coonsSurf.ctrlpts_size_u
        Nv = coonsSurf.ctrlpts_size_v
        knotvectorU = coonsSurf.knotvector_u
        knotvectorV = coonsSurf.knotvector_v
        ctrlNet = np.transpose(coonsSurf.ctrlpts)
        ctrlNet = np.reshape(ctrlNet, (2,Nu,Nv), order='C')
        SurfWeights = np.transpose(coonsSurf.weights)
        SurfWeights = np.reshape(SurfWeights, (Nu,Nv), order='C')

        # Map the control points to homogeneous space | P_w = (x*w,y*w,z*w,w)
        ctrlNet_W = np.concatenate((ctrlNet * SurfWeights[np.newaxis, :], SurfWeights[np.newaxis, :]), axis=0)

        # Compute the array of control points in homogeneous space
        N_basis_v = MeshGeneration.compute_basis_polynomials(Nv - 1, degreeV, knotvectorV, float(v0)).flatten()   # use float() to avoid problem with numba and integers
        N_basis_v = N_basis_v[np.newaxis, np.newaxis, :]
        ctrlPts_W = np.sum(ctrlNet_W * N_basis_v, axis=2)

        # Compute the array of control points in ordinary space and the array of control point weights (inverse map)
        ctrlPts = np.transpose(ctrlPts_W[0:-1, :]/ctrlPts_W[-1, :]).tolist()
        weights = ctrlPts_W[-1, :].tolist()

        # Create the NURBS isoparametric curve in the v direction
        isocurveUNurbs = NURBS.Curve()
        isocurveUNurbs.degree = degreeU
        isocurveUNurbs.ctrlpts = ctrlPts
        isocurveUNurbs.weights = weights
        isocurveUNurbs.knotvector = knotvectorU
        isocurveUNurbs.sample_size = 10
        return isocurveUNurbs

    def compute_basis_polynomials(n, p, U, u, return_degree=None):

        # Evaluate the n-th B-Spline basis polynomials of degree ´p´ for the input u-parametrization
        # The basis polynomials are computed from their definition by implementing equation 2.5 directly
        # Parameters
        # ----------
        # n : integer
        #     Highest index of the basis polynomials (n+1 basis polynomials)
        # p : integer
        #     Degree of the basis polynomials
        # U : ndarray with shape (r+1=n+p+2,)
        #     Knot vector of the basis polynomials
        #     Set the multiplicity of the first and last entries equal to ´p+1´ to obtain a clamped spline
        # u : scalar or ndarray with shape (Nu,)
        #     Parameter used to evaluate the basis polynomials (real or complex!)
        # return_degree : int
        #     Degree of the returned basis polynomials
        # Returns
        # -------
        # N : ndarray with shape (n+1, Nu)
        #     Array containing the basis polynomials of order ´p´ evaluated at ´u´
        #     The first dimension of ´N´ spans the n-th polynomials
        #     The second dimension of ´N´ spans the ´u´ parametrization sample points

        # # Check the degree of the basis basis polynomials (not possible to compile with Numba yet)
        # if p < 0: raise Exception('The degree of the basis polynomials cannot be negative')
        #
        # # Check the number of basis basis polynomials (not possible to compile with Numba yet)
        # if p > n: raise Exception('The degree of the basis polynomials must be equal or lower than the number of basis polynomials')

        # Number of points where the polynomials are evaluated (vectorized computations)
        u = np.asarray(u * 1.0)     # Convert to array of floats
        Nu = u.size

        # Number of basis polynomials at the current step of the recursion
        m = n + p + 1

        # Initialize the array of basis polynomials
        N = np.zeros((p + 1, m, Nu), dtype=u.dtype)

        # First step of the recursion formula (p = 0)
        # The case when point_index==n and u==1 is an special case. See the NURBS book section 2.5 and algorithm A2.1
        # The np.real() operator is used such that the function extends to complex u-parameter as well
        for i in range(m):
            # N[0, i, :] = 0.0 + 1.0 * (u >= U[i]) * (u < U[i + 1])
            # N[0, i, :] = 0.0 + 1.0 * (u >= U[i]) * (u < U[i + 1]) + 1.00 * (np.logical_and(u == 1, i == n))
            N[0, i, :] = 0.0 + 1.0 * (np.real(u) >= U[i]) * (np.real(u) < U[i + 1]) + 1.00 * (np.logical_and(np.real(u) == U[-1], i == n))

        # Second and next steps of the recursion formula (p = 1, 2, ...)
        for k in range(1, p + 1):

            # Update the number of basis polynomials
            m = m - 1

            # Compute the basis polynomials using the de Boor recursion formula
            for i in range(m):

                # Compute first factor (avoid division by zero by convention)
                if (U[i + k] - U[i]) == 0:
                    n1 = np.zeros((Nu,), dtype=u.dtype)
                else:
                    n1 = (u - U[i]) / (U[i + k] - U[i]) * N[k - 1, i, :]

                # Compute second factor (avoid division by zero by convention)
                if (U[i + k + 1] - U[i + 1]) == 0:
                    n2 = np.zeros((Nu,), dtype=u.dtype)
                else:
                    n2 = (U[i + k + 1] - u) / (U[i + k + 1] - U[i + 1]) * N[k - 1, i + 1, :]

                # Compute basis polynomial (recursion formula 2.5)
                N[k, i, ...] = n1 + n2

        # Get the n+1 basis polynomials of the desired degree
        N = N[p, 0:n+1, :] if return_degree is None else N[return_degree, 0:n+1, :]

        # # Numba assertions
        # assert p >= 0    # The degree of the basis polynomials cannot be negative
        # assert p <= n    # The degree of the basis polynomials must be equal or lower than the number of basis polynomials

        return N