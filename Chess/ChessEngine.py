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
        self.moveFunctions = {
            "p" : self.getPawnMove,
            "R" : self.getRookMove,
            "B" : self.getBishopMove,
            "N" : self.getKnightMove,
            "Q" : self.getQueenMove,
            "K" : self.getKingMove
        } 
        
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
    def getValidMove(self):
        return self.getAllMove()       
    def getAllMove(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):    
                team = self.board[r][c][0]
                if (team == "w" and self.whiteToMove) or (team == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    def getPawnMove(self,r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >=0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c-1 >=0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1), self.board))
    def getRookMove(self,r, c, moves):
        direction = ((-1,0),(0,-1),(1,0),(0,1))
        enemy = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol= c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getBishopMove(self, r, c, moves):
        direction = ((1,1),(1,-1),(-1,-1),(-1,1))
        enemy = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMove(self, r,c,moves):
        knightMoves = ((-2,1),(-2,-1),(-1,2),(1,2),(2,-1),(2,1),(1,-2),(-1,-2))
        ally = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r,c),(endRow,endCol), self.board))
    def getQueenMove(self, r,c,moves):
        self.getBishopMove(r,c,moves)
        self.getRookMove(r,c,moves)
    def getKingMove(self,r,c,moves):
        kingMove = ((1,1),(1,-1),(-1,-1),(-1,1), (-1,0),(0,-1),(1,0),(0,1)) # queen but nerfed
        ally = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMove[i][0]
            endCol = c + kingMove[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r,c),(endRow,endCol), self.board))
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
        self.moveID = self.oldRow * 1000 + self.oldCol * 100 + self.newRow * 10 + self.newCol
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getFileAndRank(self.oldRow, self.oldCol) + self.getFileAndRank(self.newRow, self.newCol)
    def getFileAndRank(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]