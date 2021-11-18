from geometry.point import Point
from compgeom.tesselation import Tesselation
from compgeom.compgeom import CompGeom


class Patch:

    def __init__(self):
        self.pts = []  # boundary points
        self.segments = []  # vector of boundary segments
        # orientations of segments with respect to counter-clockwise region boundary
        self.segmentOrients = []
        self.mesh = None
        self.selected = False
        self.holes = []  # vector of region holes
        self.holesOrients = []
        self.internalSegments = []
        self.internalSegmentsOrients = []
        self.isDeleted = False
        self.face = None
        self.attributes = []

    def __del__(self):
        if self.mesh:
            del self.mesh

    def getPoints(self):
        return self.pts

    def getSegments(self):
        return self.segments

    def getSegmentOrients(self):
        return self.segmentOrients

    def setSelected(self, _select):
        self.selected = _select

    def isSelected(self):
        return self.selected

    def setMesh(self, _mesh):
        self.mesh = _mesh

    def getMesh(self):
        return self.mesh

    def getBoundBox(self):

        if len(self.pts) == 0:
            return

        xmin = self.pts[0].getX()
        ymin = self.pts[0].getY()
        xmax = self.pts[0].getX()
        ymax = self.pts[0].getY()

        if len(self.pts) == 1:
            return

        for j in range(1, len(self.pts)):
            xmin = min(xmin, self.pts[j].getX())
            xmax = max(xmax, self.pts[j].getX())
            ymin = min(ymin, self.pts[j].getY())
            ymax = max(ymax, self.pts[j].getY())

        return xmin, xmax, ymin, ymax

    def setBoundary(self, _boundarysegments, _isOriented):
        self.segments = _boundarysegments
        self.segmentOrients = _isOriented
        self.pts = self.boundaryPolygon()

    def setHoles(self, _holessegments, _isOriented):
        self.holes = _holessegments
        self.holesOrients = _isOriented

    def setInternalSegments(self, _internalSegments, _isOriented):
        self.internalSegments = _internalSegments
        self.internalSegmentsOrients = _isOriented

    def isPointInside(self, _pt):
        numIntersec = 0
        for i in range(0, len(self.segments)):
            numIntersec += self.segments[i].ray(_pt)

        if numIntersec % 2 != 0:
            for i in range(0, len(self.holes)):
                numIntersec = 0
                for j in range(0, len(self.holes[i])):
                    numIntersec += self.holes[i][j].ray(_pt)

                if numIntersec % 2 != 0:
                    return False

            return True

        else:
            return False

    def boundaryPolygon(self):
        polygon = []
        for i in range(0, len(self.segments)):
            segmentPol = self.segments[i].getPoints()
            if self.segmentOrients[i]:
                for j in range(0, len(segmentPol)-1):
                    polygon.append(segmentPol[j])
            else:
                for j in range(len(segmentPol)-1, 0, -1):
                    polygon.append(segmentPol[j])

        return polygon

    def boundaryHole(self):
        polygons = []

        for i in range(0, len(self.holes)):
            polygon = []
            for j in range(0, len(self.holes[i])):
                segmentpol = self.holes[i][j].getPoints()
                if self.holesOrients[i][j]:
                    for m in range(0, len(segmentpol)-1):
                        polygon.append(segmentpol[m])
                else:
                    for m in range(len(segmentpol)-1, 0, -1):
                        polygon.append(segmentpol[m])

            polygon.reverse()
            polygons.append(polygon)

        return polygons

    def boundaryInternalSegments(self):
        polygons = []
        for i in range(0, len(self.internalSegments)):
            polygon = []
            for j in range(0, len(self.internalSegments[i])):
                segmentpol = self.internalSegments[i][j].getPoints()
                if self.internalSegmentsOrients[i][j]:
                    for m in range(0, len(segmentpol)-1):
                        polygon.append(segmentpol[m])
                else:
                    for m in range(len(segmentpol)-1, 0, -1):
                        polygon.append(segmentpol[m])

            polygon.reverse()
            polygons.append(polygon)

        return polygons

    def Area(self):
        Area = 0
        pts = self.pts
        triangs = Tesselation.triangleParing(pts)
        for j in range(0, len(triangs)):
            a = Point(pts[triangs[j][0]].getX(),
                      pts[triangs[j][0]].getY())
            b = Point(pts[triangs[j][1]].getX(),
                      pts[triangs[j][1]].getY())
            c = Point(pts[triangs[j][2]].getX(),
                      pts[triangs[j][2]].getY())

            Area += (a.getX()*b.getY() - a.getY()*b.getX()
                     + a.getY()*c.getX() - a.getX()*c.getY()
                     + b.getX()*c.getY() - c.getX()*b.getY()) / 2.0

        internalFaces = self.face.internalFaces()
        if len(internalFaces) > 0:
            for face in internalFaces:
                Area -= face.patch.Area()
                adjacentFaces = face.adjacentFaces()
                for adjface in adjacentFaces:
                    if adjface not in internalFaces and adjface != self.face:
                        pts = adjface.patch.getPoints()
                        if CompGeom.isPointInPolygon(self.pts, pts[0]):
                            Area -= adjface.patch.Area()

        return Area
