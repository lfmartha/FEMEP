
class Grid:

    def __init__(self):
        self.isSnapOn = False
        self.gridX = 1.0
        self.gridY = 1.0

    def reset(self):
        self.isSnapOn = False
        self.gridX = 1.0
        self.gridY = 1.0

    def setSnapData(self, _isSnapOn, _dx, _dy):
        self.gridX = _dx
        self.gridY = _dy
        self.isSnapOn = _isSnapOn

    def getSnapInfo(self):
        return self.isSnapOn

    def getGridSpace(self):
        return self.gridX, self.gridY

    def snapTo(self, _x, _y):
        fp = _x / self.gridX
        ip = int(fp)
        fp = fp - ip
        if fp > 0.5:
            _x = (ip + 1.0) * self.gridX
        elif fp < -0.5:
            _x = (ip - 1.0) * self.gridX
        else:
            _x = ip * self.gridX

        fp = _y / self.gridY
        ip = int(fp)
        fp = fp - ip

        if fp > 0.5:
            _y = (ip + 1.0) * self.gridY
        elif fp < -0.5:
            _y = (ip - 1.0) * self.gridY
        else:
            _y = ip * self.gridY
        return _x, _y
