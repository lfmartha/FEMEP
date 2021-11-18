# Shell class declaration
class Shell:

    def __init__(self, face=None):
        self.face = face
        self.vertices = []
        self.edges = []
        self.faces = []
        self.num_vertices = 0
        self.num_edges = 0
        self.num_faces = -1
        self.num_loops = 0
        self.num_hes = 0

    def insertVertex(self, _vertex):

        if _vertex.ID is None:
            self.num_vertices += 1
            _vertex.ID = self.num_vertices
        elif _vertex.ID > self.num_vertices:
            self.num_vertices = _vertex.ID

        if _vertex.he is not None:
            if _vertex.he.ID is None:
                self.num_hes += 1
                _vertex.he.ID = self.num_hes
            elif _vertex.he.ID > self.num_hes:
                self.num_hes = _vertex.he.ID

            if _vertex.he.loop.ID is None:
                self.num_loops += 1
                _vertex.he.loop.ID = self.num_loops
            elif _vertex.he.loop.ID > self.num_loops:
                self.num_loops = _vertex.he.loop.ID

        if len(self.vertices) > 0:
            _vertex.prev = self.vertices[-1]
            self.vertices[-1].next = _vertex

        self.vertices.append(_vertex)

    def insertEdge(self, _edge):
        if _edge.ID is None:
            self.num_edges += 1
            _edge.ID = self.num_edges
        elif _edge.ID > self.num_edges:
            self.num_edges = _edge.ID

        if _edge.he1 is not None:
            if _edge.he1.ID is None:
                self.num_hes += 1
                _edge.he1.ID = self.num_hes
            elif _edge.he1.ID > self.num_hes:
                self.num_hes = _edge.he1.ID

        if _edge.he2 is not None:
            if _edge.he2.ID is None:
                self.num_hes += 1
                _edge.he2.ID = self.num_hes
            elif _edge.he2.ID > self.num_hes:
                self.num_hes = _edge.he2.ID

        if len(self.edges) > 0:
            _edge.prev = self.edges[-1]
            self.edges[-1].next = _edge

        self.edges.append(_edge)

    def insertFace(self, _face):
        self.faces.append(_face)

        if _face.ID is None:
            self.num_faces += 1
            _face.ID = self.num_faces
        elif _face.ID > self.num_faces:
            self.num_faces = _face.ID

        if _face.loop.ID is None:
            self.num_loops += 1
            _face.loop.ID = self.num_loops
        elif _face.loop.ID > self.num_loops:
            self.num_loops = _face.loop.ID

    def removeVertex(self, _vertex):
        self.vertices.remove(_vertex)

    def removeEdge(self, _edge):
        self.edges.remove(_edge)

    def removeFace(self, _face):
        self.faces.remove(_face)

    def renumberIDS(self):

        self.num_vertices = 0
        self.num_edges = 0
        self.num_faces = -1
        self.num_loops = 0
        self.num_hes = 0

        # renumber vertices IDS
        for vertex in self.vertices:
            self.num_vertices += 1
            vertex.ID = self.num_vertices

        # renumber edges IDS
        for edge in self.edges:
            self.num_edges += 1
            edge.ID = self.num_edges

        # renumber faces,loops and half-edges IDS
        for face in self.faces:
            self.num_faces += 1
            face.ID = self.num_faces
            loop = face.loop

            while loop is not None:
                self.num_loops += 1
                loop.ID = self.num_loops
                he = loop.he
                he_begin = he

                if he is not None:
                    while True:
                        self.num_hes += 1
                        he.ID = self.num_hes

                        he = he.next

                        if he == he_begin:
                            break

                loop = loop.next
