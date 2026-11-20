import random

class Board:
    def knight_init_board(self, n: int) -> list[int]:
        return list(range(1, n, 2)) + list(range(0, n, 2))

    def __init__(self, n: int):
        self.n = int(n)

        if self.n % 6 not in [2,3]:
            self.board = self.knight_init_board(self.n)
        else:
            self.board = [random.randrange(0, self.n) for i in range(self.n)]

        self.queensPerRow = [0 for i in range(self.n)]
        self.queensPerD1 = [0 for i in range(self.n*2-1)]
        self.queensPerD2 = [0 for i in range(self.n*2-1)]
        for x in range(self.n):
            y = self.board[x]
            d1 = self.n-1 + (x-y)
            d2 = (x+y)            
            self.queensPerRow[y]+=1
            self.queensPerD1[d1]+=1
            self.queensPerD2[d2]+=1

    def findConflictedQ(self) -> dict:
        conflicts={}
        for x in range(self.n):
            y = self.board[x]
            d1 = self.n - 1 + x - y
            d2 = x + y

            cnt = self.queensPerRow[y] + self.queensPerD1[d1] + self.queensPerD2[d2] - 3

            if cnt>0:
                conflicts[x] = cnt

        return conflicts

    def tempQRemoval(self, x, y, val):
        d1 = self.n - 1 + x -y
        d2 = x + y

        self.queensPerD2[d2]+=val
        self.queensPerD1[d1]+=val
        self.queensPerRow[y]+=val

    def minConRow(self, x):
        oldR = self.board[x]

        self.tempQRemoval(x, oldR, -1)
        conflicts=[]

        for y in range(self.n):
            d1 = self.n - 1 + x - y
            d2 = x + y
            cnt = self.queensPerRow[y]+self.queensPerD1[d1]+self.queensPerD2[d2]
            conflicts.append(cnt)

        minConflict = min(conflicts)

        options = [y for y in range(self.n) if conflicts[y]==minConflict]

        newR = random.choice(options)
        self.board[x] = newR
        self.tempQRemoval(x, newR, 1)

        return newR

    def minConflicts(self):
        if self.n == 2 or self.n == 3:
            return -1

        max_steps = 100000

        for step in range(max_steps):
            conflicted = self.findConflictedQ()

            if len(conflicted) == 0:
                return self.board

            maxConflict = max(conflicted.values())
            maxConflictedQueens = [cQ for cQ in conflicted.keys() if conflicted[cQ]==maxConflict]
            queen = random.choice(maxConflictedQueens)

            self.minConRow(queen)
        return -1

    
    def drawBoard(self):
        board1 = []
        row=" "
        for i in range(self.n):
            for j in range(self.n):
                if self.board[j] == i:
                    row+=('* ')
                else:
                    row+=('_ ')
            board1.append(row)
            row=" "

        for i in range(self.n):
            print(board1[i])


n = input()
while int(n) <= 0 :
    print("Invalid input")
    n = input()

b = Board(n)
#b.drawBoard()
print(b.minConflicts())