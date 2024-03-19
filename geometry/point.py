from compgeom.pnt2d import Pnt2D


class Point(Pnt2D):

    def __init__(self, _x=None, _y=None):
        self.x = _x
        self.y = _y
        self.selected = False
        self.vertex = None
        self.attributes = []

    def setSelected(self, _select):
        self.selected = _select

    def isSelected(self):
        return self.selected
