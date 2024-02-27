from he.topologicalEntities.edge import Edge
from he.topologicalEntities.halfedge import HalfEdge
from he.topologicalEntities.loop import Loop


# MakeEdgeFace class declaration
class MEKR:
    def __init__(self, segment, v_begin, v_end, v_begin_next, v_end_next, face_on, edge=None):

        if segment is not None:
            self.edge = Edge(segment)
        else:
            self.edge = edge

        self.v_begin = v_begin
        self.v_end = v_end
        self.v_begin_next = v_begin_next
        self.v_end_next = v_end_next
        self.face_on = face_on

    def name(self):
        return 'MEKR'

    def execute(self):
        # Loop l2 is always deleted. Therefore, this loop must not be
        # the outter loop of the self.face. This can be avoided by ensuring that
        # he2 is always a half-edge which belongs to an inner loop. This check
        # is currently implemented in previous lines to MEKR usage.
        # [see Class: Hecontroller function: makeEdge for more information.]

        # get the half-edges
        he1 = HalfEdge.inBetween(self.v_begin, self.v_begin_next, self.face_on)
        he2 = HalfEdge.inBetween(self.v_end, self.v_end_next, self.face_on)

        l1 = he1.loop
        l2 = he2.loop

        n_he1 = l2.he

        while True:
            n_he1.loop = l1
            n_he1 = n_he1.next

            if n_he1 == l2.he:
                break

        n_he1 = self.edge.AddHe(he1.vertex, he1, True)
        n_he2 = self.edge.AddHe(he2.vertex, he2, False)
        n_he1.next = he2
        n_he2.next = he1
        he2.prev = n_he1
        he1.prev = n_he2

        l2.delete()

    def unexecute(self):
        kemr = KEMR(self.edge, self.edge.he1.vertex)
        kemr.execute()


# killEdgeFace class declaration
class KEMR:
    def __init__(self, edge, v_out):
        self.edge = edge
        self.v_out = v_out
        self.v_begin = None
        self.v_end = None
        self.v_begin_next = None
        self.v_end_next = None
        self.face_on = None

    def name(self):
        return 'KEMR'

    def execute(self):
        he1 = self.edge.he1
        he2 = self.edge.he2

        if he1.vertex != self.v_out:
            aux = he1
            he1 = he2
            he2 = aux

        # Store the necessary entities for undo
        self.v_begin = he1.vertex
        self.v_end = he2.vertex
        self.face_on = he1.loop.face

        if he2.next == he1:  # Case 1.1 -> he1 vertex is an isolated vertex
            self.v_begin_next = self.v_begin
        elif he2.next.next == he1:  # Case 1.2 -> he1 vertex has a closed segment
            self.v_begin_next = self.v_begin
        else:  # Case 1.3 -> he1 vertex has a branch
            self.v_begin_next = he2.next.mate().vertex

        if he1.next == he2:  # Case 2.1 -> he1 vertex is an isolated vertex
            self.v_end_next = self.v_end
        elif he1.next.next == he2:  # Case 2.2 -> he1 vertex has a closed segment
            self.v_end_next = self.v_end
        else:  # Case 2.3 -> he1 vertex has a branch
            self.v_end_next = he1.next.mate().vertex

        # Now, execute the operation
        ol = he1.loop
        nl = Loop(ol.face)

        he3 = he1.next
        he1.next = he2.next
        he2.next.prev = he1
        he2.next = he3
        he3.prev = he2
        he4 = he2

        while True:
            he4.loop = nl
            he4 = he4.next

            if he4 == he2:
                break

        he1.vertex.he = he1.next
        he2.vertex.he = he2.next

        ol.he = he1.delete()
        nl.he = he2.delete()

        self.edge.he1 = None
        self.edge.he2 = None

        if he1.prev.next != he1:
            del he1
        if he2.prev.next != he2:
            del he2

        self.edge.delete()

    def unexecute(self):
        mekr = MEKR(None, self.v_begin, self.v_end,
                    self.v_begin_next, self.v_end_next, self.face_on, self.edge)
        mekr.execute()
