from compgeom.compgeom import CompGeom
from compgeom.pnt2d import Pnt2D
from geometry.point import Point
from geometry.curves.polyline import Polyline
from geometry.segment import Segment
from geometry.curves.curve import Curve


class HeModel:

    def __init__(self):
        self.shell = None
        self.infinityFace = None
        self.segments = []
        self.points = []
        self.patches = []
        self.updateSortPatches = False

    def insertShell(self, _shell):
        self.shell = _shell

    def insertVertex(self, _vertex):
        self.shell.insertVertex(_vertex)
        self.points.append(_vertex.point)
        _vertex.point.vertex = _vertex

    def insertEdge(self, _edge):
        self.shell.insertEdge(_edge)
        self.segments.append(_edge.segment)
        _edge.segment.edge = _edge

    def insertFace(self, _face):

        if len(self.shell.faces) == 0:
            self.infinityFace = _face

        self.shell.insertFace(_face)
        _face.patch.face = _face
        self.updateSortPatches = True

    def removeVertex(self, _vertex):
        _vertex.point.vertex = None
        self.shell.removeVertex(_vertex)
        self.points.remove(_vertex.point)

    def removeFace(self, _face):
        if _face == self.infinityFace:
            self.infinityFace = None

        self.shell.removeFace(_face)
        _face.patch.face = None
        self.updateSortPatches = True

    def removeEdge(self, _edge):
        self.shell.removeEdge(_edge)
        self.segments.remove(_edge.segment)
        _edge.segment.edge = None

    def removeShell(self):
        self.shell = None

    def isEmpty(self):
        if self.shell is None:
            return True
        else:
            return False

    def clearAll(self):
        self.shell = None
        self.infinityFace = None
        self.segments = []
        self.points = []
        self.patches = []

    def getPoints(self):
        return self.points

    def getSegments(self):
        return self.segments

    def getPatches(self):
        if not self.isEmpty():
            if self.updateSortPatches:
                self.patches = self.sortPatches()

        return self.patches

    def selectedEdges(self):
        selectedEdges = []

        if self.isEmpty():
            return selectedEdges

        edges = self.shell.edges
        for edge in edges:
            if edge.segment.isSelected():
                selectedEdges.append(edge)

        return selectedEdges

    def selectedVertices(self):

        selectedVertices = []

        if self.isEmpty():
            return selectedVertices

        vertices = self.shell.vertices
        for vertex in vertices:
            if vertex.point.isSelected():
                selectedVertices.append(vertex)

        return selectedVertices

    def selectedFaces(self):

        selectedFaces = []
        if self.isEmpty():
            return selectedFaces

        faces = self.shell.faces
        for face in faces:
            if face.patch.isSelected():
                selectedFaces.append(face)

        return selectedFaces

    def verticesCrossingWindow(self, _xmin, _xmax, _ymin, _ymax):
        vertices = []
        # search the points that are contained in the given rectangle
        vertices_list = self.shell.vertices
        for vertex in vertices_list:
            if _xmin <= vertex.point.getX() and _xmax >= vertex.point.getX():
                if _ymin <= vertex.point.getY() and _ymax >= vertex.point.getY():
                    # then point is in window
                    vertices.append(vertex)

        vertices = list((vertices))

        return vertices

    def edgesInWindow(self, _xmin, _xmax, _ymin, _ymax):

        edges_targets = []

        # search the edges that are contained in the given rectangle
        edges_list = self.shell.edges
        for edge in edges_list:
            edge_segment = edge.segment
            edg_xmin, edg_xmax, edg_ymin, edg_ymax = edge_segment.getBoundBox()

            if _xmin <= edg_xmin and _xmax >= edg_xmax:
                if _ymin <= edg_ymin and _ymax >= edg_ymax:
                    # then the edge is in window
                    edges_targets.append(edge)

        return edges_targets

    def edgesCrossingFence(self, _xmin, _xmax, _ymin, _ymax, _tol):
        edges_targets = []

        pts = []
        if _ymin == _ymax or _xmin == _xmax:
            pts.append(Pnt2D(_xmin, _ymin))
            pts.append(Pnt2D(_xmax, _ymax))
        else:
            # create a retangular fence
            pts.append(Pnt2D(_xmin, _ymin))
            pts.append(Pnt2D(_xmax, _ymin))
            pts.append(Pnt2D(_xmax, _ymax))
            pts.append(Pnt2D(_xmin, _ymax))
            pts.append(Pnt2D(_xmin, _ymin))
        fencePoly = Polyline(pts)

        # get segments crossing fence's bounding box
        edges_list = self.shell.edges
        for edge in edges_list:
            segment = edge.segment
            segment_xmin, segment_xmax, segment_ymin, segment_ymax = segment.getBoundBox()

            if not (_xmax < segment_xmin or segment_xmax < _xmin or
                    _ymax < segment_ymin or segment_ymax < _ymin):
                edges_targets.append(edge)

        # Checks if the segment intersects the _fence
        for edge in edges_targets:
            edgePolyline = Polyline(edge.segment.getPoints())
            status = self.chkIntersectPolylines(fencePoly, edgePolyline, _tol)

            # If it does not, remove the edge from edgesInFence and go to next edge
            if not status:
                edges_targets.remove(edge)

        return edges_targets

    def edgesCrossingWindow(self, _xmin, _xmax, _ymin, _ymax, _tol):

        edges = self.edgesInWindow(_xmin, _xmax, _ymin, _ymax)

        edges_crossing = self.edgesCrossingFence(_xmin, _xmax, _ymin, _ymax, _tol)
        edges.extend(edges_crossing)

        edges = list(set(edges))  # remove duplicates

        return edges

    def whichFace(self, _pt):
        face = self.infinityFace.next

        while face is not None:
            if face.patch.isPointInside(_pt):
                return face

            face = face.next

        return self.infinityFace

    def sortPatches(self):
        patchesWithoutHoles = []
        facesWithHoles = []

        # initially the faces are organized in two lists of faces with holes
        #  and patches without holes
        faces = self.shell.faces
        for i in range(1, len(faces)):
            if len(faces[i].patch.holes) > 0:
                facesWithHoles.append(faces[i])
            else:
                patchesWithoutHoles.append(faces[i].patch)

        sort_patches = []

        # From this point on, the list of faces with holes is searched looking
        #  for the outermost face. Then the outermost face is added to the new
        #  list of patches with holes
        while len(facesWithHoles) > 0:
            insert = True
            face_target = facesWithHoles[0]
            for j in range(1, len(facesWithHoles)):
                face_point = face_target.loop.he.vertex.point
                poly = facesWithHoles[j].patch.getPoints()

                if CompGeom.isPointInPolygon(poly, face_point):
                    insert = False
                    break

            if insert:
                sort_patches.append(face_target.patch)
                facesWithHoles.pop(0)
            else:
                facesWithHoles.pop(0)
                facesWithHoles.append(face_target)

        sort_patches.extend(patchesWithoutHoles)

        self.updateSortPatches = False

        return sort_patches

    def chkIntersectPolylines(self, _polylineA, _polylineB, _tol):

        polyptsA = _polylineA.getCtrlPoints()
        polyptsB = _polylineB.getCtrlPoints()

        # In case the given tolerance is positive, attract the endpoints of
        # each polyline to the other polyline (within the given tolerance).
        status, clstPt, dmin, t, tang = _polylineB.closestPoint(polyptsA[0].getX(), polyptsA[0].getY())
        if status:
            if dmin <= _tol:
                polyptsA[0].setX(clstPt.getX())
                polyptsA[0].setY(clstPt.getY())
        status, clstPt, dmin, t, tang = _polylineB.closestPoint(polyptsA[-1].getX(), polyptsA[-1].getY())
        if status:
            if dmin <= _tol:
                polyptsA[-1].setX(clstPt.getX())
                polyptsA[-1].setY(clstPt.getY())
        status, clstPt, dmin, t, tang = _polylineA.closestPoint(polyptsB[0].getX(), polyptsB[0].getY())
        if status:
            if dmin <= _tol:
                polyptsB[0].setX(clstPt.getX())
                polyptsB[0].setY(clstPt.getY())
        status, clstPt, dmin, t, tang = _polylineA.closestPoint(polyptsB[-1].getX(), polyptsB[-1].getY())
        if status:
            if dmin <= _tol:
                polyptsB[-1].setX(clstPt.getX())
                polyptsB[-1].setY(clstPt.getY())

        # Perform intersection of the two polylines.
        status, intersPts, parsA, parsB, overlap = CompGeom.computePolyPolyIntersection(
                                                               polyptsA, polyptsB)
        return status

    def intersectSegments(self, _segA, _segB, _tol):
        # Get the owning curves and polyline of each given segment.
        curveA = _segA.curve
        curveB = _segB.curve
        polyptsA = _segA.getPoints()
        polyptsB = _segB.getPoints()

        # It is assumed that segment _segB is the one being inserted.
        # Attract the endpoints of polyline B to the polyline A
        # (within the given tolerance). This is done because the 
        # intersections of the two segments are found first based
        # on the intersection of the polylines of the two segments.
        polylineA = Polyline(polyptsA)
        status, clstPt, dmin, t, tang = polylineA.closestPoint(polyptsB[0].getX(), polyptsB[0].getY())
        if status:
            if dmin <= _tol:
                polyptsB[0].setX(clstPt.getX())
                polyptsB[0].setY(clstPt.getY())
        status, clstPt, dmin, t, tang = polylineA.closestPoint(polyptsB[-1].getX(), polyptsB[-1].getY())
        if status:
            if dmin <= _tol:
                polyptsB[-1].setX(clstPt.getX())
                polyptsB[-1].setY(clstPt.getY())

        # Perform intersection of the two polylines.
        # The function CompGeom.computePolyPolyIntersection computes the intersection
        # point coordinates and the polyline parametric values along the two segments.
        # These parametric values range from 0.0 to 1.0 in each polyline and correspond
        # to the ratio between the polyline arc length of the intersection point and
        # the total polyline length.
        # In the sequence, these parametric values will be computed on the owning
        # curve parametric representation (if there is one) of each segment.
        status, intersPts, parsA, parsB, overlap = CompGeom.computePolyPolyIntersection(
                                                               polyptsA, polyptsB)
        if not status:
            return False, intersPts, parsA, parsB

        numIntersPts = len(intersPts)

        if curveA is not None:
            for i in range (0, numIntersPts):
                StA, clstPt, dmin, parsA[i], tang = curveA.closestPointParam(intersPts[i].getX(), intersPts[i].getY(), parsA[i])

        if curveB is not None:
            for i in range (0, numIntersPts):
                StB, clstPt, dmin, parsB[i], tang = curveB.closestPointParam(intersPts[i].getX(), intersPts[i].getY(), parsB[i])

        # If both given segments have owing curves, recompute the intersection
        # points based on parametric description of curves. The parametric values
        # of the intersection points on each curve are also recomputed.
        if (curveA is not None) and (curveB is not None):
            for i in range(0, numIntersPts):
                status, intersPts[i], parsA[i], parsB[i] = Curve.paramCurvesIntersection(
                                        curveA, curveB, parsA[i], parsB[i])

        return status, intersPts, parsA, parsB
