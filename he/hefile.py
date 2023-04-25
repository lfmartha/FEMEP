import json
from compgeom.pnt2d import Pnt2D
from OpenGL.error import Error
from geometry.point import Point
from geometry.curves.line import Line
from geometry.curves.polyline import Polyline
from geometry.curves.cubicspline import CubicSpline
from geometry.curves.circle import Circle
from geometry.curves.circlearc import CircleArc
from geometry.curves.ellipse import Ellipse
from geometry.curves.ellipsearc import EllipseArc
from geometry.patch import Patch
from he.topologicalEntities.vertex import Vertex
from he.topologicalEntities.face import Face
from he.topologicalEntities.edge import Edge
from he.topologicalEntities.loop import Loop
from he.topologicalEntities.halfedge import HalfEdge
from he.topologicalEntities.shell import Shell
from geometry.attributes.attribsymbols import AttribSymbols
from compgeom.compgeom import CompGeom
from mesh.mesh1d import Mesh1D
from geometry.segment import Segment
from geometry.curves.curve import Curve
import numpy as np
import math
import copy


class HeFile():

    @staticmethod
    def saveFile(_shell, _attributes, _filename):

        # get topological entities
        vertices = _shell.vertices
        edges = _shell.edges
        faces = _shell.faces

        # create/ open a file
        split_name = _filename.split('.')
        if split_name[-1] == 'json':
            file = open(f"{_filename}", "w")
        else:
            file = open(f"{_filename}.json", "w")

        # saves the vertices
        vertices_list = []
        for vertex in vertices:

            attributes = vertex.point.attributes
            att_list = []
            for att in attributes:
                att_list.append(att['name'])

            attributes_dict = {
                "att_names": att_list
            }

            if vertex.prev is None:
                prev_ID = None
            else:
                prev_ID = vertex.prev.ID

            if vertex.next is None:
                next_ID = None
            else:
                next_ID = vertex.next.ID

            vertex_dict = {
                'type': 'VERTEX',
                'ID': vertex.ID,
                'prev_ID': prev_ID,
                'next_ID': next_ID,
                'he_ID': vertex.he.ID,
                'point': (vertex.point.getX(), vertex.point.getY()),
                'attributes': attributes_dict
            }
            vertices_list.append(vertex_dict)

        # saves the edges
        edges_list = []
        for edge in edges:

            data_dict = edge.segment.getDataToInitCurve()

            attributes = edge.segment.attributes.copy()
            if edge.segment.nsudv is not None:
                attributes.remove(edge.segment.nsudv)
            att_list = []
            for att in attributes:
                att_list.append(att['name'])

            attributes_dict = {
                "nsudv": edge.segment.nsudv,
                "att_names": att_list
            }

            if edge.prev is None:
                prev_ID = None
            else:
                prev_ID = edge.prev.ID

            if edge.next is None:
                next_ID = None
            else:
                next_ID = edge.next.ID

            edge_dict = {
                'type': 'EDGE',
                'ID': edge.ID,
                'prev_ID': prev_ID,
                'next_ID': next_ID,
                'he1_ID': edge.he1.ID,
                'he2_ID': edge.he2.ID,
                'segment_type': f'{edge.segment.getType()}',
                'data': data_dict,
                'attributes': attributes_dict
            }

            edges_list.append(edge_dict)

        # saves the faces
        faces_list = []
        for face in faces:

            if face.loop.next is None:
                next_ID = None
            else:
                next_ID = face.loop.next.ID

            # saves the external loop
            he = face.loop.he
            he_begin = he

            if he is None:
                he_list = None
            else:
                he_list = []
                while True:

                    he_dict = {
                        'type': 'HALF-EDGE',
                        'ID': he.ID,
                        'prev_ID': he.prev.ID,
                        'next_ID': he.next.ID,
                        'vertex_ID': he.vertex.ID,
                        'edge_ID': he.edge.ID,
                        'loop_ID': he.loop.ID
                    }

                    he_list.append(he_dict)
                    he = he.next

                    if he == he_begin:
                        break

            loop_dict = {
                'type': 'LOOP',
                'ID': face.loop.ID,
                'prev_ID': None,
                'next_ID': next_ID,
                'face_ID': face.ID,
                'he_loop': he_list,
                'isClosed': face.loop.isClosed

            }

            # saves the internal loops
            intLoops = []
            intLoop = face.loop.next
            while intLoop is not None:

                he = intLoop.he
                he_begin = he

                he_list = []
                while True:

                    if he.edge is None:
                        edge_ID = None
                    else:
                        edge_ID = he.edge.ID

                    he_dict = {
                        'type': 'HALF-EDGE',
                        'ID': he.ID,
                        'prev_ID': he.prev.ID,
                        'next_ID': he.next.ID,
                        'vertex_ID': he.vertex.ID,
                        'edge_ID': edge_ID,
                        'loop_ID': he.loop.ID
                    }

                    he_list.append(he_dict)
                    he = he.next

                    if he == he_begin:
                        break

                if intLoop.next is None:
                    next_ID = None
                else:
                    next_ID = intLoop.next.ID

                intLoop_dict = {
                    'type': 'LOOP',
                    'ID': intLoop.ID,
                    'prev_ID': intLoop.prev.ID,
                    'next_ID': next_ID,
                    'face_ID': face.ID,
                    'he_loop': he_list,
                    'isClosed': intLoop.isClosed
                }

                intLoops.append(intLoop_dict)
                intLoop = intLoop.next

            attributes = face.patch.attributes.copy()
            if face.patch.mesh is not None:
                mesh_dict = face.patch.mesh.mesh_dict
                attributes.remove(mesh_dict)
            else:
                mesh_dict = None

            att_list = []
            for att in attributes:
                att_list.append(att['name'])

            attributes_dict = {
                'isDeleted': face.patch.isDeleted,
                'mesh': mesh_dict,
                "att_names": att_list
            }

            if face.prev is None:
                prev_ID = None
            else:
                prev_ID = face.prev.ID

            if face.next is None:
                next_ID = None
            else:
                next_ID = face.next.ID

            dataSurf_dict = face.patch.getDataToInitSurface()

            face_dict = {
                'type': 'FACE',
                'ID': face.ID,
                'prev_ID': prev_ID,
                'next_ID': next_ID,
                'loop': loop_dict,
                'intLoops': intLoops,
                'attributes': attributes_dict,
                'dataSurf': dataSurf_dict
            }

            faces_list.append(face_dict)

        shell = {
            'type': 'SHELL',
            'vertices': vertices_list,
            'edges': edges_list,
            'faces': faces_list,
            'attributes_list': _attributes
        }

        json.dump(shell, file, indent=4)
        file.close()

    @ staticmethod
    def loadFile(_file):
        with open(_file, 'r') as file:
            input = json.load(file)

        vertices = input['vertices']
        edges = input['edges']
        faces = input['faces']
        attributes = input['attributes_list']

        # creates the shell
        shell = Shell()

        # creates the edges
        for edge_dict in edges:
            edge = Edge()
            edge.ID = edge_dict['ID']

            # creates a key for the edge
            edge_dict['edge'] = edge

            # set edge segment
            data_dict = edge_dict['data']
            type = edge_dict['segment_type']

            if type == 'LINE':
                pt0 = Pnt2D(data_dict['pt0'][0], data_dict['pt0'][1])
                pt1 = Pnt2D(data_dict['pt1'][0], data_dict['pt1'][1])
                curve = Line(pt0, pt1)
                curvePoly = curve.getEquivPolyline()
                segment = Segment(curvePoly, curve)
                #segment.originalNurbs = copy.deepcopy(curve.nurbs)
                segment.isReversed = data_dict['isReversed']
                try:
                    segment.surfDirection = data_dict['surfDirection']
                except:
                    pass

                if data_dict['isReversed'] == True:
                    segment.ReverseNurbs()

                diff = data_dict['currentDegree'] - curve.nurbs.degree
                if diff > 0:
                    for i in range(diff):
                        segment.degreeChange()

                if data_dict['currentKnotVector'] != curve.nurbs.knotvector:
                    segment.conformFromKnotVector(data_dict['currentKnotVector'])

            elif type == 'POLYLINE':
                pts = []
                for i in range (len(data_dict['pts'])):
                    pts.append(Pnt2D(data_dict['pts'][i][0], data_dict['pts'][i][1]))
                curve = Polyline(pts)
                curvePoly = curve.getEquivPolyline()
                segment = Segment(curvePoly, curve)
                segment.originalNurbs = copy.deepcopy(curve.nurbs)
                segment.isReversed = data_dict['isReversed']
                try:
                    segment.surfDirection = data_dict['surfDirection']
                except:
                    pass

                if data_dict['isReversed'] == True:
                    segment.ReverseNurbs()
                    
                diff = data_dict['currentDegree'] - curve.nurbs.degree
                if diff > 0:
                    for i in range(diff):
                        segment.degreeChange()

                if data_dict['currentKnotVector'] != curve.nurbs.knotvector:
                    segment.conformFromKnotVector(data_dict['currentKnotVector'])

            elif type == 'CUBICSPLINE':
                degree = data_dict['degree']
                ctrlpts = data_dict['ctrlpts']
                weights = data_dict['weights']
                knotvector = data_dict['knotvector']
                curve = CubicSpline(degree, ctrlpts, weights, knotvector)
                curvePoly = curve.getEquivPolyline()
                segment = Segment(curvePoly, curve)
                segment.originalNurbs = copy.deepcopy(curve.nurbs)
                segment.isReversed = data_dict['isReversed']
                try:
                    segment.surfDirection = data_dict['surfDirection']
                except:
                    pass

            elif type == 'CIRCLEARC':
                center = Pnt2D(data_dict['center'][0], data_dict['center'][1])
                circ1 = Pnt2D(data_dict['circ1'][0], data_dict['circ1'][1])
                circ2 = Pnt2D(data_dict['circ2'][0], data_dict['circ2'][1])
                curve = CircleArc(center, circ1, circ2)
                curvePoly = curve.getEquivPolyline()
                segment = Segment(curvePoly, curve)
                segment.originalNurbs = copy.deepcopy(curve.nurbs)
                segment.isReversed = data_dict['isReversed']
                try:
                    segment.surfDirection = data_dict['surfDirection']
                except:
                    pass

                if data_dict['isReversed'] == True:
                    segment.ReverseNurbs()
                    
                diff = data_dict['currentDegree'] - curve.nurbs.degree
                if diff > 0:
                    for i in range(diff):
                        segment.degreeChange()

                if data_dict['currentKnotVector'] != curve.nurbs.knotvector:
                    segment.conformFromKnotVector(data_dict['currentKnotVector'])

            elif type == 'ELLIPSEARC':
                center = Pnt2D(data_dict['center'][0], data_dict['center'][1])
                ellip1 = Pnt2D(data_dict['ellip1'][0], data_dict['ellip1'][1])
                ellip2 = Pnt2D(data_dict['ellip2'][0], data_dict['ellip2'][1])
                arc1 = Pnt2D(data_dict['arc1'][0], data_dict['arc1'][1])
                arc2 = Pnt2D(data_dict['arc2'][0], data_dict['arc2'][1])
                curve = EllipseArc(center, ellip1, ellip2, arc1, arc2)
                curvePoly = curve.getEquivPolyline()
                segment = Segment(curvePoly, curve)
                segment.originalNurbs = copy.deepcopy(curve.nurbs)
                segment.isReversed = data_dict['isReversed']
                try:
                    segment.surfDirection = data_dict['surfDirection']
                except:
                    pass

                if data_dict['isReversed'] == True:
                    segment.ReverseNurbs()
                    
                diff = data_dict['currentDegree'] - curve.nurbs.degree
                if diff > 0:
                    for i in range(diff):
                        segment.degreeChange()

                if data_dict['currentKnotVector'] != curve.nurbs.knotvector:
                    segment.conformFromKnotVector(data_dict['currentKnotVector'])

            edge.segment = segment

            # set segment attributes
            att_names = edge_dict['attributes']['att_names']
            for att_name in att_names:
                for attribute in attributes:
                    if att_name == attribute['name']:
                        segment.attributes.append(attribute)

            if edge_dict['attributes']['nsudv'] is not None:
                segment.setNumberSdv(
                    edge_dict['attributes']['nsudv'])
                segment.attributes.append(edge_dict['attributes']['nsudv'])

        # creates the vertices
        for vertex_dict in vertices:
            vertex = Vertex()
            vertex.ID = vertex_dict['ID']

            # creates a key for the vertex
            vertex_dict['vertex'] = vertex

            # set the point
            pt = vertex_dict['point']
            vertex.point = Point(pt[0], pt[1])

            # set point attributes
            att_names = vertex_dict['attributes']['att_names']
            for att_name in att_names:
                for attribute in attributes:
                    if att_name == attribute['name']:
                        vertex.point.attributes.append(attribute)

        # creates the faces
        for face_dict in faces:
            face = Face(shell)
            face.patch = Patch()
            face.ID = face_dict['ID']

            # set patch attributes
            att_names = face_dict['attributes']['att_names']
            for att_name in att_names:
                for attribute in attributes:
                    if att_name == attribute['name']:
                        face.patch.attributes.append(attribute)

            # creates a key for the face
            face_dict['face'] = face

            # creates the outer loop
            loop_dict = face_dict['loop']
            loop = Loop(face)
            loop.ID = loop_dict['ID']
            loop.isClosed = loop_dict['isClosed']

            # creates the half-edges
            he_dicts = loop_dict['he_loop']
            if he_dicts is not None:
                for he_dict in he_dicts:
                    he = HalfEdge()
                    he.ID = he_dict['ID']
                    he.loop = loop

                    # creates a key for the he
                    he_dict['he'] = he

                    # set he.vertex and vertex.he
                    for vertex_dict in vertices:
                        if he_dict['vertex_ID'] == vertex_dict['ID']:
                            he.vertex = vertex_dict['vertex']

                            if vertex_dict['he_ID'] == he.ID:
                                he.vertex.he = he

                            break

                    # set he.edge and edge.he(1 or 2)
                    for edge_dict in edges:
                        if he_dict['edge_ID'] == edge_dict['ID']:
                            he.edge = edge_dict['edge']

                            if edge_dict['he1_ID'] == he.ID:
                                he.edge.he1 = he
                                he.edge.segment.setInitPoint(he.vertex.point)
                            else:
                                he.edge.he2 = he
                                he.edge.segment.setEndPoint(he.vertex.point)

                            break

                # set he.prev/next
                he_dicts[0]['he'].prev = he_dicts[-1]['he']
                he_dicts[-1]['he'].next = he_dicts[0]['he']
                for i in range(1, len(he_dicts)):
                    he_dicts[i]['he'].prev = he_dicts[i-1]['he']
                    he_dicts[i-1]['he'].next = he_dicts[i]['he']

                # set loop.he
                loop.he = he_dicts[0]['he']

            # creates internal loops
            intLoops_list = []
            intLoops_dict = face_dict['intLoops']
            for intLoop_dict in intLoops_dict:
                intLoop = Loop()
                intLoop.face = face
                intLoop.ID = intLoop_dict['ID']
                intLoop.isClosed = intLoop_dict['isClosed']
                intLoops_list.append(intLoop)

                # creates the half-edges
                he_dicts = intLoop_dict['he_loop']
                for he_dict in he_dicts:
                    he = HalfEdge()
                    he.ID = he_dict['ID']
                    he.loop = intLoop

                    # creates a key for the he
                    he_dict['he'] = he

                    # set he.vertex and vertex.he
                    for vertex_dict in vertices:
                        if he_dict['vertex_ID'] == vertex_dict['ID']:
                            he.vertex = vertex_dict['vertex']

                            if vertex_dict['he_ID'] == he.ID:
                                he.vertex.he = he

                            break

                    # set he.edge and edge.he(1 or 2)
                    for edge_dict in edges:
                        if he_dict['edge_ID'] == edge_dict['ID']:
                            he.edge = edge_dict['edge']

                            if edge_dict['he1_ID'] == he.ID:
                                he.edge.he1 = he
                                he.edge.segment.setInitPoint(he.vertex.point)
                            else:
                                he.edge.he2 = he
                                he.edge.segment.setEndPoint(he.vertex.point)

                # set he.prev/next
                he_dicts[0]['he'].prev = he_dicts[-1]['he']
                he_dicts[-1]['he'].next = he_dicts[0]['he']
                for i in range(1, len(he_dicts)):
                    he_dicts[i]['he'].prev = he_dicts[i-1]['he']
                    he_dicts[i-1]['he'].next = he_dicts[i]['he']

                # set loop.he
                intLoop.he = he_dicts[0]['he']

            # set loop.prev/next
            if len(intLoops_list) > 0:
                intLoops_list[0].prev = loop
                loop.next = intLoops_list[0]

            for i in range(1, len(intLoops_list)):
                intLoops_list[i].prev = intLoops_list[i-1]
                intLoops_list[i-1].next = intLoops_list[i]

            # set attributes
            attributes_dict = face_dict['attributes']
            face.patch.isDeleted = attributes_dict['isDeleted']

        # set shell face
        shell.face = faces[0]['face']

        # set face prev/next
        for i in range(1, len(faces)):
            faces[i]['face'].prev = faces[i-1]['face']
            faces[i-1]['face'].next = faces[i]['face']

        return vertices, edges, faces, attributes

    @ staticmethod
    def exportFile(_option, _shell, _filename, _alType, _gpT3, _gpT6, _gpQ4, _qpQ8):

        if _option == "Femoolab":
            if _alType == "Plane Stress":
                HeFile.exportFileToFemoolabPlaneStress(
                    _shell, _filename, _gpT3, _gpT6, _gpQ4, _qpQ8)
            elif _alType == "Plane Conduction":
                HeFile.exportFileToTFemoolabPlaneConduction(
                    _shell, _filename, _gpT3, _gpT6, _gpQ4, _qpQ8)

    @ staticmethod
    # Export to Femoolab - Finite Element Model Laboratory
    def exportFileToFemoolabPlaneStress(_shell, _filename, _gpT3, _gpT6, _gpQ4, _qpQ8):

        split_name = _filename.split('.')
        if split_name[-1] == 'json':
            split_name.remove('json')

        filename = ''
        for i in range(len(split_name)):
            if i == 0:
                filename += split_name[i]
            else:
                filename += '.' + split_name[i]

        faces = _shell.faces
        edges = _shell.edges
        vertices = _shell.vertices

        # the faces of the solid must be connected
        if len(_shell.face.intLoops) > 1:
            raise Error

        sc_points = []  # points that have support conditions
        ul_segments = []  # segments that have uniform load
        cl_points = []  # points that have concentrated load
        for edge in edges:
            attributes = edge.segment.attributes
            support_condition = None
            number_subdv = None
            uniform_load = None
            isQuadratic = False
            isIsogeometric = False
            incidentFaces = edge.incidentFaces()

            for face in incidentFaces:
                if face.patch.mesh is not None:
                    mesh_dict = face.patch.mesh.mesh_dict
                    if mesh_dict['properties']['Element type'] == "T6" or mesh_dict['properties']['Element type'] == "Q8":
                        isQuadratic = True

                    if mesh_dict['properties']['Element type'] == "Isogeometric":
                        isIsogeometric = True

            for att in attributes:
                if att["type"] == "Uniform Load":
                    uniform_load = att
                elif att["type"] == "Support Conditions":
                    support_condition = att
                elif att["type"] == "Number of Subdivisions":
                    number_subdv = att

            if support_condition is not None:
                if number_subdv is not None:
                    subdv_pts = HeFile.Nsbdvs(
                        number_subdv, edge.segment, isQuadratic, isIsogeometric)

                    for pt in subdv_pts:
                        sc_point = {
                            "point": pt,
                            "support": support_condition
                        }
                        sc_points.append(sc_point)

            if uniform_load is not None:

                if uniform_load['properties']['Direction']["index"] != 0:
                    localUL = True
                else:
                    localUL = False
                    load = [uniform_load['properties']['Qx'],
                            uniform_load['properties']['Qy']]

                if number_subdv is not None:
                    subdv_pts = HeFile.Nsbdvs(
                        number_subdv, edge.segment, isQuadratic, isIsogeometric)
                    edge_pts = edge.segment.getPoints()
                    subdv_pts.insert(0, edge_pts[0])
                    subdv_pts.append(edge_pts[-1])

                    while len(subdv_pts) > 1:
                        if isIsogeometric:
                            seg = Polyline(subdv_pts)

                            if localUL:
                                load = HeFile.getUniformLoadGlobalValues(
                                    uniform_load, seg)

                            ul_segment = {
                                "segment": seg,
                                "load": load,
                                "mesh_pts": [0] * len(subdv_pts)
                            }
                            ul_segments.append(ul_segment)
                            subdv_pts = []

                        else: 
                            seg = Line(subdv_pts.pop(0), subdv_pts[0])

                            if localUL:
                                load = HeFile.getUniformLoadGlobalValues(
                                    uniform_load, seg)

                            ul_segment = {
                                "segment": seg,
                                "load": load,
                                "mesh_pt1": None,
                                "mesh_pt2": None
                            }
                            ul_segments.append(ul_segment)
                else:
                    # ???
                    ul_segment = {
                        "segment": edge.segment,
                        "load": load,
                        "mesh_pt1": None,
                        "mesh_pt2": None
                    }
                    ul_segments.append(ul_segment)

        for vertex in vertices:
            attributes = vertex.point.attributes

            for att in attributes:
                if att["type"] == "Support Conditions":
                    sc_point = {
                        "point": Pnt2D(vertex.point.getX(), vertex.point.getY()),
                        "support": att
                    }
                    sc_points.append(sc_point)

                elif att["type"] == "Concentrated Load":
                    cl_point = {
                        "point": Pnt2D(vertex.point.getX(), vertex.point.getY()),
                        "load": att
                    }
                    cl_points.append(cl_point)

        # it is not possible to export a model without support conditions
        if len(sc_points) == 0:
            raise Error

        # get information
        meshes = []  # list of meshes
        mesh_points = []  # list of all points in the global mesh
        meshes_map_pts = []  # set of points in each local mesh
        mesh_support_pts = []  # list of points with support conditions
        mesh_cl_pts = []  # list of points with concentraded load
        materials = []  # list of materials
        thicknesses = []  # list of thicknesses
        global_index = 1  # global index of points
        material_index = 1  # index of material
        thickness_index = 1  # index of thickness
        mesh_index = 0  # index of meshes
        surf_map = [] # list of nurbs surface

        for i in range(1, len(faces)):
            local_index = 1
            if faces[i].patch.isDeleted:
                continue

            # collect nurbs surface properties
            nurbs_surf = faces[i].patch.nurbs
            if nurbs_surf != []:
                surf_dict = {'degree_u': nurbs_surf.degree_u,
                             'degree_v': nurbs_surf.degree_v,
                             'ctrlpts_size_u': nurbs_surf.ctrlpts_size_u,
                             'ctrlpts_size_v': nurbs_surf.ctrlpts_size_v,
                             'knotvector_u': nurbs_surf.knotvector_u,
                             'knotvector_v': nurbs_surf.knotvector_v
                             }
                surf_map.append(surf_dict)
                             
            mesh_index += 1
            mesh_map = []
            pressure = None

            attributes = faces[i].patch.attributes

            for att in attributes:
                if att['type'] == 'Material':
                    material = att
                    insert = True
                    for mat_dict in materials:
                        if mat_dict["material"] == material:
                            insert = False
                            material_dict = mat_dict
                            break

                    if insert:
                        material_dict = {
                            "material": material,
                            "index": material_index
                        }
                        materials.append(material_dict)
                        material_index += 1

                elif att['type'] == 'Thickness':
                    thickness = att
                    insert = True
                    for thick_dict in thicknesses:
                        if thick_dict["thickness"] == thickness:
                            insert = False
                            thickness_dict = thick_dict
                            break

                    if insert:
                        thickness_dict = {
                            "thickness": thickness,
                            "index": thickness_index
                        }
                        thicknesses.append(thickness_dict)
                        thickness_index += 1

                elif att['type'] == 'Pressure':
                    pressure = att

                if att['type'] == 'Mesh':
                    mesh = att

            mesh_dict = {
                "mesh": mesh,
                "material": material_dict['index'],
                "thickness": thickness_dict['index'],
                "pressure": pressure
            }

            meshes.append(mesh_dict)

            # collect the mesh points
            coords = mesh['coords'].copy()
            if isIsogeometric:
                weights = mesh['IsoGe']['weights'].copy()
            while len(coords) > 0:
                point = Pnt2D(coords[0], coords[1])
                local_index = 1

                insert = True
                for pt_dict in mesh_points:
                    tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)
                    if Pnt2D.equal(pt_dict["point"], point, tol):
                        insert = False
                        pt_dict_target = pt_dict
                        break

                if insert:
                    mesh_point_dict = {
                        "point": point,
                        "mesh_index": mesh_index,
                        "local_index": local_index,
                        "global_index": global_index
                    }

                    if isIsogeometric:
                        mesh_point_dict["weight"] = weights[0]

                    mesh_points.append(mesh_point_dict)
                    global_index += 1

                    # support conditions
                    for sc_point in sc_points:
                        tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)
                        if Pnt2D.equal(sc_point["point"], point, tol):
                        # if sc_point["point"] == point:
                            sc = sc_point["support"]["properties"]
                            mesh_point_dict["support"] = [0, 0, 0]

                            if sc["Dx"]:
                                mesh_point_dict["support"][0] = 1

                            if sc["Dy"]:
                                mesh_point_dict["support"][1] = 1

                            if sc["Rz"]:
                                mesh_point_dict["support"][2] = 1

                            mesh_support_pts.append(mesh_point_dict)
                            sc_points.remove(sc_point)
                            break

                    # concentrated Load
                    for cl_point in cl_points:
                        if cl_point['point'] == point:
                            mesh_point_dict['c_load'] = cl_point['load']
                            mesh_cl_pts.append(mesh_point_dict)
                            cl_points.remove(cl_point)
                            break

                    # uniform load
                    tol = Pnt2D(Curve.COORD_TOL, Curve.COORD_TOL)
                    for ul_segment in ul_segments:

                        if isIsogeometric:
                            pts = ul_segment['segment'].getEquivPolyline()
                            for j in range(len(pts)):
                                if Pnt2D.equal(pts[j], point, tol):
                                    ul_segment['mesh_pts'][j] = mesh_point_dict

                        else:
                            pts = ul_segment['segment'].getEquivPolyline()
                            if Pnt2D.equal(pts[0], point, tol):
                                ul_segment['mesh_pt1'] = mesh_point_dict
                            elif Pnt2D.equal(pts[1], point, tol):
                                ul_segment['mesh_pt2'] = mesh_point_dict

                else:
                    mesh_point_dict = pt_dict_target.copy()
                    mesh_point_dict["mesh_index"] = mesh_index
                    mesh_point_dict["local_index"] = local_index

                mesh_map.append(mesh_point_dict)
                local_index += 1
                coords.pop(0)
                coords.pop(0)
                if isIsogeometric:
                    weights.pop(0)

            meshes_map_pts.append(mesh_map)

        T3 = []
        T6 = []
        Q4 = []
        Q8 = []
        Iso = []

        nel_index = 0  # index of global elements
        mesh_elem = []  # mesh element list
        elem_pressure = []  # list of elements that are under pressure
        copy_meshes_map_pts = meshes_map_pts.copy() # copy of meshes_map_pts
        for mesh in meshes:
            conn = mesh['mesh']['conn'].copy()
            mesh_map = copy_meshes_map_pts.pop(0)

            while len(conn) > 0:
                stop = conn.pop(0)
                elem_type = stop
                step = 0

                elem_con = []
                while step < stop:
                    try:
                        elem_index = mesh_map[conn.pop(0)]['global_index']
                    except:
                        print(conn)
                    if elem_index not in elem_con:
                        elem_con.append(elem_index)
                    else:
                        elem_type -= 1
                    step += 1

                mesh_name = mesh['mesh']['name']
                if mesh_name == "Triangular Boundary C." or mesh_name == "Quadrilateral Seam":
                    elem_con.reverse()

                str_conn = str(elem_con)
                str_conn = str_conn.replace('[', '')
                str_conn = str_conn.replace(']', '')
                str_conn = str_conn.replace(',', '')
                nel_index += 1

                elem_dict = {
                    "type": elem_type,
                    "conn": str_conn,
                    "conn_list": elem_con,
                    "material": mesh['material'],
                    "thickness": mesh["thickness"],
                    "mesh_index": mesh_map[0]['mesh_index'],
                    "index": nel_index
                }

                mesh_elem.append(elem_dict)

                if isIsogeometric:
                    Iso.append(elem_dict)
                elif elem_type == 3:
                    T3.append(elem_dict)
                elif elem_type == 4:
                    Q4.append(elem_dict)
                elif elem_type == 6:
                    T6.append(elem_dict)
                else:
                    Q8.append(elem_dict)

                if mesh['pressure'] is not None:
                    pressure_dict = {
                        "elem_index": nel_index,
                        "pressure": mesh['pressure']
                    }
                    elem_pressure.append(pressure_dict)

        with open(f'{filename}_planeStress.txt', 'w') as file:

            # initial information
            file.write("%HEADER\n")
            file.write("Output file created by FEMEP (version April/2023).\n")
            file.write("'File created by FEMEP program'\n")
            file.write("\n")

            # type of analysis
            file.write("%HEADER.ANALYSIS\n")
            file.write("'plane_stress'\n")
            file.write("\n")

            # analysis method
            file.write("%HEADER.ANALYSIS.METHOD\n")
            if isIsogeometric:
                file.write("'ISOGEOMETRIC'\n")
                file.write("\n")
            else:
                file.write("'ISOPARAMETRIC'\n")
                file.write("\n")

            # number of nodes
            file.write("%NODE\n")
            file.write(f"{len(mesh_points)}\n")
            file.write("\n")

            # node coordinates
            file.write("%NODE.COORD\n")
            file.write(f"{len(mesh_points)}\n")
            for mesh_point in mesh_points:
                file.write(
                    f"{mesh_point['global_index']}   {round(mesh_point['point'].getX(),6):.6f} {round(mesh_point['point'].getY(),6):.6f} {0.000000:.6f}\n")
            file.write("\n")

            # node weights
            if isIsogeometric:
                file.write("%NODE.WEIGHT\n")
                file.write(f"{len(mesh_points)}\n")
                for mesh_point in mesh_points:
                    file.write(
                        f"{mesh_point['global_index']}   {round(mesh_point['weight'],6):.6f}\n")
                file.write("\n")

            # supoort conditions
            file.write("%NODE.SUPPORT\n")
            file.write(f"{len(mesh_support_pts)}\n")

            for mesh_pt in mesh_support_pts:
                file.write(
                    f"{mesh_pt['global_index']}   {mesh_pt['support'][0]} {mesh_pt['support'][1]} 0 0 0 {mesh_pt['support'][2]}\n")
            file.write("\n")

            # material
            file.write("%MATERIAL\n")
            file.write(f"{len(materials)}\n")
            file.write("\n")

            file.write("%MATERIAL.ISOTROPIC\n")
            file.write(f"{len(materials)}\n")
            for i in range(0, len(materials)):
                file.write(
                    f"{i+1}   {round(materials[i]['material']['properties']['YoungsModulus'],6):.1f} {round(materials[i]['material']['properties']['PoisonsRatio'],6):.6f}\n")
            file.write("\n")

            file.write("%THICKNESS\n")
            file.write(f"{len(thicknesses)}\n")
            for i in range(0, len(thicknesses)):
                file.write(
                    f"{i+1}   {round(thicknesses[i]['thickness']['properties']['Value'],6):.6f}\n")
            file.write("\n")

            # Integration order
            file.write("%INTEGRATION.ORDER\n")
            file.write(f"4\n")

            # T3
            if _gpT3 == "1":
                file.write(f"{1} 1 1 1 1 1 1\n")
            else:
                file.write(f"{1} 3 3 1 3 3 1\n")

            # T6
            file.write(f"{2} 3 3 1 3 3 1\n")

            # Q4
            if _gpQ4 == "1x1":
                file.write(f"{3} 1 1 1 1 1 1\n")
            elif _gpQ4 == "2x2":
                file.write(f"{3} 2 2 1 2 2 1\n")
            else:
                file.write(f"{3} 3 3 1 3 3 1\n")

            # Q8
            file.write(f"{4} 2 2 1 2 2 1\n")
            file.write("\n")

            # surface
            if isIsogeometric:
                file.write("%SURFACE\n")
                file.write(f"{len(surf_map)}\n")
                file.write("\n")

                # surface degrees
                file.write("%SURFACE.DEGREE\n")
                for i in range(len(surf_map)):
                    file.write(f"{i+1}   {surf_map[i]['degree_u']} {surf_map[i]['degree_v']}\n")
                file.write("\n")

                # surface knot vectors
                file.write("%SURFACE.KNOTVECTOR\n")
                for i in range(len(surf_map)):

                    knotvector_u = ''
                    for knot in surf_map[i]['knotvector_u']:
                        knotvector_u += str(round(knot,6)) + ' '
                    knotvector_u = knotvector_u[:-1]

                    knotvector_v = ''
                    for knot in surf_map[i]['knotvector_v']:
                        knotvector_v += str(round(knot,6)) + ' '
                    knotvector_v = knotvector_v[:-1]

                    file.write(f"{i+1}   {len(surf_map[i]['knotvector_u'])}   {knotvector_u}   {len(surf_map[i]['knotvector_v'])}   {knotvector_v}\n")
                file.write("\n")

                # surface control net
                file.write("%SURFACE.CTRLNET\n")
                copy_meshes_map_pts = meshes_map_pts.copy()
                for i in range(len(copy_meshes_map_pts)):
                    file.write(f"{i+1}\n")
                    Nu = surf_map[i]['ctrlpts_size_u']
                    Nv = surf_map[i]['ctrlpts_size_v']
                    for j in range(Nv):
                        for k in range(Nu):
                            file.write(f"{copy_meshes_map_pts[i][0]['global_index']}  ")
                            copy_meshes_map_pts[i].pop(0)
                        file.write("\n")
                file.write("\n")

            # elements
            file.write("%ELEMENT\n")
            file.write(f"{nel_index}\n")
            file.write("\n")

            index = 0
            if len(Iso) > 0:
                file.write("%ELEMENT.ISOGEOMETRIC\n")
                for i in range(len(surf_map)):
                    uniqueKnotVectorU = sorted(set(surf_map[i]['knotvector_u']))
                    uniqueKnotVectorV = sorted(set(surf_map[i]['knotvector_v']))
                    NelemU = len(uniqueKnotVectorU) - 1
                    NelemV = len(uniqueKnotVectorV) - 1
                    Nelem = NelemU * NelemV
                    # Nelem = (len(set(surf_map[i]['knotvector_u'])) - 1) * (len(set(surf_map[i]['knotvector_v'])) - 1)
                    file.write(f"{i+1}   {Nelem}\n")
                    for j in range(NelemV):
                        for k in range(NelemU):
                            file.write(f"{Iso[index]['index']}   {Iso[index]['material']} {Iso[index]['thickness']} {4}   {len(Iso[index]['conn_list'])}   {Iso[index]['conn']}   {round(uniqueKnotVectorU[0],6)} {round(uniqueKnotVectorU[1],6)}   {round(uniqueKnotVectorV[0],6)} {round(uniqueKnotVectorV[1],6)}\n")
                            index += 1
                            uniqueKnotVectorU.pop(0)
                        uniqueKnotVectorU = sorted(set(surf_map[i]['knotvector_u']))
                        uniqueKnotVectorV.pop(0)
            file.write("\n")

            if len(T3) > 0:
                file.write("%ELEMENT.T3\n")
                file.write(f"{len(T3) }\n")

                for elem in T3:
                    file.write(
                        f"{elem['index']}   {elem['material']} {elem['thickness']} {1} {elem['conn']}\n")
                    nel_index += 1
                file.write("\n")

            if len(T6) > 0:
                file.write("%ELEMENT.T6\n")
                file.write(f"{len(T6) }\n")

                for elem in T6:
                    file.write(
                        f"{elem['index']}   {elem['material']} {elem['thickness']} {2} {elem['conn']}\n")
                    nel_index += 1
                file.write("\n")

            if len(Q4) > 0:
                file.write("%ELEMENT.Q4\n")
                file.write(f"{len(Q4)}\n")

                for elem in Q4:
                    file.write(
                        f"{elem['index']}   {elem['material']} {elem['thickness']} {3} {elem['conn']}\n")
                    nel_index += 1

                file.write("\n")

            if len(Q8) > 0:
                file.write("%ELEMENT.Q8\n")
                file.write(f"{len(Q8)}\n")

                for elem in Q8:
                    file.write(
                        f"{elem['index']}   {elem['material']} {elem['thickness']} {4} {elem['conn']}\n")
                    nel_index += 1

                file.write("\n")

            # load
            file.write("%LOAD\n")
            file.write("1\n")
            file.write("1	'Load_Case_1'\n")
            file.write("\n")

            file.write("%LOAD.CASE\n")
            file.write("1\n")
            file.write("\n")

            # nodal loads
            if len(mesh_cl_pts) > 0:
                file.write("%LOAD.CASE.NODAL.FORCES\n")
                file.write(f"{len(mesh_cl_pts)}\n")

                for mesh_point in mesh_cl_pts:
                    file.write(
                        f"{mesh_point['global_index']} {mesh_point['c_load']['properties']['Fx']:.6f}	{mesh_point['c_load']['properties']['Fy']:.6f} 0.000000 0.000000 0.000000 {mesh_point['c_load']['properties']['Mz']:.6f}\n")

                file.write("\n")

            # uniform load
            ul_quadraticElem = []  # list of quadratic elem with uniform load
            string_loads = []
            if len(ul_segments) > 0:
                if isIsogeometric:
                    count_load_elems = 0
                    file.write("%LOAD.CASE.LINE.FORCE.UNIFORM\n")
                    for ul_segment in ul_segments:
                        Qx = ul_segment['load'][0]
                        Qy = ul_segment['load'][1]
                        pts_dicts_list = ul_segment['mesh_pts']
                        pts_index = [pts["global_index"] for pts in pts_dicts_list]
                        for elem in Iso:
                            surf_index = elem['mesh_index'] - 1
                            NuElem = surf_map[surf_index]['degree_u'] + 1
                            NvElem = surf_map[surf_index]['degree_v'] + 1
                            conn = np.array(elem['conn_list'])
                            conn_matrix = np.array(conn).reshape((NvElem, NuElem))
                            
                            row_in_matrix = np.where(np.all(np.isin(conn_matrix, pts_index), axis=1))[0].tolist()
                            column_in_matrix = np.where(np.all(np.isin(conn_matrix, pts_index), axis=0))[0].tolist()

                            if len(row_in_matrix) > 0:
                                row = conn_matrix[row_in_matrix[0],:]
                                index_pt1 = row[0]
                                index_pt2 = row[-1]
                                string_loads.append(f"{elem['index']}   {index_pt1} {index_pt2}   0   {Qx:.6f} {Qy:.6f} 0.000000")
                                count_load_elems += 1

                            if len(column_in_matrix) > 0:
                                column = conn_matrix[:,column_in_matrix[0]]
                                index_pt1 = column[-1]
                                index_pt2 = row[0]
                                string_loads.append(f"{elem['index']}   {index_pt1} {index_pt2}   0   {Qx:.6f} {Qy:.6f} 0.000000")
                                count_load_elems += 1

                    file.write(f"{count_load_elems}\n")
                    for load in string_loads:
                        file.write(f"{load}\n")
                    file.write("\n")

                else:
                    for ul_segment in ul_segments:
                        index_pt1 = ul_segment['mesh_pt1']['global_index']
                        index_pt2 = ul_segment['mesh_pt2']['global_index']
                        Qx = ul_segment['load'][0]
                        Qy = ul_segment['load'][1]
                        for elem in mesh_elem:
                            if index_pt1 in elem['conn_list'] and index_pt2 in elem['conn_list']:
                                elem_target = elem
                                elem_index = elem['index']
                                break

                        if elem_target['type'] == 6 or elem_target['type'] == 8:
                            ul_quadraticElem.append([ul_segment, elem_target])
                            continue

                        string_loads.append(
                            f"{elem_index}	{index_pt1}	{index_pt2}	0	{Qx:.6f}	{Qy:.6f}	0.000000")

                    len_quadricElem = len(ul_quadraticElem)
                    while len(ul_quadraticElem) > 0:
                        quadElem1 = ul_quadraticElem.pop(0)
                        quadElem2 = ul_quadraticElem.pop(0)
                        index_pt1 = quadElem1[0]['mesh_pt1']['global_index']
                        index_pt2 = quadElem2[0]['mesh_pt2']['global_index']
                        Qx = quadElem1[0]['load'][0]
                        Qy = quadElem2[0]['load'][1]
                        elem_index = quadElem1[1]['index']

                        string_loads.append(
                            f"{elem_index}	{index_pt1}	{index_pt2}	0	{Qx:.6f}	{Qy:.6f}	0.000000")

                    file.write("%LOAD.CASE.LINE.FORCE.UNIFORM\n")
                    file.write(f"{int(len(ul_segments)-len_quadricElem/2)}\n")
                    for load in string_loads:
                        file.write(f"{load}\n")
                    file.write("\n")

            if len(elem_pressure) > 0:
                file.write("%LOAD.CASE.DOMAIN.FORCE.UNIFORM\n")
                file.write(f"{len(elem_pressure)}\n")
                for elem in elem_pressure:
                    elem_index = elem['elem_index']
                    Px = elem['pressure']['properties']['Px']
                    Py = elem['pressure']['properties']['Py']
                    file.write(f"{elem_index}	{Px:.6f}	{Py:.6f}	0.000000\n")
                file.write("\n")

            file.write("%END")

    def exportFileToTFemoolabPlaneConduction(_shell, _filename, _gpT3, _gpT6, _gpQ4, _qpQ8):
        # create/ open a file
        split_name = _filename.split('.')
        if split_name[-1] == 'json':
            filename = split_name[0]
        else:
            filename = _filename

        faces = _shell.faces
        edges = _shell.edges
        vertices = _shell.vertices

        # the faces of the solid must be connected
        if len(_shell.face.intLoops) > 1:
            raise Error

        nt_points = []  # points that have nodal temperature
        uf_segments = []  # segments that have uniform flux
        for edge in edges:
            attributes = edge.segment.attributes
            temperature = None
            number_subdv = None
            uniform_flux = None
            isQuadratic = False
            incidentFaces = edge.incidentFaces()

            for face in incidentFaces:
                if face.patch.mesh is not None:
                    mesh_dict = face.patch.mesh.mesh_dict
                    if mesh_dict['properties']['Element type'] == "T6" or mesh_dict['properties']['Element type'] == "Q8":
                        isQuadratic = True

            for att in attributes:
                if att['type'] == "Temperature":
                    temperature = att
                elif att["type"] == "Uniform Heat Flux":
                    uniform_flux = att
                elif att["type"] == "Number of Subdivisions":
                    number_subdv = att

            if temperature is not None:
                subdv_pts = HeFile.Nsbdvs(
                    number_subdv, edge.segment, isQuadratic)

                for pt in subdv_pts:
                    nt_point = {
                        "point": pt,
                        "temperature": temperature
                    }
                    nt_points.append(nt_point)

            if uniform_flux is not None:

                flux = uniform_flux['properties']['Value']

                if number_subdv is not None:
                    subdv_pts = HeFile.Nsbdvs(
                        number_subdv, edge.segment, isQuadratic)
                    edge_pts = edge.segment.getPoints()
                    subdv_pts.insert(0, edge_pts[0])
                    subdv_pts.append(edge_pts[-1])

                    while len(subdv_pts) > 1:
                        seg = Line(subdv_pts.pop(0), subdv_pts[0])

                        uf_segment = {
                            "segment": seg,
                            "flux": flux,
                            "mesh_pt1": None,
                            "mesh_pt2": None
                        }
                        uf_segments.append(uf_segment)
                else:
                    uf_segment = {
                        "segment": edge.segment,
                        "flux": flux,
                        "mesh_pt1": None,
                        "mesh_pt2": None
                    }
                    uf_segments.append(uf_segment)

        nf_points = []  # points that have nodal flux
        for vertex in vertices:
            attributes = vertex.point.attributes

            for att in attributes:
                if att["type"] == "Temperature":
                    nt_point = {
                        "point": vertex.point,
                        "temperature": att
                    }
                    nt_points.append(nt_point)

                elif att["type"] == "Nodal Heat Flux":
                    nf_point = {
                        "point": vertex.point,
                        "flux": att
                    }
                    nf_points.append(nf_point)

        # it is not possible to export a model without support conditions
        if len(nt_points) == 0:
            raise Error

        # get information
        meshes = []  # list of meshes
        mesh_points = []  # list of all points in the global mesh
        meshes_map_pts = []  # set of points in each local mesh
        mesh_nt_pts = []  # list of points with nodal temperature
        mesh_nf_pts = []  # list of points with nodal flux
        materials = []  # list of materials
        thicknesses = []  # list of thicknesses
        global_index = 1  # global index of points
        material_index = 1  # index of material
        thickness_index = 1  # index of thickness
        mesh_index = 0  # index of meshes

        for i in range(1, len(faces)):

            if faces[i].patch.isDeleted:
                continue

            mesh_index += 1
            local_index = 1
            mesh_map = []
            inner_flux = None
            temperature = None

            attributes = faces[i].patch.attributes

            for att in attributes:
                if att['type'] == 'Material':
                    material = att
                    insert = True
                    for mat_dict in materials:
                        if mat_dict["material"] == material:
                            insert = False
                            material_dict = mat_dict
                            break

                    if insert:
                        material_dict = {
                            "material": material,
                            "index": material_index
                        }
                        materials.append(material_dict)
                        material_index += 1

                elif att['type'] == 'Thickness':
                    thickness = att
                    insert = True
                    for thick_dict in thicknesses:
                        if thick_dict["thickness"] == thickness:
                            insert = False
                            thickness_dict = thick_dict
                            break

                    if insert:
                        thickness_dict = {
                            "thickness": thickness,
                            "index": thickness_index
                        }
                        thicknesses.append(thickness_dict)
                        thickness_index += 1

                elif att['type'] == 'Inner Heat Flux':
                    inner_flux = att

                elif att['type'] == 'Temperature':
                    temperature = att

                if att['type'] == 'Mesh':
                    mesh = att

            mesh_dict = {
                "mesh": mesh,
                "material": material_dict['index'],
                "thickness": thickness_dict['index'],
                "inner_flux": inner_flux
            }

            meshes.append(mesh_dict)

            # collect the mesh points
            coords = mesh['coords'].copy()
            while len(coords) > 0:
                point = Point(coords[0], coords[1])
                local_index = 1

                insert = True
                for pt_dict in mesh_points:
                    if pt_dict["point"] == point:
                        insert = False
                        pt_dict_target = pt_dict
                        break

                if insert:
                    mesh_point_dict = {
                        "point": point,
                        "mesh_index": mesh_index,
                        "local_index": local_index,
                        "global_index": global_index
                    }
                    mesh_points.append(mesh_point_dict)
                    global_index += 1

                    # temperature
                    for nt_point in nt_points:
                        if nt_point['point'] == point:
                            mesh_point_dict['nt_load'] = nt_point['temperature']
                            mesh_nt_pts.append(mesh_point_dict)
                            nt_points.remove(nt_point)
                            break

                    if temperature is not None:
                        if mesh_point_dict not in mesh_nt_pts:
                            mesh_point_dict['nt_load'] = temperature
                            mesh_nt_pts.append(mesh_point_dict)

                    # nodal flux
                    for nf_point in nf_points:
                        if nf_point['point'] == point:
                            mesh_point_dict['nf_load'] = nf_point['flux']
                            mesh_nf_pts.append(mesh_point_dict)
                            nf_points.remove(nf_point)
                            break

                    # uniform flux
                    tol = Point(0.01, 0.01)
                    for uf_segment in uf_segments:
                        pts = uf_segment['segment'].getPoints()
                        if point.equal(pts[0], tol):
                            uf_segment['mesh_pt1'] = mesh_point_dict
                        elif point.equal(pts[1], tol):
                            uf_segment['mesh_pt2'] = mesh_point_dict

                else:
                    mesh_point_dict = pt_dict_target.copy()
                    mesh_point_dict["mesh_index"] = mesh_index
                    mesh_point_dict["local_index"] = local_index

                mesh_map.append(mesh_point_dict)
                local_index += 1
                coords.pop(0)
                coords.pop(0)

            meshes_map_pts.append(mesh_map)

        T3 = []
        T6 = []
        Q4 = []
        Q8 = []

        nel_index = 0  # index of global elements
        mesh_elem = []  # mesh element list
        elem_flux = []  # list of elements that are under inner flux
        for mesh in meshes:
            conn = mesh['mesh']['conn'].copy()
            mesh_map = meshes_map_pts.pop(0)

            while len(conn) > 0:
                stop = conn.pop(0)
                elem_type = stop
                step = 0

                elem_con = []
                while step < stop:
                    elem_index = mesh_map[conn.pop(0)]['global_index']
                    if elem_index not in elem_con:
                        elem_con.append(elem_index)
                    else:
                        elem_type -= 1
                    step += 1

                mesh_name = mesh['mesh']['name']
                if mesh_name == "Triangular Boundary C." or mesh_name == "Quadrilateral Seam":
                    elem_con.reverse()

                str_conn = str(elem_con)
                str_conn = str_conn.replace('[', '')
                str_conn = str_conn.replace(']', '')
                str_conn = str_conn.replace(',', '')
                nel_index += 1

                elem_dict = {
                    "type": elem_type,
                    "conn": str_conn,
                    "conn_list": elem_con,
                    "material": mesh['material'],
                    "thickness": mesh["thickness"],
                    "mesh_index": mesh_map[0]['mesh_index'],
                    "index": nel_index
                }

                mesh_elem.append(elem_dict)

                if elem_type == 3:
                    T3.append(elem_dict)
                elif elem_type == 4:
                    Q4.append(elem_dict)
                elif elem_type == 6:
                    T6.append(elem_dict)
                else:
                    Q8.append(elem_dict)

                if mesh['inner_flux'] is not None:
                    inner_flux_dict = {
                        "elem_index": nel_index,
                        "inner_flux": mesh['inner_flux']
                    }
                    elem_flux.append(inner_flux_dict)

        with open(f'{filename}_planeConduction.txt', 'w') as file:

            # initial information
            file.write("%HEADER\n")
            file.write("Output file created by FEMEP (version October/2021).\n")
            file.write("'File created by FEMEP program'\n")
            file.write("\n")

            # type of analysis
            file.write("%HEADER.ANALYSIS\n")
            file.write("'plane_conduction'\n")
            file.write("\n")

            # number of nodes
            file.write("%NODE\n")
            file.write(f"{len(mesh_points)}\n")
            file.write("\n")

            # node coordinates
            file.write("%NODE.COORD\n")
            file.write(f"{len(mesh_points)}\n")
            for mesh_point in mesh_points:
                file.write(
                    f"{mesh_point['global_index']} {round(mesh_point['point'].getX(),6):.6f} {round(mesh_point['point'].getY(),6):.6f} {0.000000:.6f}\n")
            file.write("\n")

            # material
            file.write("%MATERIAL\n")
            file.write(f"{len(materials)}\n")
            file.write("\n")

            file.write("%MATERIAL.PROPERTY.THERMAL\n")
            file.write(f"{len(materials)}\n")
            for i in range(0, len(materials)):
                file.write(
                    f"{i+1} {round(materials[i]['material']['properties']['Conductivity'],6):.6f} {round(materials[i]['material']['properties']['SpecificHeat'],6):.6f}\n")
            file.write("\n")

            file.write("%THICKNESS\n")
            file.write(f"{len(thicknesses)}\n")
            for i in range(0, len(thicknesses)):
                file.write(
                    f"{i+1} {round(thicknesses[i]['thickness']['properties']['Value'],6):.6f}\n")
            file.write("\n")

            # Integration order
            file.write("%INTEGRATION.ORDER\n")
            file.write(f"4\n")

            # T3
            if _gpT3 == "1":
                file.write(f"{1} 1 1 1 1 1 1\n")
            else:
                file.write(f"{1} 3 3 1 3 3 1\n")

            # T6
            file.write(f"{2} 3 3 1 3 3 1\n")

            # Q4
            if _gpQ4 == "1x1":
                file.write(f"{3} 1 1 1 1 1 1\n")
            elif _gpQ4 == "2x2":
                file.write(f"{3} 2 2 1 2 2 1\n")
            else:
                file.write(f"{3} 3 3 1 3 3 1\n")

            # Q8
            file.write(f"{4} 2 2 1 2 2 1\n")
            file.write("\n")

            # elements
            file.write("%ELEMENT\n")
            file.write(f"{nel_index}\n")
            file.write("\n")

            if len(T3) > 0:
                file.write("%ELEMENT.T3\n")
                file.write(f"{len(T3) }\n")

                for elem in T3:
                    file.write(
                        f"{elem['index']} {elem['material']} {elem['thickness']} 1 {elem['conn']}\n")
                    nel_index += 1
                file.write("\n")

            if len(T6) > 0:
                file.write("%ELEMENT.T6\n")
                file.write(f"{len(T6) }\n")

                for elem in T6:
                    file.write(
                        f"{elem['index']} {elem['material']} {elem['thickness']} 2 {elem['conn']}\n")
                    nel_index += 1
                file.write("\n")

            if len(Q4) > 0:
                file.write("%ELEMENT.Q4\n")
                file.write(f"{len(Q4)}\n")

                for elem in Q4:
                    file.write(
                        f"{elem['index']} {elem['material']} {elem['thickness']} 3 {elem['conn']}\n")
                    nel_index += 1

                file.write("\n")

            if len(Q8) > 0:
                file.write("%ELEMENT.Q8\n")
                file.write(f"{len(Q8)}\n")

                for elem in Q8:
                    file.write(
                        f"{elem['index']} {elem['material']} {elem['thickness']} 4 {elem['conn']}\n")
                    nel_index += 1

                file.write("\n")

            # nodal loads
            if len(mesh_nt_pts) > 0:
                file.write("%LOAD.CASE.NODAL.TEMPERATURE\n")
                file.write(f"{len(mesh_nt_pts)}\n")

                for mesh_point in mesh_nt_pts:
                    file.write(
                        f"{mesh_point['global_index']} {mesh_point['nt_load']['properties']['Value']:.6f}\n")

                file.write("\n")

            if len(mesh_nf_pts) > 0:
                file.write("%LOAD.CASE.NODAL.FLUX\n")
                file.write(f"{len(mesh_nf_pts)}\n")

                for mesh_point in mesh_nf_pts:
                    file.write(
                        f"{mesh_point['global_index']} {mesh_point['nf_load']['properties']['Value']:.6f}\n")

                file.write("\n")

            # uniform flux
            uf_quadraticElem = []  # list of quadratic elem with uniform flux
            string_loads = []
            if len(uf_segments) > 0:
                for uf_segment in uf_segments:
                    index_pt1 = uf_segment['mesh_pt1']['global_index']
                    index_pt2 = uf_segment['mesh_pt2']['global_index']
                    flux = uf_segment['flux']

                    for elem in mesh_elem:
                        if index_pt1 in elem['conn_list'] and index_pt2 in elem['conn_list']:
                            elem_target = elem
                            elem_index = elem['index']
                            break

                    if elem_target['type'] == 6 or elem_target['type'] == 8:
                        uf_quadraticElem.append([uf_segment, elem_target])
                        continue

                    string_loads.append(
                        f"{elem_index} {index_pt1} {index_pt2} {flux:.6f}")

                len_quadricElem = len(uf_quadraticElem)
                while len(uf_quadraticElem) > 0:
                    quadElem1 = uf_quadraticElem.pop(0)
                    quadElem2 = uf_quadraticElem.pop(0)
                    index_pt1 = quadElem1[0]['mesh_pt1']['global_index']
                    index_pt2 = quadElem2[0]['mesh_pt2']['global_index']
                    flux = quadElem1[0]['flux']['properties']['Value']
                    elem_index = quadElem1[1]['index']

                    string_loads.append(
                        f"{elem_index} {index_pt1} {index_pt2} {flux:.6f}")

                file.write("%LOAD.CASE.LINE.HEAT.FLUX.UNIFORM\n")
                file.write(f"{int(len(uf_segments)-len_quadricElem/2)}\n")
                for load in string_loads:
                    file.write(f"{load}\n")
                file.write("\n")

            # inner flux
            if len(elem_flux) > 0:
                file.write("%LOAD.CASE.AREA.HEAT.FLUX.UNIFORM\n")
                file.write(f"{len(elem_flux)}\n")
                for elem in elem_flux:
                    elem_index = elem['elem_index']
                    flux = elem['inner_flux']['properties']['Value']
                    file.write(f"{elem_index}	{flux:.6f}\n")
                file.write("\n")

            file.write("%END")

    def Nsbdvs(_attribute, _seg, _isQuadratic, _isIsogeometric):
        points = []

        if _attribute is not None:
            properties = _attribute['properties']
            number = properties['Value']
            ratio = properties['Ratio']

            if _isIsogeometric:
                ctrlpts = _seg.getCtrlPts().copy()
                ctrlpts.pop(0)
                ctrlpts.pop()
                for ctrlpt in ctrlpts:
                    points.append(Pnt2D(ctrlpt[0], ctrlpt[1]))
            else:
                points = Mesh1D.subdivideSegment(_seg, number, ratio, _isQuadratic)

        return points

    def getUniformLoadGlobalValues(_attribute, _segment):
        properties = _attribute['properties']
        points = _segment.getPoints()
        v = points[1] - points[0]
        local_Qx = properties['Qx']
        local_Qy = properties['Qy']
        global_Qx = 0
        global_Qy = 0

        ang = AttribSymbols.getAngWithXDirec(v)
        ang = ang*math.pi/180
        sin = math.sin(ang)
        cos = math.cos(ang)

        tol = 1e-7
        if points[1].getY() < points[0].getY():

            if abs(cos) <= tol:
                global_Qx += local_Qy*sin
            else:
                global_Qx += local_Qy*sin/abs(cos) + local_Qx*cos/abs(cos)

            if abs(sin) <= tol:
                global_Qy += local_Qy*cos
            else:
                global_Qy += local_Qy*cos/abs(sin) - local_Qx*sin/abs(sin)
        else:
            if abs(cos) <= tol:
                global_Qx += -local_Qy*sin
            else:
                global_Qx += -local_Qy*sin/abs(cos) + local_Qx*cos/abs(cos)

            if abs(sin) <= tol:
                global_Qy += local_Qy*cos
            else:
                global_Qy += local_Qy*cos/abs(sin) + local_Qx*sin/abs(sin)

        return [global_Qx, global_Qy]
