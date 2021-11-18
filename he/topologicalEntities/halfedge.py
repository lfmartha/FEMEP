from he.topologicalEntities.linkedlist import Linkedlist


class HalfEdge(Linkedlist):

    def __init__(self, vertex=None, loop=None, edge=None, prev=None, next=None):
        Linkedlist.__init__(self, prev, next)
        self.vertex = vertex
        self.edge = edge
        self.loop = loop
        self.ID = None

    # Prepares the half-edge to be deleted
    def delete(self):

        if self.edge is None:
            return
        elif self.next == self:
            self.edge = None
            return self
        else:
            self.edge = None
            self.prev.next = self.next
            self.next.prev = self.prev
            return self.prev

    # Gets the opposite half-edge
    def mate(self):

        if self.edge is None:
            return self.next.prev

        if self == self.edge.he1:
            return self.edge.he2
        else:
            return self.edge.he1

    @staticmethod
    def inBetween(_v1, _v2, _f):

        he = _v1.he
        he_begin = he

        while True:

            if he.mate().vertex == _v2:
                if he.loop.face == _f:
                    return he

            he = he.mate().next

            if he == he_begin:
                return
