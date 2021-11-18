# ------------------------------------------------------------

# This code contains a set of operations necessary for
#  the proper functioning of the UndoRedo class

# ------------------------------------------------------------

# migrates loops from one face (origin) to a new face (destination)
class MigrateLoops:
    def __init__(self, _origin, _destination, _loops):
        self.origin = _origin
        self.destination = _destination
        self.loops = _loops

    def name(self):
        return 'MIGRATESLOOPS'

    def execute(self):
        for loop_vertex in self.loops:
            loop = self.findLoopOfFace(loop_vertex, self.origin)

            loop.prev.next = loop.next

            if loop.next is not None:
                loop.next.prev = loop.prev

            loop.face = self.destination
            out_loop = self.destination.loop
            loop.prev = out_loop
            loop.next = out_loop.next

            if out_loop.next is not None:
                out_loop.next.prev = loop

            out_loop.next = loop

    def unexecute(self):
        inverse = MigrateLoops(self.destination, self.origin, self.loops)
        inverse.execute()

    def findLoopOfFace(self, _vertex, _face):
        he_begin = _vertex.he
        he = he_begin

        while True:
            if he.loop.face == _face:
                return he.loop

            he = he.mate().next

            if he == he_begin:
                break


# inverts the half-edges of an edge
class Flip:
    def __init__(self, _edge):
        self.edge = _edge

    def name(self):
        return 'FLIP'

    def execute(self):
        temp = self.edge.he1
        self.edge.he1 = self.edge.he2
        self.edge.he2 = temp

    def unexecute(self):
        self.execute()


# Prevents showing the patch on the screen
class DelPatch:
    def __init__(self, _patch):
        self.patch = _patch

    def name():
        return 'DEL_PATCH'

    def execute(self):
        self.patch.isDeleted = True
        self.patch.setSelected(False)

    def unexecute(self):
        self.patch.isDeleted = False


# Allows to show the patch on the screen
class CreatePatch:
    def __init__(self, _patch):
        self.patch = _patch

    def name(self):
        return 'CREATE_PATCH'

    def execute(self):
        self.patch.isDeleted = False
        self.patch.setSelected(False)

    def unexecute(self):
        self.patch.isDeleted = True


class InsertShell:
    def __init__(self, _shell, _hemodel):
        self.shell = _shell
        self.hemodel = _hemodel

    def name(self):
        return 'INSERT_SHELL'

    def execute(self):
        self.hemodel.insertShell(self.shell)

    def unexecute(self):
        self.hemodel.removeShell()


class RemoveShell:
    def __init__(self, _shell, _hemodel):
        self.shell = _shell
        self.hemodel = _hemodel

    def name(self):
        return 'REMOVE_SHELL'

    def execute(self):
        self.hemodel.removeShell()

    def unexecute(self):
        self.hemodel.insertShell(self.shell)


class InsertFace:
    def __init__(self, _face, _hemodel):
        self.face = _face
        self.hemodel = _hemodel

    def name(self):
        return 'INSERT_FACE'

    def execute(self):
        self.hemodel.insertFace(self.face)

    def unexecute(self):
        self.hemodel.removeFace(self.face)


class RemoveFace:
    def __init__(self, _face, _hemodel):
        self.face = _face
        self.hemodel = _hemodel

    def name(self):
        return 'REMOVE_FACE'

    def execute(self):
        self.face.patch.setSelected(False)
        self.hemodel.removeFace(self.face)

    def unexecute(self):
        self.hemodel.insertFace(self.face)


class InsertEdge:
    def __init__(self, _edge, _hemodel):
        self.edge = _edge
        self.hemodel = _hemodel

    def name(self):
        return 'INSERT_EDGE'

    def execute(self):
        self.hemodel.insertEdge(self.edge)

    def unexecute(self):
        self.hemodel.removeEdge(self.edge)


class RemoveEdge:
    def __init__(self, _edge, _hemodel):
        self.edge = _edge
        self.hemodel = _hemodel

    def name(self):
        return 'REMOVE_EDGE'

    def execute(self):
        self.edge.segment.setSelected(False)
        self.hemodel.removeEdge(self.edge)

    def unexecute(self):
        self.hemodel.insertEdge(self.edge)


