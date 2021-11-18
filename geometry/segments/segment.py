
class Segment:
    selected = False
    PARAM_TOL = 1e-7
    nsudv = None

    def setNumberOfSubdivisions(self, _number):
        self.nsudv = _number

    def getNumberOfSubdivisions(self):
        return self.nsudv

    def setSelected(self, _select):
        self.selected = _select

    def isSelected(self):
        return self.selected
