# Linkedlist superclass declaration
class Linkedlist:
    def __init__(self, prev=None, next=None):

        self.prev = prev
        self.next = next

        if prev is not None:
            self.prev.next = self
        if next is not None:
            self.next.prev = self
