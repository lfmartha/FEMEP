import math
import numpy as np


class Pnt2D():

    def __init__(self, _x=None, _y=None):
        self.x = _x
        self.y = _y

    def setX(self, _x):
        self.x = _x

    def setY(self, _y):
        self.y = _y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setCoords(self, _x, _y):
        self.x = _x
        self.y = _y

    # Equality test with tolerance (Manhattan distance)
    def equal(p1, p2, tol):
        return abs(p1.x - p2.x) < tol.x and abs(p1.y-p2.y) < tol.y

    # Equality test without tolerance
    def __eq__(p1, p2):
        return (p1.x == p2.x) and (p1.y == p2.y)

    # operator <
    def __lt__(p1, p2):
        if p1.x == p2.x:
            return p1.y < p2.y
        else:
            return p1.x < p2.x

    # # operator >
    def __gt__(p1, p2):
        if p1.x == p2.x:
            return p1.y > p2.y
        else:
            return p1.x > p2.x

    # Inequality test without tolerance
    def __ne__(p1, p2):
        return not (p1 == p2)

    # Addition +
    def __add__(p1, p2):
        return Pnt2D(p1.x+p2.x, p1.y+p2.y)

    # Addition +=
    def __iadd__(p1, p2):
        p1 = p1+p2
        return p1

    # Subtraction -
    def __sub__(p1, p2):
        return Pnt2D(p1.x-p2.x, p1.y-p2.y)

    # Subtraction -=
    def __isub__(p1, p2):
        p1 = p1-p2
        return p1

    # Scalar multiplication
    def __mul__(p, s):
        return Pnt2D(p.x*s, p.y*s)

    # Division by scalar
    def __truediv__(p, s):
        if s == 0:
            return Pnt2D(0.0, 0.0)
        return Pnt2D(p.x/s, p.y/s)

    # Euclidian distance
    def euclidiandistance(p1, p2):
        return math.sqrt((p1.x-p2.x)*(p1.x-p2.x) +
                         (p1.y-p2.y)*(p1.y-p2.y))

    # Manhattan distance
    def manhattandistance(p1, p2):
        return abs(p1.x-p2.x) + abs(p1.y-p2.y)

    # Square of size (vector)
    def sizesquare(p):
        return (p.x * p.x) + (p.y * p.y)

    # Size (vector)
    def size(p):
        return math.sqrt(Pnt2D.sizesquare(p))

    # Dot product (vector)
    def dotprod(p1, p2):
        return (p1.x * p2.x) + (p1.y * p2.y)

    # Cross product (vector)
    def crossprod(p1, p2):
        return (p1.x * p2.y) - (p2.x * p1.y)

    # Normalize (vector)
    def normalize(p):
        norm = Pnt2D.size(p)
        if norm == 0:
            return Pnt2D(0.0, 0.0)
        return Pnt2D(p.x/norm, p.y/norm)

    # Twice the signed area of triangle p1-p2-p3
    def area2d(p1, p2, p3):
        ptA = p2 - p1
        ptB = p3 - p1
        return Pnt2D.crossprod(ptA, ptB)

    # Rotate around a certain point by a given angle
    def rotate(p, center, ang):
        sen = math.sin(ang)
        cos = math.cos(ang)
        T1 = np.array([[1.0, 0.0, center.x], [0.0, 1.0, center.y], [0.0, 0.0, 1.0]])
        Rot = np.array([[cos, -sen, 0.0], [sen, cos, 0.0], [0.0, 0.0, 1.0]])
        T2 = np.array([[1.0, 0.0, -center.x], [0.0, 1.0, -center.y], [0.0, 0.0, 1.0]])
        Pt = np.array([[p.x], [p.y], [1.0]])
        PtRot = T1@Rot@T2@Pt
        return Pnt2D(PtRot[0][0], PtRot[1][0])
