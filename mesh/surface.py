from compgeom.pnt2d import Pnt2D
from geomdl import NURBS
from geomdl import helpers


class NurbsSurface:
    def __init__(self, _degree=None, _knotVectorU=None, _knotVectorV=None, _weights=None, _ctrlPts=None):
        self.degree = _degree
        self.knotVectorU = _knotVectorU
        self.knotVectorV = _knotVectorV
        self.weights = _weights
        self.ctrlPts = _ctrlPts

    def getIsoCurveU(self, _u):
        N = helpers.basis_function(self.degree, self.knotVectorU, 7, 4.0)
        M = helpers.basis_function(self.degree, self.knotVectorV, 7, 4.0)

        IsoCurveU = NURBS.Curve()
        IsoCurveU.degree = 2
        IsoCurveU.ctrlpts = ctrlPtsValues
        IsoCurveU.weights = weights
        IsoCurveU.knotvector = knotVector
        IsoCurveU.sample_size = 10

        return IsoCurveU

    def getIsoCurveV(self, _v):
        IsoCurveV = None
        return IsoCurveV

    def evalPoint(self, _u, _v):
        # Search for knot span in u direction:
        knotVectorU = self.knotVectorU
        for i in range(1, len(knotVectorU)):
            if knotVectorU[i] - knotVectorU[i - 1] != 0.0:
                if _u >= knotVectorU[i - 1] and _u <= knotVectorU[i]:
                    spanU = i - 1
                    break

        # Search for knot span in v direction:
        knotVectorV = self.knotVectorV
        for i in range(1, len(knotVectorV)):
            if knotVectorV[i] - knotVectorV[i - 1] != 0.0:
                if _v >= knotVectorV[i - 1] and _v <= knotVectorV[i]:
                    spanV = i - 1
                    break

        N = helpers.basis_function(self.degree, self.knotVectorU, spanU, _u)
        M = helpers.basis_function(self.degree, self.knotVectorV, spanV, _v)

        # Weighting function
        weights = self.weights
        for i in range(len(weights)):    
            W = 
        pt = None
        return pt

class TSplineSurface:
    def __init__(self, degree=None, knotVectorU=None, knotVectorV=None, weights=None, ctrlPts=None):
        pass