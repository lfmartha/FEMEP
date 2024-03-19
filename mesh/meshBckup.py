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
from geometry.curves.curve import Curve
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
                return False, None, None, None, None, None, None
            
            # Check for inner loops
            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None, None

            # Get curves Nurbs
            for i in range(4):
                west_SegmentIndex = i
                try:
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
                        return False, None, None, None, None, None, None
        
                    # Check if opposite segments have conforming knot vectors
                    if nurbs_west.knotvector != nurbs_east.knotvector or nurbs_south.knotvector != nurbs_north.knotvector:
                        msg = QMessageBox(MeshGeneration.App)
                        msg.setWindowTitle('Warning')
                        msg.setText('Opposite segments must have conforming knotvectors')
                        msg.exec()
                        return False, None, None, None, None, None, None

                    check, coonsSurf = MeshGeneration.getCoonsSurface(nurbs_north, nurbs_south, nurbs_west, nurbs_east)
                    if check:
                        _face.patch.nurbs = coonsSurf
                        return MeshGeneration.isogeometricMesh(coonsSurf)
                except:
                    pass

            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('Check for corner compatibility')
            msg.exec()
            return False, None, None, None, None, None, None




        elif _mesh_type == 'Isogeometric Template':
            # Check if the patch has four segments
            if len(segments) != 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 4')
                msg.exec()
                return False, None, None, None, None, None, None
            
            # Check for inner loops
            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None, None
            
            segmentOrientsCopy = segmentOrients.copy()

            # For Template 
            if segments[0].curve.nurbs.knotvector == segments[2].curve.nurbs.knotvector:
                opposites = [segments[0], segments[2]]
                if len(segments[1].curve.nurbs.knotvector) < len(segments[3].curve.nurbs.knotvector):
                    lessSdv = segments[1]
                    moreSdv = segments[3]
                else:
                    lessSdv = segments[3]
                    moreSdv = segments[1]
            
            elif segments[1].curve.nurbs.knotvector == segments[3].curve.nurbs.knotvector:
                opposites = [segments[1], segments[3]]
                if len(segments[0].curve.nurbs.knotvector) < len(segments[2].curve.nurbs.knotvector):
                    lessSdv = segments[0]
                    moreSdv = segments[2]
                else:
                    lessSdv = segments[2]
                    moreSdv = segments[0]

            corner1 = Pnt2D(lessSdv.curve.nurbs.ctrlpts[0][0], lessSdv.curve.nurbs.ctrlpts[0][1])
            corner2 = Pnt2D(lessSdv.curve.nurbs.ctrlpts[-1][0], lessSdv.curve.nurbs.ctrlpts[-1][1])
            
            polygon = []
            polygon_weights = []
            subv = []

            additionalPts = []

            for i in range(0, len(segments)):
                ctrlPts = segments[i].curve.nurbs.ctrlpts
                weights = segments[i].curve.nurbs.weights

                if segments[i] == moreSdv:
                    subv.append(len(ctrlPts) - 1)
                elif segments[i] == lessSdv:
                    subv.append(len(ctrlPts) - 3)
                elif segments[i] == opposites[0] or segments[i] == opposites[1]:
                    subv.append(len(ctrlPts) - 2)

                if segments[i].isReversed:
                    if segmentOrientsCopy[i] == True:
                        segmentOrientsCopy[i] = False
                    else:
                        segmentOrientsCopy[i] == True

                polygonSeg = []
                polygon_weightsSeg = []

                if segmentOrients[i]:
                    for j in range(0, len(ctrlPts)-1):
                        polygonSeg.append(ctrlPts[j])
                        polygon_weightsSeg.append(weights[j])
                else:
                    for j in range(len(ctrlPts)-1, 0, -1):
                        polygonSeg.append(ctrlPts[j])
                        polygon_weightsSeg.append(weights[j])

                if segments[i] == moreSdv:
                    pass
                elif segments[i] == lessSdv:
                    additionalPt_dict = {"Pt": Pnt2D(ctrlPts[1][0], ctrlPts[1][1]),
                                         "PtWeight": weights[1],
                                         "adjacentCorner": Pnt2D(ctrlPts[0][0], ctrlPts[0][1]),
                                         "adjacentPt": Pnt2D(ctrlPts[2][0], ctrlPts[2][1])}
                    additionalPts.append(additionalPt_dict)
                    additionalPt_dict = {"Pt": Pnt2D(ctrlPts[-2][0], ctrlPts[-2][1]),
                                         "PtWeight": weights[-2],
                                         "adjacentCorner": Pnt2D(ctrlPts[-1][0], ctrlPts[-1][1]),
                                         "adjacentPt": Pnt2D(ctrlPts[-3][0], ctrlPts[-3][1])}
                    additionalPts.append(additionalPt_dict)
                    polygonSeg.pop(1)
                    polygonSeg.pop(-1)
                    polygon_weightsSeg.pop(1)
                    polygon_weightsSeg.pop(-1)
                elif segments[i] == opposites[0] or segments[i] == opposites[1]:
                    firstCtrlPt = Pnt2D(polygonSeg[0][0], polygonSeg[0][1])
                    tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)
                    if Pnt2D.equal(firstCtrlPt, corner1, tol) or Pnt2D.equal(firstCtrlPt, corner2, tol):
                        additionalPt_dict = {"Pt": Pnt2D(ctrlPts[1][0], ctrlPts[1][1]),
                                            "PtWeight": weights[1],
                                            "adjacentCorner": Pnt2D(ctrlPts[0][0], ctrlPts[0][1]),
                                            "adjacentPt": Pnt2D(ctrlPts[2][0], ctrlPts[2][1])}
                        additionalPts.append(additionalPt_dict)
                        polygonSeg.pop(1)
                        polygon_weightsSeg.pop(1)
                    else:
                        additionalPt_dict = {"Pt": Pnt2D(ctrlPts[-2][0], ctrlPts[-2][1]),
                                            "PtWeight": weights[-2],
                                            "adjacentCorner": Pnt2D(ctrlPts[-1][0], ctrlPts[-1][1]),
                                            "adjacentPt": Pnt2D(ctrlPts[-3][0], ctrlPts[-3][1])}
                        additionalPts.append(additionalPt_dict)
                        polygonSeg.pop(-1)
                        polygon_weightsSeg.pop(-1)

                polygon.extend(polygonSeg)
                polygon_weights.extend(polygon_weightsSeg)




        


            return MeshGeneration.Msh2DTemplateIsogeometric(polygon, polygon_weights, subv, additionalPts)





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
                return False, None, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None, None

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
                return False, None, None, None, None, None, None

        elif _mesh_type == 'Trilinear Transfinite':

            if len(segments) != 3:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText('The number of segments must be equal to 3')
                msg.exec()
                return False, None, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None, None

            m = side_pts[0]
            for number in side_pts:
                if number != m:
                    msg = QMessageBox(MeshGeneration.App)
                    msg.setWindowTitle('Warning')
                    msg.setText(
                        'All sides must have the same number of subdivisions')
                    msg.exec()
                    return False, None, None, None, None, None, None
            return MeshGeneration.Msh2DTrilinear(polygon, _elem_type, m)

        elif _mesh_type == 'Quadrilateral Template':
            num_seg = len(segments)

            if num_seg > 4:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'The number of segments must be between 2 and 4')
                msg.exec()
                return False, None, None, None, None, None, None

            if len(_face.intLoops) != 0:
                msg = QMessageBox(MeshGeneration.App)
                msg.setWindowTitle('Warning')
                msg.setText(
                    'it is not possible to generate the mesh with inner loops')
                msg.exec()
                return False, None, None, None, None, None, None

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
                        return False, None, None, None, None, None, None

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
            isIsogeometric = properties['isIsogeometric']
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
        pts = Mesh1D.subdivideSegment(_seg, number, ratio, quad, isIsogeometric)
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
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None

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
            return True, lines,  coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None

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
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None

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
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None

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
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None

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
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None
        
    def Msh2DTemplateIsogeometric(_pts, _weights, _subdv, _additionalPts):

        bry = aux.doublePointerWithValue(0.0, len(_pts)*3)
        subdv = aux.intPointerWithValue(0, 4)

        for i in range(0, len(_subdv)):
            aux.setIntValue(subdv, i, _subdv[i])

        index = 0
        for i in range(0, len(_pts)):
            aux.setDoubleValue(bry, index, float(_pts[i][0]) * float(_weights[i]))
            aux.setDoubleValue(bry, index + 1, float(_pts[i][1]) * float(_weights[i]))
            aux.setDoubleValue(bry, index + 2, float(_weights[i]))
            index += 3

        nno_output = aux.intPointerWithValue(0, 1)
        nel_output = aux.intPointerWithValue(0, 1)
        coords_output = aux.doubleVectorOfPointers(1, 1)
        conn_output = aux.intVectorOfPointers(1, 1)

        msh2d.Msh2DTemplate(4, subdv, 3, 4, 1,
                            bry, nno_output, coords_output, nel_output, conn_output)

        nno = aux.getIntValue(nno_output, 0)
        nel = aux.getIntValue(nel_output, 0)

        coords = []
        weights = []
        conn = []
        pts_pointer = aux.getDoublePointerOfVector(coords_output, 0)
        conn_pointer = aux.getIntPointerOfVector(conn_output, 0)

        item_index = 0
        for i in range(0, nno):
            tempItem = []
            for j in range(0, 3):
                item = aux.getDoubleValue(pts_pointer, item_index)
                tempItem.append(item)
                item_index += 1
            coords.extend([tempItem[0]/tempItem[2], tempItem[1]/tempItem[2]])
            weights.append(tempItem[2])


        for i in range(0, nel*(4+1)):
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


        # teste
        coords = [5.075000, 5.075000,
                5.033333, 5.595833,
                5.008125, 6.352969,
                5.001354, 7.211042,
                5.000000, 8.102344,
                5.000000, 9.000000,
                4.650521, 4.650521,
                4.364063, 5.243750,
                4.246562, 6.069687,
                4.208125, 7.015000,
                4.200937, 8.002812,
                4.200000, 9.000000,
                4.042031, 4.042031,
                3.644688, 4.741562,
                3.469688, 5.682500,
                3.413125, 6.751875,
                3.401094, 7.870469,
                3.400000, 9.000000,
                3.315729, 3.315729,
                2.870625, 4.146250,
                2.675625, 5.230000,
                2.615000, 6.451250,
                2.601250, 7.719375,
                2.600000, 9.000000,
                2.413281, 2.413281,
                2.005625, 3.445000,
                1.858125, 4.737656,
                1.810625, 6.130313,
                1.801406, 7.561250,
                1.800000, 9.000000,
                1.000000, 1.000000,
                1.000000, 2.600000,
                1.000000, 4.200000,
                1.000000, 5.800000,
                1.000000, 7.400000,
                1.000000, 9.000000,
                2.600000, 1.000000,
                4.200000, 1.000000,
                5.800000, 1.000000,
                7.400000, 1.000000,
                9.000000, 1.000000,
                3.445000, 2.005625,
                4.737656, 1.858125,
                6.130312, 1.810625,
                7.561250, 1.801406,
                9.000000, 1.800000,
                4.146250, 2.870625,
                5.230000, 2.675625,
                6.451250, 2.615000,
                7.719375, 2.601250,
                9.000000, 2.600000,
                4.741562, 3.644687,
                5.682500, 3.469688,
                6.751875, 3.413125,
                7.870469, 3.401094,
                9.000000, 3.400000,
                5.243750, 4.364062,
                6.069687, 4.246562,
                7.015000, 4.208125,
                8.002813, 4.200938,
                9.000000, 4.200000,
                5.595833, 5.033333,
                6.352969, 5.008125,
                7.211042, 5.001354,
                8.102344, 5.000000,
                9.000000, 5.000000,
                9.000000, 5.800000,
                9.000000, 6.600000,
                9.000000, 7.400000,
                9.000000, 8.200000,
                9.000000, 9.000000,
                8.161875, 5.799375,
                8.189375, 6.599531,
                8.198125, 7.399687,
                8.199844, 8.199844,
                8.200000, 9.000000,
                7.326875, 5.795625,
                7.378750, 6.594375,
                7.396250, 7.396250,
                7.399688, 8.198125,
                7.400000, 9.000000,
                6.505625, 5.779375,
                6.572813, 6.572813,
                6.594375, 7.378750,
                6.599531, 8.189375,
                6.600000, 9.000000,
                5.729687, 5.729688,
                5.779375, 6.505625,
                5.795625, 7.326875,
                5.799375, 8.161875,
                5.800000, 9.000000]

        # T-mesh array
        TMesh = np.array([[[conn[4], conn[3]], [conn[1], conn[2]]]])
        TMeshElem = []
        for i in range(6, len(conn)):
            if i%5 == 0:
                TMesh = np.concatenate((TMesh, [[[TMeshElem[3], TMeshElem[2]], [TMeshElem[0], TMeshElem[1]]]]), axis=0)
                TMeshElem = []
            else:
                TMeshElem.append(conn[i])
        TMesh = np.concatenate((TMesh, [[[TMeshElem[3], TMeshElem[2]], [TMeshElem[0], TMeshElem[1]]]]), axis=0)

        TMesh = np.array([[[7, 8],
                        [1, 2]],
                        [[8, 9],
                        [2, 3]],
                        [[9, 10],
                        [3, 4]],
                        [[10, 11],
                        [4, 5]],
                        [[11, 12],
                        [5, 6]],
                        [[13, 14],
                        [7, 8]],
                        [[14, 15],
                        [8, 9]],
                        [[15, 16],
                        [9, 10]],
                        [[16, 17],
                        [10, 11]],
                        [[17, 18],
                        [11, 12]],
                        [[19, 20],
                        [13, 14]],
                        [[20, 21],
                        [14, 15]],
                        [[21, 22],
                        [15, 16]],
                        [[22, 23],
                        [16, 17]],
                        [[23, 24],
                        [17, 18]],
                        [[25, 26],
                        [19, 20]],
                        [[26, 27],
                        [20, 21]],
                        [[27, 28],
                        [21, 22]],
                        [[28, 29],
                        [22, 23]],
                        [[29, 30],
                        [23, 24]],
                        [[31, 32],
                        [25, 26]],
                        [[32, 33],
                        [26, 27]],
                        [[33, 34],
                        [27, 28]],
                        [[34, 35],
                        [28, 29]],
                        [[35, 36],
                        [29, 30]],
                        [[25, 42],
                        [31, 37]],
                        [[42, 43],
                        [37, 38]],
                        [[43, 44],
                        [38, 39]],
                        [[44, 45],
                        [39, 40]],
                        [[45, 46],
                        [40, 41]],
                        [[19, 47],
                        [25, 42]],
                        [[47, 48],
                        [42, 43]],
                        [[48, 49],
                        [43, 44]],
                        [[49, 50],
                        [44, 45]],
                        [[50, 51],
                        [45, 46]],
                        [[13, 52],
                        [19, 47]],
                        [[52, 53],
                        [47, 48]],
                        [[53, 54],
                        [48, 49]],
                        [[54, 55],
                        [49, 50]],
                        [[55, 56],
                        [50, 51]],
                        [[7, 57],
                        [13, 52]],
                        [[57, 58],
                        [52, 53]],
                        [[58, 59],
                        [53, 54]],
                        [[59, 60],
                        [54, 55]],
                        [[60, 61],
                        [55, 56]],
                        [[1, 62],
                        [7, 57]],
                        [[62, 63],
                        [57, 58]],
                        [[63, 64],
                        [58, 59]],
                        [[64, 65],
                        [59, 60]],
                        [[65, 66],
                        [60, 61]],
                        [[65, 72],
                        [66, 67]],
                        [[72, 73],
                        [67, 68]],
                        [[73, 74],
                        [68, 69]],
                        [[74, 75],
                        [69, 70]],
                        [[75, 76],
                        [70, 71]],
                        [[64, 77],
                        [65, 72]],
                        [[77, 78],
                        [72, 73]],
                        [[78, 79],
                        [73, 74]],
                        [[79, 80],
                        [74, 75]],
                        [[80, 81],
                        [75, 76]],
                        [[63, 82],
                        [64, 77]],
                        [[82, 83],
                        [77, 78]],
                        [[83, 84],
                        [78, 79]],
                        [[84, 85],
                        [79, 80]],
                        [[85, 86],
                        [80, 81]],
                        [[62, 87],
                        [63, 82]],
                        [[87, 88],
                        [82, 83]],
                        [[88, 89],
                        [83, 84]],
                        [[89, 90],
                        [84, 85]],
                        [[90, 91],
                        [85, 86]],
                        [[1, 2],
                        [62, 87]],
                        [[2, 3],
                        [87, 88]],
                        [[3, 4],
                        [88, 89]],
                        [[4, 5],
                        [89, 90]],
                        [[5, 6],
                        [90, 91]]])

        nCtrlPoints = int(len(coords)/2)
        nTMeshElements = TMesh.shape[0]

        weights = [1.0] * nCtrlPoints

        _additionalPts = []
        additionalPt_dict = {"Pt": Pnt2D(1.0, 1.5),
                            "PtWeight": 1.0,
                            "adjacentCorner": Pnt2D(1.0, 1.0),
                            "adjacentPt": Pnt2D(1.0, 2.6)}
        _additionalPts.append(additionalPt_dict)

        additionalPt_dict = {"Pt": Pnt2D(1.5, 1.0),
                            "PtWeight": 1.0,
                            "adjacentCorner": Pnt2D(1.0, 1.0),
                            "adjacentPt": Pnt2D(2.6, 1.0)}
        _additionalPts.append(additionalPt_dict)

        boundaryCPIndex = np.array([], dtype=int)
        boundaryElements = np.array([], dtype=int)

        extraordinaryCPIndex = np.array([], dtype=int)
        oneRingECPElements = np.array([], dtype=int)

        # Find boundary elements
        for CP in range(1, nCtrlPoints + 1): #
            num = np.count_nonzero(TMesh == CP)
            elem = np.nonzero(TMesh == CP)
            elem = elem[0] + 1 #
            if num == 1 or num == 2:
                boundaryCPIndex = np.append(boundaryCPIndex, [CP])
                boundaryElements = np.append(boundaryElements, elem)

                for i in range(len(_additionalPts)):
                    additionalPt_dict = _additionalPts[i]
                    if Pnt2D.equal(additionalPt_dict["adjacentCorner"], Pnt2D(coords[CP*2-2], coords[CP*2-1]), Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)):
                        _additionalPts.remove(additionalPt_dict)
                        additionalPt_dict["adjacentCornerCPIndex"] = CP
                        _additionalPts.insert(i, additionalPt_dict)
                
                    if Pnt2D.equal(additionalPt_dict["adjacentPt"], Pnt2D(coords[CP*2-2], coords[CP*2-1]), Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)):
                        _additionalPts.remove(additionalPt_dict)
                        additionalPt_dict["adjacentPtCPIndex"] = CP
                        _additionalPts.insert(i, additionalPt_dict)

            elif num != 4:
                extraordinaryCPIndex = np.append(extraordinaryCPIndex, [CP])
                oneRingECPElements = np.append(oneRingECPElements, elem)

        boundaryElements = np.unique(boundaryElements)

        for i in range(len(_additionalPts)):
            additionalPt_dict = _additionalPts[i]
            Pt = additionalPt_dict["Pt"]
            coords.extend([Pt.getX(), Pt.getY()])
            _additionalPts.remove(additionalPt_dict)
            additionalPt_dict["PtCPIndex"] = int(len(coords)/2)
            _additionalPts.insert(i, additionalPt_dict)

        connec = []
        operators = []

        nExtraordinaryCP = len(extraordinaryCPIndex)
        # Conectivity of one ring extraordinaty control points elements
        index = 0
        for i in range(nExtraordinaryCP):
            CP = extraordinaryCPIndex[i]
            for j in range(3):
                elem = oneRingECPElements[index] - 1
                TMeshElem = TMesh[elem]

                # Resize
                while TMeshElem[1,0] != CP:
                    TMeshElem = np.array([[TMeshElem[0][1], TMeshElem[1][1]], [TMeshElem[0][0], TMeshElem[1][0]]])

                P4, P5, P8, P9 = TMeshElem[1,0], TMeshElem[1,1], TMeshElem[0,0], TMeshElem[0,1]

                topEdge = TMeshElem[0,:]
                bottomEdge = TMeshElem[1,:]
                rightEdge = TMeshElem[:,1]
                leftEdge = TMeshElem[:,0]

                # Top
                topEdgeElemIndex = np.intersect1d(np.nonzero(TMesh == topEdge[0])[0], np.nonzero(TMesh == topEdge[1])[0])
                topEdgeElem = TMesh[np.setdiff1d(topEdgeElemIndex,[elem])[0]]

                if (topEdgeElem[0,:] == np.flip(topEdge)).all():
                    P12, P13 = topEdgeElem[1,1], topEdgeElem[1,0]
                elif (topEdgeElem[1,:] == topEdge).all():
                    P12, P13 = topEdgeElem[0,0], topEdgeElem[0,1]
                elif (topEdgeElem[:,1] == np.flip(topEdge)).all():
                    P12, P13 = topEdgeElem[1,0], topEdgeElem[0,0]
                elif (topEdgeElem[:,0] == topEdge).all():
                    P12, P13 = topEdgeElem[0,1], topEdgeElem[1,1]

                # Bottom
                bottomEdgeElemIndex = np.intersect1d(np.nonzero(TMesh == bottomEdge[0])[0], np.nonzero(TMesh == bottomEdge[1])[0])
                bottomEdgeElem = TMesh[np.setdiff1d(bottomEdgeElemIndex,[elem])[0]]

                if (bottomEdgeElem[0,:] == bottomEdge).all():
                    P1, P2 = bottomEdgeElem[1,0], bottomEdgeElem[1,1]
                elif (bottomEdgeElem[1,:] == np.flip(bottomEdge)).all():
                    P1, P2 = bottomEdgeElem[0,1], bottomEdgeElem[0,0]
                elif (bottomEdgeElem[:,1] == bottomEdge).all():
                    P1, P2 = bottomEdgeElem[0,0], bottomEdgeElem[1,0]
                elif (bottomEdgeElem[:,0] == np.flip(bottomEdge)).all():
                    P1, P2 = bottomEdgeElem[1,1], bottomEdgeElem[0,1]

                # Right
                rightEdgeElemIndex = np.intersect1d(np.nonzero(TMesh == rightEdge[0])[0], np.nonzero(TMesh == rightEdge[1])[0])
                rightEdgeElem = TMesh[np.setdiff1d(rightEdgeElemIndex,[elem])[0]]

                if (rightEdgeElem[0,:] == np.flip(rightEdge)).all():
                    P6, P10 = rightEdgeElem[1,0], rightEdgeElem[1,1]
                elif (rightEdgeElem[1,:] == rightEdge).all():
                    P6, P10 = rightEdgeElem[0,1], rightEdgeElem[0,0]
                elif (rightEdgeElem[:,1] == np.flip(rightEdge)).all():
                    P6, P10 = rightEdgeElem[0,0], rightEdgeElem[1,0]
                elif (rightEdgeElem[:,0] == rightEdge).all():
                    P6, P10 = rightEdgeElem[1,1], rightEdgeElem[0,1]

                # Left
                leftEdgeElemIndex = np.intersect1d(np.nonzero(TMesh == leftEdge[0])[0], np.nonzero(TMesh == leftEdge[1])[0])
                leftEdgeElem = TMesh[np.setdiff1d(leftEdgeElemIndex,[elem])[0]]

                if (leftEdgeElem[0,:] == leftEdge).all():
                    P7 = leftEdgeElem[1,0]
                elif (leftEdgeElem[1,:] == np.flip(leftEdge)).all():
                    P7 = leftEdgeElem[0,1]
                elif (leftEdgeElem[:,1] == leftEdge).all():
                    P7 = leftEdgeElem[0,0]
                elif (leftEdgeElem[:,0] == np.flip(leftEdge)).all():
                    P7 = leftEdgeElem[1,1]

                # Corners
                P3index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P2)[0], np.nonzero(TMesh == P5)[0]), np.nonzero(TMesh == P6)[0])[0]
                P3 = np.sum(TMesh[P3index]) - (P2 + P5 + P6)
                P11index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P7)[0], np.nonzero(TMesh == P8)[0]), np.nonzero(TMesh == P12)[0])[0]
                P11 = np.sum(TMesh[P11index]) - (P7 + P8 + P12)
                P14index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P9)[0], np.nonzero(TMesh == P10)[0]), np.nonzero(TMesh == P13)[0])[0]
                P14 = np.sum(TMesh[P14index]) - (P9 + P10 + P13)

                # Append on connec 
                connec.append([P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14])

                index += 1

        # Conectivity of two ring extraordinaty control points elements and regular elements
        otherElements = np.setdiff1d(np.setdiff1d(np.linspace(1, nTMeshElements, num=nTMeshElements, dtype=int), boundaryElements), oneRingECPElements)
        for elem in otherElements:
            elem = elem - 1
            TMeshElem = TMesh[elem]
            print(TMeshElem)

            P6, P7, P10, P11 = TMeshElem[1,0], TMeshElem[1,1], TMeshElem[0,0], TMeshElem[0,1]

            topEdge = TMeshElem[0,:]
            bottomEdge = TMeshElem[1,:]
            rightEdge = TMeshElem[:,1]
            leftEdge = TMeshElem[:,0]

            # Top
            topNum = 0
            topEdgeLim = False
            targetElem = elem
            while not topEdgeLim and topNum < 3:
                topEdgeElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == topEdge[0])[0], np.nonzero(TMesh == topEdge[1])[0]),[targetElem])[0]
                topEdgeElem = TMesh[topEdgeElemIndex]

                if topNum == 0:
                    if (topEdgeElem[0,:] == np.flip(topEdge)).all():
                        P14, P15 = topEdgeElem[1,1], topEdgeElem[1,0]
                    elif (topEdgeElem[1,:] == topEdge).all():
                        P14, P15 = topEdgeElem[0,0], topEdgeElem[0,1]
                    elif (topEdgeElem[:,1] == np.flip(topEdge)).all():
                        P14, P15 = topEdgeElem[1,0], topEdgeElem[0,0]
                    elif (topEdgeElem[:,0] == topEdge).all():
                        P14, P15 = topEdgeElem[0,1], topEdgeElem[1,1]

                topEdge = np.setdiff1d(topEdgeElem.flatten(), topEdge)
                if np.isin(topEdge, boundaryCPIndex).all():
                    topEdgeLim = True

                targetElem = topEdgeElemIndex
                topNum += 1
            
            # Bottom
            bottomNum = 0
            bottomEdgeLim = False
            targetElem = elem
            while not bottomEdgeLim and bottomNum < 3:
                bottomEdgeElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == bottomEdge[0])[0], np.nonzero(TMesh == bottomEdge[1])[0]),[targetElem])[0]
                bottomEdgeElem = TMesh[bottomEdgeElemIndex]

                if bottomNum == 0:
                    if (bottomEdgeElem[0,:] == bottomEdge).all():
                        P2, P3 = bottomEdgeElem[1,0], bottomEdgeElem[1,1]
                    elif (bottomEdgeElem[1,:] == np.flip(bottomEdge)).all():
                        P2, P3 = bottomEdgeElem[0,1], bottomEdgeElem[0,0]
                    elif (bottomEdgeElem[:,1] == bottomEdge).all():
                        P2, P3 = bottomEdgeElem[0,0], bottomEdgeElem[1,0]
                    elif (bottomEdgeElem[:,0] == np.flip(bottomEdge)).all():
                        P2, P3 = bottomEdgeElem[1,1], bottomEdgeElem[0,1]

                bottomEdge = np.setdiff1d(bottomEdgeElem.flatten(), bottomEdge)
                if np.isin(bottomEdge, boundaryCPIndex).all():
                    bottomEdgeLim = True

                targetElem = bottomEdgeElemIndex
                bottomNum += 1

            # Right
            rightNum = 0
            rightEdgeLim = False
            targetElem = elem
            while not rightEdgeLim and rightNum < 3:
                rightEdgeElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == rightEdge[0])[0], np.nonzero(TMesh == rightEdge[1])[0]),[targetElem])[0]
                rightEdgeElem = TMesh[rightEdgeElemIndex]

                if rightNum == 0:
                    if (rightEdgeElem[0,:] == np.flip(rightEdge)).all():
                        P8, P12 = rightEdgeElem[1,0], rightEdgeElem[1,1]
                    elif (rightEdgeElem[1,:] == rightEdge).all():
                        P8, P12 = rightEdgeElem[0,1], rightEdgeElem[0,0]
                    elif (rightEdgeElem[:,1] == np.flip(rightEdge)).all():
                        P8, P12 = rightEdgeElem[0,0], rightEdgeElem[1,0]
                    elif (rightEdgeElem[:,0] == rightEdge).all():
                        P8, P12 = rightEdgeElem[1,1], rightEdgeElem[0,1]

                rightEdge = np.setdiff1d(rightEdgeElem.flatten(), rightEdge)
                if np.isin(rightEdge, boundaryCPIndex).all():
                    rightEdgeLim = True

                targetElem = rightEdgeElemIndex
                rightNum += 1
            
            # Left
            leftNum = 0
            leftEdgeLim = False
            targetElem = elem
            while not leftEdgeLim and leftNum < 3:
                leftEdgeElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == leftEdge[0])[0], np.nonzero(TMesh == leftEdge[1])[0]),[targetElem])[0]
                leftEdgeElem = TMesh[leftEdgeElemIndex]

                if leftNum == 0:
                    if (leftEdgeElem[0,:] == leftEdge).all():
                        P5, P9 = leftEdgeElem[1,1], leftEdgeElem[1,0]
                    elif (leftEdgeElem[1,:] == np.flip(leftEdge)).all():
                        P5, P9 = leftEdgeElem[0,0], leftEdgeElem[0,1]
                    elif (leftEdgeElem[:,1] == leftEdge).all():
                        P5, P9 = leftEdgeElem[1,0], leftEdgeElem[0,0], 
                    elif (leftEdgeElem[:,0] == np.flip(leftEdge)).all():
                        P5, P9 = leftEdgeElem[0,1], leftEdgeElem[1,1]

                leftEdge = np.setdiff1d(leftEdgeElem.flatten(), leftEdge)
                if np.isin(leftEdge, boundaryCPIndex).all():
                    leftEdgeLim = True

                targetElem = leftEdgeElemIndex
                leftNum += 1

            # topNum = 1: quina
            # topNum = 2
            # topNum = 3: elemento regular

            # Corners
            P1index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P2)[0], np.nonzero(TMesh == P5)[0]), np.nonzero(TMesh == P6)[0])[0]
            P1 = np.sum(TMesh[P1index]) - (P2 + P5 + P6)
            P4index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P3)[0], np.nonzero(TMesh == P7)[0]), np.nonzero(TMesh == P8)[0])[0]
            P4 = np.sum(TMesh[P4index]) - (P3 + P7 + P8)
            P13index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P9)[0], np.nonzero(TMesh == P10)[0]), np.nonzero(TMesh == P14)[0])[0]
            P13 = np.sum(TMesh[P13index]) - (P9 + P10 + P14)
            P16index = np.intersect1d(np.intersect1d(np.nonzero(TMesh == P11)[0], np.nonzero(TMesh == P12)[0]), np.nonzero(TMesh == P15)[0])[0]
            P16 = np.sum(TMesh[P16index]) - (P11 + P12 + P15)

            # Append on connec 
            connec.append([P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16])

        for additionalPt_dict in _additionalPts:
            adjacentCorner = additionalPt_dict["adjacentCorner"]
            adjacentCornerCPIndex = additionalPt_dict["adjacentCornerCPIndex"]
            adjacentPt = additionalPt_dict["adjacentPt"]
            adjacentPtCPIndex = additionalPt_dict["adjacentPtCPIndex"]
            Pt = additionalPt_dict["Pt"]
            PtCPIndex = additionalPt_dict["PtCPIndex"]

            for elem in boundaryElements:
                elem = elem - 1
                TMeshElem = TMesh[elem]
                if np.isin([adjacentCornerCPIndex, adjacentPtCPIndex], TMeshElem.flatten()).all():
                    while TMeshElem[1,0] != adjacentCornerCPIndex:
                        TMeshElem = np.array([[TMeshElem[0][1], TMeshElem[1][1]], [TMeshElem[0][0], TMeshElem[1][0]]])
                    # Calculate remaining control points:
                    if TMeshElem[0,0] == adjacentPtCPIndex:
                        TMeshElem_0_0 = adjacentPt
                        TMeshElem_0_1 = Pnt2D(coords[TMeshElem[0,1]*2-2], coords[TMeshElem[0,1]*2-1])
                        TMeshElem_1_0 = adjacentCorner
                        TMeshElem_1_1 = Pnt2D(coords[TMeshElem[1,1]*2-2], coords[TMeshElem[1,1]*2-1])

                        PolyTop = Polyline([TMeshElem_0_0, TMeshElem_0_1])
                        PolyBottom = Polyline([TMeshElem_1_0, TMeshElem_1_1])
                        PolyLeft = Polyline([TMeshElem_1_0, Pt, TMeshElem_0_0])
                        PolyRight = Polyline([TMeshElem_1_1, TMeshElem_0_1])

                        u, v = 1/3, 1/3
                        internalPt = (PolyBottom.evalPointSeg(u) * (1.0 - v) + PolyTop.evalPointSeg(u) * v + PolyLeft.evalPointSeg(v) * (1.0 - u) + PolyRight.evalPointSeg(v) * u -
                                      TMeshElem_1_0 * (1.0 - u) * (1.0 - v) - TMeshElem_0_0 * (1.0 - u) * v - TMeshElem_0_1 * u * v - TMeshElem_1_1 * u * (1.0 - v))
                        coords.extend([internalPt.getX(), internalPt.getY()])
                        internalPtCPIndex = int(len(coords)/2)

                        u, v = 1/3, 0.0
                        internalPtEdge = (PolyBottom.evalPointSeg(u) * (1.0 - v) + PolyTop.evalPointSeg(u) * v + PolyLeft.evalPointSeg(v) * (1.0 - u) + PolyRight.evalPointSeg(v) * u -
                                      TMeshElem_1_0 * (1.0 - u) * (1.0 - v) - TMeshElem_0_0 * (1.0 - u) * v - TMeshElem_0_1 * u * v - TMeshElem_1_1 * u * (1.0 - v))
                        
                        for j in range(0, len(coords), 2):
                            if Pnt2D.equal(internalPtEdge, Pnt2D(coords[j], coords[j+1]), Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)):
                                internalPtEdgeCPIndex = j/2 + 1
                            else:
                                coords.extend([internalPtEdge.getX(), internalPtEdge.getY()])
                                internalPtEdgeCPIndex = int(len(coords)/2)

                        # Connectivity
                        # Case 6
                        Case6ElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == TMeshElem[0,1])[0], np.nonzero(TMesh == TMeshElem[1,1])[0]),[elem])[0]
                        Case6Elem = TMesh[Case6ElemIndex]

                        while Case6Elem[1,0] != TMeshElem[0,1]:
                            Case6Elem = np.array([[Case6Elem[0][1], Case6Elem[1][1]], [Case6Elem[0][0], Case6Elem[1][0]]])

                        connecIndex = int(otherElements.index(Case6ElemIndex + 1) + nExtraordinaryCP * 3)
                        conE = connec[connecIndex]
                        while Case6Elem[1,0] != conE[6] and Case6Elem[1,1] != conE[7] and Case6Elem[0,0] != conE[10] and Case6Elem[0,1] != conE[11]:
                            conE = [conE[4], conE[8], conE[12], conE[16], conE[3], conE[7], conE[11], conE[15],
                                    conE[2], conE[6], conE[10], conE[14], conE[1], conE[5], conE[9], conE[13]]
                            
                        conE[3] = PtCPIndex
                        conE[4] = adjacentCornerCPIndex
                        conE[8]

                        # Case 5
                        topEdgeCase6Elem = Case6Elem[0,:]
                        Case5ElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == topEdgeCase6Elem[0])[0], np.nonzero(TMesh == topEdgeCase6Elem[1])[0]),[Case6Elem])[0]
                        Case5Elem = TMesh[Case5ElemIndex]

                        while Case5Elem[1,0] != Case6Elem[0,0]:
                            Case5Elem = np.array([[Case5Elem[0][1], Case5Elem[1][1]], [Case5Elem[0][0], Case5Elem[1][0]]])

                        connecIndex = int(otherElements.index(Case5ElemIndex + 1) + nExtraordinaryCP * 3)
                        conE = connec[connecIndex]
                        while Case5Elem[1,0] != conE[6] and Case5Elem[1,1] != conE[7] and Case5Elem[0,0] != conE[10] and Case5Elem[0,1] != conE[11]:
                            conE = [conE[4], conE[8], conE[12], conE[16], conE[3], conE[7], conE[11], conE[15],
                                    conE[2], conE[6], conE[10], conE[14], conE[1], conE[5], conE[9], conE[13]]

                        # Case 2
                        leftEdgeCase6Elem = Case6Elem[:,0]
                        Case2ElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == leftEdgeCase6Elem[0])[0], np.nonzero(TMesh == leftEdgeCase6Elem[1])[0]),[Case6Elem])[0]
                        Case2Elem = TMesh[Case2ElemIndex]

                        while Case2Elem[1,1] != Case6Elem[1,0]:
                            Case2Elem = np.array([[Case2Elem[0][1], Case2Elem[1][1]], [Case2Elem[0][0], Case2Elem[1][0]]])

                        connecIndex = int(otherElements.index(Case2ElemIndex + 1) + nExtraordinaryCP * 3)
                        conE = connec[connecIndex]
                        while Case2Elem[1,0] != conE[6] and Case2Elem[1,1] != conE[7] and Case2Elem[0,0] != conE[10] and Case2Elem[0,1] != conE[11]:
                            conE = [conE[4], conE[8], conE[12], conE[16], conE[3], conE[7], conE[11], conE[15],
                                    conE[2], conE[6], conE[10], conE[14], conE[1], conE[5], conE[9], conE[13]]

                        # Case 1
                        topEdgeCase2Elem = Case2Elem[0,:]
                        Case1ElemIndex = np.setdiff1d(np.intersect1d(np.nonzero(TMesh == topEdgeCase2Elem[0])[0], np.nonzero(TMesh == topEdgeCase2Elem[1])[0]),[Case2Elem])[0]
                        Case1Elem = TMesh[Case1ElemIndex]

                        while Case1Elem[1,0] != Case2Elem[0,0]:
                            Case1Elem = np.array([[Case1Elem[0][1], Case1Elem[1][1]], [Case1Elem[0][0], Case1Elem[1][0]]])

                        connecIndex = int(otherElements.index(Case1ElemIndex + 1) + nExtraordinaryCP * 3)
                        conE = connec[connecIndex]
                        while Case1Elem[1,0] != conE[6] and Case1Elem[1,1] != conE[7] and Case1Elem[0,0] != conE[10] and Case1Elem[0,1] != conE[11]:
                            conE = [conE[4], conE[8], conE[12], conE[16], conE[3], conE[7], conE[11], conE[15],
                                    conE[2], conE[6], conE[10], conE[14], conE[1], conE[5], conE[9], conE[13]]
                        
                    elif TMeshElem[1,1] == adjacentPtCPIndex:
                        TMeshElem_0_0 = Pnt2D(coords[TMeshElem[0,0]*2-2], coords[TMeshElem[0,0]*2-1])
                        TMeshElem_0_1 = Pnt2D(coords[TMeshElem[0,1]*2-2], coords[TMeshElem[0,1]*2-1])
                        TMeshElem_1_0 = adjacentCorner
                        TMeshElem_1_1 = adjacentPt

                        PolyTop = Polyline([TMeshElem_0_0, TMeshElem_0_1])
                        PolyBottom = Polyline([TMeshElem_1_0, TMeshElem_1_1])
                        PolyLeft = Polyline([TMeshElem_1_0, Pt, TMeshElem_0_0])
                        PolyRight = Polyline([TMeshElem_1_1, TMeshElem_0_1])
                        
                        u, v = 1/3, 1/3
                        internalPt = (PolyBottom.evalPointSeg(u) * (1.0 - v) + PolyTop.evalPointSeg(u) * v + PolyLeft.evalPointSeg(v) * (1.0 - u) + PolyRight.evalPointSeg(v) * u -
                                      TMeshElem_1_0 * (1.0 - u) * (1.0 - v) - TMeshElem_0_0 * (1.0 - u) * v - TMeshElem_0_1 * u * v - TMeshElem_1_1 * u * (1.0 - v))
                        coords.extend([internalPt.getX(), internalPt.getY()])
                        internalPtCPIndex = int(len(coords)/2)

                        u, v = 0.0, 1/3
                        internalPtEdge = (PolyBottom.evalPointSeg(u) * (1.0 - v) + PolyTop.evalPointSeg(u) * v + PolyLeft.evalPointSeg(v) * (1.0 - u) + PolyRight.evalPointSeg(v) * u -
                                      TMeshElem_1_0 * (1.0 - u) * (1.0 - v) - TMeshElem_0_0 * (1.0 - u) * v - TMeshElem_0_1 * u * v - TMeshElem_1_1 * u * (1.0 - v))
                        
                        for j in range(0, len(coords), 2):
                            if Pnt2D.equal(internalPtEdge, Pnt2D(coords[j], coords[j+1]), Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)):
                                internalPtEdgeCPIndex = j/2 + 1
                            else:
                                coords.extend([internalPtEdge.getX(), internalPtEdge.getY()])
                                internalPtEdgeCPIndex = int(len(coords)/2)
                        
                    

        if len(lines) > 0:
            return True, lines, coords, conn, nno, nel, None
        else:
            msg = QMessageBox(MeshGeneration.App)
            msg.setWindowTitle('Warning')
            msg.setText('it is not possible to generate the mesh')
            msg.exec()
            return False, lines, coords, conn, nno, nel, None
        
    # Based on nurbspy package developed by Roberto Agromayor PhD 
    # at Norwegian University of Science and Technology (NTNU) 
    # https://github.com/RoberAgro/nurbspy
    # Adapted to work with geomdl package

    def getCoonsSurface(nurbs_north, nurbs_south, nurbs_west, nurbs_east):
        # Check the that the NURBS curves are conforming

        # Check the number of control points
        if len(nurbs_north.ctrlpts) != len(nurbs_south.ctrlpts):
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves north and south must have conforming arrays of control points")
            # msg.exec()
            return False, None

        if len(nurbs_west.ctrlpts) != len(nurbs_east.ctrlpts):
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves north and south must have conforming arrays of control points")
            # msg.exec()
            return False, None

        # Check the number of weights
        if len(nurbs_north.weights) != len(nurbs_south.weights):
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves north and south must have conforming arrays of weights")
            # msg.exec()
            return False, None

        if len(nurbs_west.weights) != len(nurbs_east.weights):
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves west and east must have conforming arrays of weights")
            # msg.exec()
            return False, None

        # Check the curve degrees
        if nurbs_north.degree != nurbs_south.degree:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves north and south must have the same degree")
            # msg.exec()
            return False, None

        if nurbs_west.degree != nurbs_east.degree:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves west and east must have the same degree")
            # msg.exec()
            return False, None

        # Check the knot vectors
        if nurbs_north.knotvector != nurbs_south.knotvector:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves north and south must have the same knotvector")
            # msg.exec()
            return False, None

        if nurbs_west.knotvector != nurbs_east.knotvector:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("Curves west and east must have the same knotvector")
            # msg.exec()
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
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The north-west corner is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_south.ctrlpts[0][0] - nurbs_west.ctrlpts[0][0] <= Curve.COORD_TOL) and
            (nurbs_south.ctrlpts[0][1] - nurbs_west.ctrlpts[0][1] <= Curve.COORD_TOL)):

            nurbs_south.ctrlpts[0][0] = (nurbs_south.ctrlpts[0][0] + nurbs_west.ctrlpts[0][0]) / 2.0
            nurbs_west.ctrlpts[0][0] = nurbs_south.ctrlpts[0][0]
            nurbs_south.ctrlpts[0][1] = (nurbs_south.ctrlpts[0][1] + nurbs_west.ctrlpts[0][1]) / 2.0
            nurbs_west.ctrlpts[0][1] = nurbs_south.ctrlpts[0][1]

            P_sw = np.array([nurbs_south.ctrlpts[0][0], nurbs_south.ctrlpts[0][1]])
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-west corner is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_south.ctrlpts[-1][0] - nurbs_east.ctrlpts[0][0] <= Curve.COORD_TOL) and
            (nurbs_south.ctrlpts[-1][1] - nurbs_east.ctrlpts[0][1] <= Curve.COORD_TOL)):

            nurbs_south.ctrlpts[-1][0] = (nurbs_south.ctrlpts[-1][0] + nurbs_east.ctrlpts[0][0]) / 2.0
            nurbs_east.ctrlpts[0][0] = nurbs_south.ctrlpts[-1][0]
            nurbs_south.ctrlpts[-1][1] = (nurbs_south.ctrlpts[-1][1] + nurbs_east.ctrlpts[0][1]) / 2.0
            nurbs_east.ctrlpts[0][1] = nurbs_south.ctrlpts[-1][1]

            P_se = np.array([nurbs_south.ctrlpts[-1][0], nurbs_south.ctrlpts[-1][1]])
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-east corner is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_north.ctrlpts[-1][0] - nurbs_east.ctrlpts[-1][0] <= Curve.COORD_TOL) and
            (nurbs_north.ctrlpts[-1][1] - nurbs_east.ctrlpts[-1][1] <= Curve.COORD_TOL)):

            nurbs_north.ctrlpts[-1][0] = (nurbs_north.ctrlpts[-1][0] + nurbs_east.ctrlpts[-1][0]) / 2.0
            nurbs_east.ctrlpts[-1][0] = nurbs_north.ctrlpts[-1][0]
            nurbs_north.ctrlpts[-1][1] = (nurbs_north.ctrlpts[-1][1] + nurbs_east.ctrlpts[-1][1]) / 2.0
            nurbs_east.ctrlpts[-1][1] = nurbs_north.ctrlpts[-1][1]

            P_ne = np.array([nurbs_north.ctrlpts[-1][0], nurbs_north.ctrlpts[-1][1]])
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-east corner is not compatible")
            # msg.exec()
            return False, None

        # Check corner weight compatibility
        if ((nurbs_north.weights[0] - nurbs_west.weights[-1] <= Curve.PARAM_TOL) and
            (nurbs_north.weights[0] - nurbs_west.weights[-1] <= Curve.PARAM_TOL)):

            nurbs_north.weights[0] = (nurbs_north.weights[0] + nurbs_west.weights[-1]) / 2.0
            nurbs_west.weights[-1] = nurbs_north.weights[0]

            W_nw = np.array(nurbs_north.weights)[0]
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The north-west weight is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_south.weights[0] - nurbs_west.weights[0] <= Curve.PARAM_TOL) and
            (nurbs_south.weights[0] - nurbs_west.weights[0] <= Curve.PARAM_TOL)):

            nurbs_south.weights[0] = (nurbs_south.weights[0] + nurbs_west.weights[0]) / 2.0
            nurbs_west.weights[0] = nurbs_south.weights[0]

            W_sw = np.array(nurbs_south.weights)[0]
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-west weight is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_south.weights[-1] - nurbs_east.weights[0] <= Curve.PARAM_TOL) and
            (nurbs_south.weights[-1] - nurbs_east.weights[0] <= Curve.PARAM_TOL)):

            nurbs_south.weights[-1] = (nurbs_south.weights[-1] + nurbs_east.weights[0]) / 2.0
            nurbs_east.weights[0] = nurbs_south.weights[-1]

            W_se = np.array(nurbs_south.weights)[-1]
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-east weight is not compatible")
            # msg.exec()
            return False, None

        if ((nurbs_north.weights[-1] - nurbs_east.weights[-1] <= Curve.PARAM_TOL) and
            (nurbs_north.weights[-1] - nurbs_east.weights[-1] <= Curve.PARAM_TOL)):

            nurbs_north.weights[-1] = (nurbs_north.weights[-1] + nurbs_east.weights[-1]) / 2.0
            nurbs_east.weights[-1] = nurbs_north.weights[-1]

            W_ne = np.array(nurbs_north.weights)[-1]
        else:
            # msg = QMessageBox(MeshGeneration.App)
            # msg.setWindowTitle("Warning")
            # msg.setText("The sourth-east weight is not compatible")
            # msg.exec()
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

        # Factors between 0 and 1
        facx = 0.5
        facy = 0.5

        for i in range(Nu):
            u_i = float(np.asarray(u[:, i, :]))
            if u_i < 0.5:
                if facx < 0.5:
                    deltau = u_i - 0.0
                    u[:,i,:] -= deltau * (1 - facx * 2)

                elif facx > 0.5:
                    deltau = 0.5 - u_i
                    u[:,i,:] += deltau * (facx * 2 - 1)

                elif facx == 0.5:
                    pass

            elif u_i > 0.5:
                if facx < 0.5:
                    deltau = 1.0 - u_i
                    u[:,i,:] += deltau * (1 - facx * 2)

                elif facx > 0.5:
                    deltau = u_i - 0.5
                    u[:,i,:] -= deltau * (facx * 2 - 1)

                elif facx == 0.5:
                    pass

            elif u_i == 0.5:
                pass

        for j in range(Nv):
            v_j = float(np.asarray(v[:, :, j]))
            if v_j < 0.5:
                if facy < 0.5:
                    deltav = v_j - 0.0
                    v[:,:,j] -= deltav * (1 - facy * 2)

                elif facy > 0.5:
                    deltav = 0.5 - v_j
                    v[:,:,j] += deltav * (facy * 2 - 1)

                elif facy == 0.5:
                    pass

            elif v_j > 0.5:
                if facy < 0.5:
                    deltav = 1.0 - v_j
                    v[:,:,j] += deltav * (1 - facy * 2)

                elif facy > 0.5:
                    deltav = v_j - 0.5
                    v[:,:,j] -= deltav * (facy * 2 - 1)

                elif facy == 0.5:
                    pass

            elif v_j == 0.5:
                pass

        term_1a = (1 - v) * Pw_south + (v) * Pw_north
        term_1b = (1 - u) * Pw_west + (u) * Pw_east
        u = np.linspace(0, 1, Nu)[np.newaxis, :, np.newaxis]
        v = np.linspace(0, 1, Nv)[np.newaxis, np.newaxis, :]
        term_2 = (1 - u) * (1 - v) * Pw_sw + (u) * (v) * Pw_ne + (1 - u) * (v) * Pw_nw + (u) * (1 - v) * Pw_se
        Pw = term_1a + term_1b - term_2

        Pw[:, 0, :] = Pw_west.squeeze()
        Pw[:, -1, :] = Pw_east.squeeze()
        Pw[:, :, 0] = Pw_south.squeeze()
        Pw[:, :, -1] = Pw_north.squeeze()

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
        MeshCurves = MeshGeneration.getIsoCurves(coonsSurf)

        Nu = coonsSurf.ctrlpts_size_u
        Nv = coonsSurf.ctrlpts_size_v
        degreeU = coonsSurf.degree_u
        degreeV = coonsSurf.degree_v
        knotvectorU = coonsSurf.knotvector_u
        knotvectorV = coonsSurf.knotvector_v

        nel = (len(set(coonsSurf.knotvector_u)) - 1) * (len(set(coonsSurf.knotvector_v)) - 1)
        nno = Nu * Nv

        coords = np.reshape(np.transpose(coonsSurf.ctrlpts), (2,Nu,Nv), order='C')
        coords = list(np.transpose(coords).flat)

        weights = np.reshape(coonsSurf.weights, (Nu,Nv), order='C')
        weights = list(np.transpose(weights).flat)

        elRangeU, elRangeV, element, index = MeshGeneration.connectivityIsogeometric(Nu, Nv, degreeU, degreeV, knotvectorU, knotvectorV)
        element = list(element.flat)
        element = [int(item) for item in element]
        conn = []
        nCtrlPts = (degreeU + 1) * (degreeV + 1)
        conn.append(nCtrlPts)
        for i in range(len(element)):
            conn.append(element[i])
            if (i + 1)%(nCtrlPts) == 0:
                conn.append(nCtrlPts)
        conn.pop()

        iso_dict = {"weights": weights,
                    "elRangeU": elRangeU.tolist(),
                    "elRangeV": elRangeV.tolist(),
                    "index": index.tolist()}

        return True, MeshCurves, coords, conn, nno, nel, iso_dict

    def getIsoCurves(coonsSurf):
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
        return MeshCurves
    
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
    
    def connectivityIsogeometric(noPtsU, noPtsV, p, q, uKnot, vKnot):
        noElemsU = len(set(uKnot)) - 1
        noElemsV = len(set(vKnot)) - 1
        noElems = noElemsU * noElemsV

        # chan for a 4x3 control points
        chan = np.zeros((noPtsV, noPtsU))

        count = 0
        for i in range(noPtsV):
            for j in range(noPtsU):
                chan[i,j] = count
                count = count + 1

        # Determine our element ranges and the corresponding knot indices along each direction
        elRangeU, elConnU = MeshGeneration.buildConnectivityIsogeometric(p, uKnot, noElemsU)
        elRangeV, elConnV = MeshGeneration.buildConnectivityIsogeometric(q, vKnot, noElemsV)

        # combine info from two directions to build the elements
        # element is numbered as follows
        #  5 | 6 | 7 | 8
        # ---------------
        #  1 | 2 | 3 | 4 
        # for a 4x2 mesh
        element = np.zeros((noElems, (p+1)*(q+1)))

        e = 0
        for v in range(noElemsV):
            vConn = elConnV[v,:]
            for u in range(noElemsU):
                c = 0
                uConn = elConnU[u,:]
                for i in range(len(vConn)):
                    for j in range(len(uConn)):
                        element[e,c] = chan[vConn[i],uConn[j]]
                        c = c + 1
                e = e + 1

        index = np.zeros((noElems, 2))
        count = 0

        for j in range(elRangeV.shape[0]):
            for i in range(elRangeU.shape[0]):
                index[count,0] = i
                index[count,1] = j

                count = count + 1

        return elRangeU, elRangeV, element, index

    def buildConnectivityIsogeometric(p, knotVec, noElems):
        # compute connectivity of 1D NURBS (for one direction)
        # also define the element ranges i.e. [xi1,xi2]
        # Adapted from the IGABEM code of Robert Simpson, Cardiff, UK
        # Vinh Phu Nguyen
        # Delft University of Technology, The Netherlands
        
        elRange = np.zeros((noElems, 2))   
        elKnotIndices = np.zeros((noElems, 2), dtype=int)
        elConn = np.zeros((noElems, p+1), dtype=int)
        ne = len(np.unique(knotVec)) - 1 # number of elements
        
        element = 0
        previousKnotVal = 0
        
        for i in range(len(knotVec)):
            currentKnotVal = knotVec[i]
            if knotVec[i] != previousKnotVal:
                elRange[element,:] = [previousKnotVal, currentKnotVal]
                elKnotIndices[element,:] = [i-1, i]
                element += 1
            previousKnotVal = currentKnotVal
        
        numRepeatedKnots = 0
        for e in range(ne):
            indices = np.arange(elKnotIndices[e,0]-p+1, elKnotIndices[e,0]+1)
            previousKnotVals = knotVec[(elKnotIndices[e,1]-p+1):elKnotIndices[e,1]]
            currentKnotVals = np.ones(p)*knotVec[elKnotIndices[e,0]]
            if np.array_equal(previousKnotVals,currentKnotVals) and len(np.nonzero(previousKnotVals)[0])>1:
                numRepeatedKnots += 1
            elConn[e,:] = np.arange(elKnotIndices[e,0]-p, elKnotIndices[e,0]+1)
            
        return elRange, elConn