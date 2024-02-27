from he.topologicalEntities.vertex import Vertex
from he.topologicalEntities.edge import Edge


# MakeVertexSplitEdge class declaration
class MVSE:

    def __init__(self, point, seg1, seg2, split_edge, vertex=None, edge1=None, edge2=None):

        if point is not None:
            self.vertex = Vertex(point)
            self.edge1 = Edge(seg1)
            self.edge2 = Edge(seg2)
        else:
            self.vertex = vertex
            self.edge1 = edge1
            self.edge2 = edge2

        self.split_edge = split_edge

    def name(self):
        return 'MVSE'

    def execute(self):
        he1 = self.split_edge.he1
        he2 = self.split_edge.he2

        self.edge1.he1 = he1
        self.edge2.he2 = he2
        he1.edge = self.edge1
        he2.edge = self.edge2

        self.edge1.AddHe(self.vertex, he2.next, False)
        self.edge2.AddHe(self.vertex, he1.next, True)
        self.vertex.he = self.edge2.he1

        self.split_edge.he1 = None
        self.split_edge.he2 = None

        self.split_edge.delete()

    def unexecute(self):
        kvje = KVJE(None, self.vertex, self.edge1, self.edge2, self.split_edge)
        kvje.execute()


# KillVertexJoinEdge class declaration
class KVJE:

    def __init__(self, segment, vertex, edge1, edge2, new_edge=None):

        if segment is not None:
            self.new_edge = Edge(segment)
        else:
            self.new_edge = new_edge

        self.vertex = vertex
        self.edge1 = edge1
        self.edge2 = edge2

    def name(self):
        return 'KVJE'

    def execute(self):
        # take the half-edges that are pointing to the vertex
        # that will be deleted
        if self.edge1.he1.vertex == self.vertex:
            he1 = self.edge1.he1
        else:
            he1 = self.edge1.he2

        if self.edge2.he1.vertex == self.vertex:
            he2 = self.edge2.he1
        else:
            he2 = self.edge2.he2

        # adjust the half-edges of the loops because
        # those half-edges will be erased
        he1.loop.he = he1.prev
        he2.loop.he = he2.prev

        old_he1 = he2.prev
        old_he2 = he1.prev

        if he1 == he1.edge.he1:
            self.new_edge.he1 = old_he2
            self.new_edge.he2 = old_he1
        else:
            self.new_edge.he1 = old_he1
            self.new_edge.he2 = old_he2

        he2.delete()
        he1.delete()

        old_he1.edge = self.new_edge
        old_he2.edge = self.new_edge

        self.vertex.he = None
        self.edge1.he1 = None
        self.edge1.he2 = None
        self.edge2.he1 = None
        self.edge2.he2 = None

        self.vertex.delete()
        self.edge1.delete()
        self.edge2.delete()
        del he1
        del he2

    def unexecute(self):
        mvse = MVSE(None, None, None, self.new_edge, self.vertex, self.edge1,
                    self.edge2)
        mvse.execute()
