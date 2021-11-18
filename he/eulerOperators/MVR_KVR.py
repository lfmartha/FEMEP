from he.topologicalEntities.vertex import Vertex
from he.topologicalEntities.halfedge import HalfEdge
from he.topologicalEntities.loop import Loop


# MakeVertexRing class declaration
class MVR:
    def __init__(self, point, face_on, vertex=None):

        if point is not None:
            self.vertex = Vertex(point)
        else:
            self.vertex = vertex

        self.face_on = face_on

    def name(self):
        return 'MVR'

    def execute(self):
        # create topological entities
        newloop = Loop(self.face_on)
        newhe = HalfEdge(self.vertex, newloop)

        # set parameters
        newloop.he = newhe
        newhe.prev = newhe
        newhe.next = newhe
        self.vertex.he = newhe

    def unexecute(self):
        kvr = KVR(self.vertex, self.face_on)
        kvr.execute()


# KillVertexRing class declaration
class KVR:
    def __init__(self, vertex, face_on):
        self.vertex = vertex
        self.face_on = face_on

    def name(self):
        return 'KVR'

    def execute(self):
        he = self.vertex.he
        loop = he.loop

        self.vertex.he = None

        he.delete()
        loop.delete()

        del he

    def unexecute(self):
        mvr = MVR(None, self.face_on, self.vertex)
        mvr.execute()
