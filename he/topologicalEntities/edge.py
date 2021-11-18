from he.topologicalEntities.halfedge import HalfEdge
from he.topologicalEntities.linkedlist import Linkedlist


# Edge class declaration
class Edge(Linkedlist):

    def __init__(self, segment=None, he1=None, he2=None):
        Linkedlist.__init__(self)
        self.he1 = he1
        self.he2 = he2
        self.segment = segment
        self.ID = None

    def delete(self):
        # update linked list
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def getType(self):
        return 'EDGE'

    def AddHe(self, _v, _where, _sign):

        if _where.edge is None:
            he = _where
        else:
            he = HalfEdge(prev=_where.prev, next=_where)

        he.edge = self
        he.vertex = _v
        he.loop = _where.loop

        if _sign:
            self.he1 = he
        else:
            self.he2 = he

        return he

    def incidentFaces(self):
        incFaces = []
        incFaces.append(self.he1.loop.face)
        if self.he1.loop.face != self.he2.loop.face:
            incFaces.append(self.he2.loop.face)
        return incFaces

    def adjacentEdges(self):
        adjEdges = []
        he1 = self.he1
        he2 = self.he2

        # begin the search at the next he of the first he of the edge
        he = he1.next

        # check if the edge is a closed one
        # if he1 is the half-edge inside the closed edge (do not continue)
        if he != he1:
            while he != he2:
                adjEdges.append(he.edge)
                he = he.mate().next

        # begin the search at the next he of the second he of the edge
        he = he2.next

        # check if the edge is a closed one
        # if he2 is the half-edge inside the closed edge (do not continue)
        if he != he2:
            while he != he1:
                adjEdges.append(he.edge)
                he = he.mate().next

        return adjEdges

    def incidentVertices(self):
        incVertices = []
        incVertices.append(self.he1.vertex)
        incVertices.append(self.he2.vertex)
        return incVertices
