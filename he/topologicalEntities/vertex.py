from he.topologicalEntities.linkedlist import Linkedlist


# Vertex class declaration
class Vertex(Linkedlist):

    def __init__(self, point=None, he=None):
        Linkedlist.__init__(self)
        self.point = point
        self.he = he
        self.ID = None

    def delete(self):
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def getType(self):
        return 'VERTEX'

    def incidentFaces(self):
        incFaces = []
        he = self.he
        heBegin = he
        while True:
            face = he.loop.face
            if face not in incFaces:
                incFaces.append(face)

            he = he.mate().next
            if he == heBegin:
                break

        return incFaces

    def incidentEdges(self):
        incEdges = []
        he = self.he
        heBegin = he

        if he.edge is None:
            return incEdges

        while True:
            if he.edge not in incEdges:
                incEdges.append(he.edge)

            he = he.mate().next

            if he == heBegin:
                break

        return incEdges

    def adjacentVertices(self):
        adjVertices = []
        he = self.he
        heBegin = he

        while True:
            he = he.mate()
            if he.vertex != self:
                adjVertices.append(he.vertex)

            he = he.next

            if he == heBegin:
                break

        return adjVertices
