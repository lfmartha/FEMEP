from he.topologicalEntities.edge import Edge
from he.topologicalEntities.face import Face
from he.topologicalEntities.halfedge import HalfEdge
from he.topologicalEntities.loop import Loop
from geometry.patch import Patch


# MakeEdgeFace class declaration
class MEF():
    def __init__(self, segment, v_begin, v_end, v_begin_next, v_end_next, face_on, edge=None, face=None):

        if segment is not None:
            self.edge = Edge(segment)
            self.face = Face(face_on.shell)
            self.face.patch = Patch()
        else:
            self.edge = edge
            self.face = face

        self.v_begin = v_begin
        self.v_end = v_end
        self.v_begin_next = v_begin_next
        self.v_end_next = v_end_next
        self.face_on = face_on

    def name(self):
        return 'MEF'

    def execute(self):
        next_face = self.face_on.next
        self.face.prev = self.face_on
        self.face_on.next = self.face
        self.face.next = next_face

        if next_face is not None:
            next_face.prev = self.face

        # get Half-edges
        he1 = HalfEdge.inBetween(
            self.v_begin, self.v_begin_next, self.face_on)
        he2 = HalfEdge.inBetween(
            self.v_end, self.v_end_next, self.face_on)

        newloop = Loop(self.face)
        newloop.isClosed = True

        he = he1
        while he != he2:
            he.loop = newloop
            he = he.next

        nhe1 = self.edge.AddHe(he2.vertex,  he1, False)
        nhe2 = self.edge.AddHe(he1.vertex,  he2, True)

        nhe1.prev.next = nhe2
        nhe2.prev.next = nhe1

        temp = nhe1.prev
        nhe1.prev = nhe2.prev
        nhe2.prev = temp
        newloop.he = nhe1
        nhe1.loop = newloop
        nhe2.loop.he = nhe2

    def unexecute(self):

        kef = KEF(self.edge, self.face)
        kef.execute()


# KillEdgeFace class declaration
class KEF():

    def __init__(self, edge, face):
        self.edge = edge
        self.face = face
        self.v_begin = None
        self.v_end = None
        self.v_begin_next = None
        self.v_end_next = None
        self.face_on = None

    def name(self):
        return 'KEF'

    def execute(self):
        he1 = self.edge.he1
        he2 = self.edge.he2

        # Store the necessary entities for undo
        self.v_begin = he1.vertex
        self.v_end = he2.vertex
        self.v_begin_next = he2.next.next.vertex
        self.v_end_next = he1.next.next.vertex
        self.face_on = he1.loop.face

        # Now, execute the operation
        loop_to_delete = he2.loop
        face_to_delete = self.face
        loop_to_keep = he1.loop

        # set the loops of the half-edges belonging to the loop_to_delete as the loop_to_keep
        he = loop_to_delete.he
        while True:
            he.loop = loop_to_keep
            he = he.next

            if he == loop_to_delete.he:
                break

        # stitch the remaining half-egdes
        he1.prev.next = he2
        he2.prev.next = he1
        he = he2.prev
        he2.prev = he1.prev
        he1.prev = he

        he2.delete()
        he1.delete()

        # set the appropriate half-edges of the vertex that will be kept in the model
        he2.vertex.he = he1.next

        if he2.next != he1:
            he1.vertex.he = he2.next

        # set the appropriate half-edge of the loop_to_keep
        loop_to_keep.he = he1.next

        # reset data of the deleted entities
        self.edge.he1 = None
        self.edge.he2 = None
        self.face.loop = None

        self.edge.delete()
        face_to_delete.delete()
        loop_to_delete.delete()

        if he1.prev.next != he1:
            del he1
        if he2.prev.next != he2:
            del he2

    def unexecute(self):
        mef = MEF(None, self.v_begin, self.v_end, self.v_begin_next,
                  self.v_end_next, self.face_on, self.edge, self.face)
        mef.execute()
