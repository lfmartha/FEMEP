# Loop class declaration
class Loop():

    def __init__(self, face=None, he=None, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.face = face
        self.he = he
        self.isClosed = False
        self.ID = None

        if face is not None:
            loopOfFace = self.face.loop
            if loopOfFace is not None:
                self.next = loopOfFace.next
                self.prev = loopOfFace
                loopOfFace.next = self

                if self.next is not None:
                    self.next.prev = self
            else:
                self.face.loop = self

    def delete(self):
        # update linked list
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        if self.face is not None:
            if self == self.face.loop:
                self.face.loop = None
