from he.topologicalEntities.edge import Edge
from he.topologicalEntities.vertex import Vertex
from he.topologicalEntities.halfedge import HalfEdge


# MakeEdgeVertex class declaration
class MEV:
    def __init__(self, point, segment, v_begin, v_next, face_on, vertex=None, edge=None):

        if point is not None:
            self.vertex = Vertex(point)
            self.edge = Edge(segment)
        else:
            self.vertex = vertex
            self.edge = edge

        self.v_begin = v_begin
        self.v_next = v_next
        self.face_on = face_on

    def name(self):
        return 'MEV'

    def execute(self):
        # get half-edges
        he = HalfEdge.inBetween(self.v_begin, self.v_next, self.face_on)

        self.edge.AddHe(he.vertex, he, False)
        self.edge.AddHe(self.vertex, he, True)

        self.vertex.he = he.prev
        he.vertex.he = he

    def unexecute(self):
        kev = KEV(self.edge, self.vertex)
        kev.execute()


# KillEdgeVertex class declaration
class KEV:
    def __init__(self, edge=None, vertex=None):
        self.edge = edge
        self.vertex = vertex
        self.v_begin = None
        self.v_next = None
        self.face_on = None

    def name(self):
        return 'KEV'

    def execute(self):
        he1 = self.edge.he1
        he2 = self.edge.he2

        # switch half-edges such that he1.vertex will be deleted
        if he1.vertex != self.vertex:
            temp = he1
            he1 = he2
            he2 = temp

        # Store the necessary entities for undo
        self.v_begin = he2.vertex

        if he2.next == he1 and he1.next == he2:
            self.v_next = self.v_begin

        elif he2.next != he1 and he1.next == he2:
            self.v_next = he2.next.mate().vertex
        else:
            self.v_next = he1.next.mate().vertex

        self.face_on = he1.loop.face

        # Now, execute the operation
        he = he2.next

        while he != he1:
            he.vertex = he2.vertex
            he = he.mate().next

        he2.vertex.he = he1.next
        he1.loop.he = he1.delete()
        he2.loop.he = he2.delete()

        # cleaning the removed entities
        self.edge.he1 = None
        self.edge.he2 = None
        self.vertex.he = None

        if he1.prev.next != he1:
            del he1

        if he2.prev.next != he2:
            del he2

        self.vertex.delete()
        self.edge.delete()

    def unexecute(self):

        mev = MEV(None, None, self.v_begin, self.v_next,
                  self.face_on, self.vertex, self.edge)
        mev.execute()
