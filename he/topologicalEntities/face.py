from he.topologicalEntities.linkedlist import Linkedlist


class Face(Linkedlist):

    def __init__(self, shell=None, loop=None, prev=None, next=None, patch=None):
        Linkedlist.__init__(self, prev, next)
        self.shell = shell
        self.loop = loop  # external loop
        self.intLoops = []  # list of internal loops
        self.patch = patch
        self.ID = None

    def delete(self):
        # update linked list
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def getType(self):
        return 'FACE'

    def adjacentFaces(self):
        adjFaces = []
        loop = self.loop
        if loop.he is not None:
            he = loop.he
            heBegin = he

            while True:
                face = he.mate().loop.face
                if face != self:
                    if face not in adjFaces:
                        adjFaces.append(face)

                he = he.next
                if he == heBegin:
                    break

        return adjFaces

    def incidentEdges(self):
        adjEdges = []
        he = self.loop.he
        heBegin = he

        while True:
            adjEdges.append(he.edge)
            he = he.next

            if he == heBegin:
                break

        return adjEdges

    def incidentVertices(self):
        adjVertexes = []
        he = self.loop.he
        heBegin = he

        while True:
            adjVertexes.append(he.vertex)
            he = he.next

            if he == heBegin:
                break

        return adjVertexes

    def internalFaces(self):
        internalFaces = []

        loop = self.loop.next

        while loop is not None:
            he_begin = loop.he
            he = he_begin

            while True:
                if he.mate().loop != loop:
                    if he.mate().loop.isClosed:
                        internalFaces.append(loop.he.mate().loop.face)
                        break

                he = he.next
                if he == he_begin:
                    break

            loop = loop.next

        return internalFaces

    def updateBoundary(self):
        he_init = self.loop.he
        he = he_init
        bound = []
        orientation = []

        while True:
            if he.edge is not None:
                bound.append(he.edge.segment)
                orientation.append(he == he.edge.he1)

            he = he.next

            if he == he_init:
                break

        self.patch.setBoundary(bound, orientation)

    def updateHoles(self):
        loop = self.loop.next
        self.intLoops.clear()  # clear the list of inner loops
        holes_bound = []
        holes_orientation = []
        intSegments = []
        intSegmentsOrientation = []

        while loop is not None:
            self.intLoops.append(loop)
            he_init = loop.he
            he = he_init
            bound = []
            orientation = []
            isClosed = False

            if he.edge is not None:
                while True:
                    if he.mate().loop.isClosed:
                        isClosed = True

                    bound.append(he.edge.segment)
                    orientation.append(he == he.edge.he1)

                    he = he.next

                    if he == he_init:
                        break

                if len(bound) > 0:
                    if isClosed:
                        holes_bound.append(bound)
                        holes_orientation.append(orientation)
                    else:
                        intSegments.append(bound)
                        intSegmentsOrientation.append(orientation)

            loop = loop.next

        self.patch.setHoles(holes_bound, holes_orientation)
        self.patch.setInternalSegments(intSegments, intSegmentsOrientation)
