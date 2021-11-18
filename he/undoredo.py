
class UndoRedo:

    def __init__(self, limit=-1):
        self.isInserting = False
        self.limit = limit
        self.temp = []
        self.undocommands = []
        self.redocommands = []

    def begin(self):
        if not self.isInserting:
            self.temp = []
            self.isInserting = True

    def end(self):

        if len(self.temp) > 0:

            # insert command
            self.undocommands.insert(0, self.temp)

            # check if reached limit
            if len(self.undocommands) - 1 == self.limit:
                self.undocommands.pop()

            self.clearRedo()

        self.isInserting = False

    def insertOperation(self, _operation):

        if self.isInserting:
            self.temp.insert(0, _operation)

    def lastCommand(self):
        return self.temp

    def lastOperation(self):
        return self.temp[0]

    def hasUndo(self):
        return len(self.undocommands) > 0

    def hasRedo(self):
        return len(self.redocommands) > 0

    def undo(self):
        if not self.isInserting:
            if self.hasUndo():
                self.temp = self.undocommands.pop(0)
                self.redocommands.insert(0, self.temp)

    def redo(self):
        if not self.isInserting:
            if self.hasRedo():
                self.temp = self.redocommands.pop(0)
                self.undocommands.insert(0, self.temp)

    def clear(self):
        self.isInserting = False
        self.clearRedo()
        self.clearUndo()
        self.temp.clear()

    def clearUndo(self):
        self.undocommands.clear()

    def clearRedo(self):
        self.redocommands.clear()