class InsertVertex:
    def __init__(self, _vertex, _hemodel):
        self.vertex = _vertex
        self.hemodel = _hemodel

    def name(self):
        return 'INSERT_VERTEX'

    def execute(self):
        self.hemodel.insertVertex(self.vertex)

    def unexecute(self):
        self.hemodel.removeVertex(self.vertex)


class RemoveVertex:
    def __init__(self, _vertex, _hemodel):
        self.vertex = _vertex
        self.hemodel = _hemodel

    def name(self):
        return 'REMOVE_VERTEX'

    def execute(self):
        self.vertex.point.setSelected(False)
        self.hemodel.removeVertex(self.vertex)

    def unexecute(self):
        self.hemodel.insertVertex(self.vertex)


class SetAttribute:
    def __init__(self, _entity, _attribute):
        self.entity = _entity
        self.attribute = _attribute
        self.oldAttribute = None

        for att in self.entity.attributes:
            if att['type'] == self.attribute['type']:
                self.oldAttribute = att
                break

    def name(self):
        return 'SET_ATTRIBUTE'

    def execute(self):
        if self.oldAttribute is not None:
            self.entity.attributes.remove(self.oldAttribute)
        self.entity.attributes.append(self.attribute)

    def unexecute(self):
        self.entity.attributes.remove(self.attribute)
        if self.oldAttribute is not None:
            self.entity.attributes.append(self.oldAttribute)


class UnSetAttribute:
    def __init__(self, _entity, _attribute):
        self.entity = _entity
        self.attribute = _attribute

    def name(self):
        return 'UNSET_ATTRIBUTE'

    def execute(self):
        self.entity.attributes.remove(self.attribute)

    def unexecute(self):
        self.entity.attributes.append(self.attribute)


class DelAttribute:
    def __init__(self, _attManager, _name, _hemodel, _cbox=None):
        self.attManager = _attManager
        self.attribute = self.attManager.getAttributeByName(_name)
        self.hemodel = _hemodel
        self.entities = []
        self.comboBox = _cbox

        if self.attribute['applyOnVertex']:
            points = self.hemodel.getPoints()
            for pt in points:
                if self.attribute in pt.attributes:
                    self.entities.append(pt)

        if self.attribute['applyOnEdge']:
            segments = self.hemodel.getSegments()
            for seg in segments:
                if self.attribute in seg.attributes:
                    self.entities.append(seg)

        if self.attribute['applyOnFace']:
            patches = self.hemodel.getPatches()
            for patch in patches:
                if self.attribute in patch.attributes:
                    self.entities.append(patch)

    def name(self):
        return 'DEL_ATTRIBUTE'

    def execute(self):
        self.attManager.removeAttribute(self.attribute)

        if self.comboBox is not None:
            self.comboBox.setCurrentText(self.attribute['name'])
            index = self.comboBox.currentIndex()
            self.comboBox.removeItem(index)

        for entity in self.entities:
            entity.attributes.remove(self.attribute)

    def unexecute(self):
        attributes = self.attManager.getAttributes()

        for att in attributes:
            if att['name'] == self.attribute['name']:
                self.attribute['name'] = self.attribute['name'] + '_1'

        self.attManager.attributes.append(self.attribute)
        if self.comboBox is not None:
            self.comboBox.addItem(self.attribute['name'])

        for entity in self.entities:
            setAtt = SetAttribute(entity, self.attribute)
            setAtt.execute()


class SetMesh:
    def __init__(self, _patch, _mesh):
        self.patch = _patch
        self.oldMesh = _patch.mesh
        self.mesh = _mesh

    def name(self):
        return 'SET_MESH'

    def execute(self):
        self.patch.mesh = self.mesh

    def unexecute(self):
        self.patch.mesh = self.oldMesh


class DelMesh:
    def __init__(self, _patch):
        self.patch = _patch
        self.oldMesh = _patch.mesh

    def name(self):
        return 'SET_MESH'

    def execute(self):
        self.patch.mesh = None

    def unexecute(self):
        self.patch.mesh = self.oldMesh


class SetNumberOfSubdivisions:
    def __init__(self, _seg, _attribute):
        self.seg = _seg
        self.numberOfSubdivision = _attribute
        self.oldnumber = _seg.getNumberOfSubdivisions()

    def name(self):
        return 'SET_NUMBER_OF_SUBDIVISIONS'

    def execute(self):
        self.seg.setNumberOfSubdivisions(self.numberOfSubdivision)

    def unexecute(self):
        self.seg.setNumberOfSubdivisions(self.oldnumber)
