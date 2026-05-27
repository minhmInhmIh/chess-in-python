class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"], 
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self, move):
        self.board[move.oldRow][move.oldCol] = "--"
        self.board[move.newRow][move.newCol] = move.movedPiece
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.oldRow][move.oldCol] = move.movedPiece
            self.board[move.newRow][move.newCol] = move.capturedPiece
            self.whiteToMove = not self.whiteToMove
    def isValidMove(self,move):
        pass               

class Move():

    ranksToRows = {
        "1" : 7,
        "2" : 6,
        "3" : 5,
        "4" : 4,
        "5" : 3,
        "6" : 2,
        "7" : 1,
        "8" : 0
    }
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    
    filesToCols = {
        "a" : 0,
        "b" : 1,
        "c" : 2,
        "d" : 3,
        "e" : 4,
        "f" : 5,
        "g" : 6,
        "h" : 7,
    }

    colsToFiles = {v : k for k, v in filesToCols.items()}

    def __init__(self,oldPos,newPos,board):
        self.oldRow = oldPos[0]
        self.oldCol = oldPos[1]
        self.newRow = newPos[0]
        self.newCol = newPos[1]
        self.movedPiece = board[self.oldRow][self.oldCol]
        self.capturedPiece = board[self.newRow][self.newCol]
    def getChessNotation(self):
        return self.getFileAndRank(self.oldRow, self.oldCol) + self.getFileAndRank(self.newRow, self.newCol)
    def getFileAndRank(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]