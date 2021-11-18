import math


class HeView:

    def __init__(self, _hemodel):
        self.hemodel = _hemodel

    def getPoints(self):
        return self.hemodel.getPoints()

    def getSegments(self):
        return self.hemodel.getSegments()

    def getPatches(self):
        return self.hemodel.getPatches()

    def isEmpty(self):
        return self.hemodel.isEmpty()

    def getSelectedPoints(self):
        points = self.hemodel.points
        selected_points = []
        for pt in points:
            if pt.isSelected():
                selected_points.append(pt)

        return selected_points

    def getSelectedSegments(self):
        segments = self.hemodel.segments
        selected_segments = []
        for seg in segments:
            if seg.isSelected():
                selected_segments.append(seg)

        return selected_segments

    def getSelectedPatches(self):
        patches = self.hemodel.patches
        selected_patches = []
        for patch in patches:
            if patch.isSelected():
                selected_patches.append(patch)

        return selected_patches

    def getEntityAttributes(self, _entity):
        return _entity.attributes

    def getMeshPoints(self, _patch):
        if _patch.mesh is not None:
            return _patch.mesh.model.getPoints()

    def getMeshSegments(self, _patch):
        if _patch.mesh is not None:
            return _patch.mesh.model.getSegments()

    def getMeshPatches(self, _patch):
        if _patch.mesh is not None:
            return _patch.mesh.model.getPatches()

    def getBoundBox(self):

        if self.hemodel.isEmpty():
            return 0.0, 10.0, 0.0, 10.0

        points = self.hemodel.points
        x = points[0].getX()
        y = points[0].getY()

        xmin = x
        ymin = y
        xmax = x
        ymax = y

        for i in range(1, len(points)):
            x = points[i].getX()
            y = points[i].getY()
            xmin = min(x, xmin)
            xmax = max(x, xmax)
            ymin = min(y, ymin)
            ymax = max(y, ymax)

        for segment in self.hemodel.segments:
            xmin_c, xmax_c, ymin_c, ymax_c = segment.getBoundBox()
            xmin = min(xmin_c, xmin)
            xmax = max(xmax_c, xmax)
            ymin = min(ymin_c, ymin)
            ymax = max(ymax_c, ymax)

        return xmin, xmax, ymin, ymax

    def snapToSegment(self, _x, _y, _tol):

        if self.isEmpty():
            return False, _x, _y

        xClst = _x
        yClst = _y
        id_target = -1
        dmin = _tol

        for i in range(0, len(self.hemodel.segments)):
            xC, yC, dist = self.hemodel.segments[i].closestPoint(_x, _y)
            if dist < dmin:
                xClst = xC
                yClst = yC
                dmin = dist
                id_target = i

        if id_target < 0:
            return False, xClst, yClst

        # try to attract to a corner of the segment
        seg_pts = self.hemodel.segments[id_target].getPoints()

        dmin = _tol*2
        for pt in seg_pts:
            pt_x = pt.getX()
            pt_y = pt.getY()
            d = math.sqrt((_x-pt_x)*(_x-pt_x)+(_y-pt_y)*(_y-pt_y))

            if d < dmin:
                xClst = pt_x
                yClst = pt_y
                dmin = d

        # If found a closest point, return its coordinates
        return True, xClst, yClst

    def snapToPoint(self, _x, _y, _tol):
        if self.isEmpty():
            return False, _x, _y

        xClst = _x
        yClst = _y
        id_target = -1
        dmin = _tol

        points = self.hemodel.points
        for i in range(0, len(points)):
            xC = points[i].getX()
            yC = points[i].getY()
            if (abs(_x - xC) < _tol) and (abs(_y - yC) < _tol):
                d = math.sqrt((_x-xC)*(_x-xC)+(_y-yC)*(_y-yC))
                if d < dmin:
                    xClst = xC
                    yClst = yC
                    dmin = d
                    id_target = i

        if id_target < 0:
            return False, xClst, yClst

        # If found a closest point, return its coordinates
        return True, xClst, yClst

    def getIncidentSegmentsFromPoint(self, _point):
        incidentEdges = _point.vertex.incidentEdges()
        incidentSegments = []

        for edge in incidentEdges:
            incidentSegments.append(edge.segment)

        return incidentSegments

    def getIncidentPatchesFromPoint(self, _point):
        incidentFaces = _point.vertex.incidentFaces()
        incidentPatches = []

        for face in incidentFaces:
            if len(face.patch.segments) > 0:
                incidentPatches.append(face.patch)

        return incidentPatches

    def getAdjacentPointsFromPoint(self, _point):
        adjacentVertices = _point.vertex.adjacentVertices()
        adjacentPoints = []

        for vertex in adjacentVertices:
            adjacentPoints.append(vertex.point)

        return adjacentPoints

    def getAdjacentSegmentsFromSegment(self, _segment):
        adjacentEdges = _segment.edge.adjacentEdges()
        adjacentSegments = []

        for edge in adjacentEdges:
            adjacentSegments.append(edge.segment)

        return adjacentSegments

    def getIncidentPatchesFromSegment(self, _segment):
        incidentFaces = _segment.edge.incidentFaces()
        adjacentPatches = []

        for face in incidentFaces:
            if len(face.patch.segments) > 0:
                adjacentPatches.append(face.patch)

        return adjacentPatches

    def getIncidentPointsFromSegment(self, _segment):
        incidentVertices = _segment.edge.incidentVertices()
        adjacentPoints = []

        for vertex in incidentVertices:
            adjacentPoints.append(vertex.point)

        return adjacentPoints

    def getIncidentSegmentsFromPatch(self, _patch):
        incidentEdges = _patch.face.incidentEdges()
        adjacentSegments = []

        for edge in incidentEdges:
            adjacentSegments.append(edge.segment)

        return adjacentSegments

    def getAdjacentPatchesFromPatch(self, _patch):
        adjacentFaces = _patch.face.adjacentFaces()
        adjacentPatches = []

        for face in adjacentFaces:
            if len(face.patch.segments) > 0:
                adjacentPatches.append(face.patch)

        return adjacentPatches

    def getIncidentPointsFromPatch(self, _patch):
        incidentVertices = _patch.face.incidentVertices()
        adjacentPoints = []

        for vertex in incidentVertices:
            adjacentPoints.append(vertex.point)

        return adjacentPoints

    def getInternalPacthesFromPatch(self, _patch):
        internalFaces = _patch.face.internalFaces()
        internalPatches = []

        for face in internalFaces:
            internalPatches.append(face.patch)

        return internalPatches
