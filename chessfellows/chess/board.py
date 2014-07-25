class Board():
    def __init__(self, x = None):
        self.board = 'rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/PPPPPPPP/RNBQKBNR'
        if x:
            x = x.replace('2','11')
            x = x.replace('3','111')
            x = x.replace('4','1111')
            x = x.replace('5','11111')
            x = x.replace('6','111111')
            x = x.replace('7','1111111')
            x = x.replace('8','11111111')
            self.board = x

    def set_board(self, x):
        # import pdb; pdb.set_trace()
        fc = ord(x[0]) % 97
        tc = ord(x[3]) % 97
        fr = int(x[1]) - 1
        tr = int(x[4]) - 1
        f = (7 - fr) * 9 + fc
        t = (7 - tr) * 9 + tc
        if f > t:
            self.board = str(self.board[:t])+str(self.board[f])+\
                         str(self.board[t+1:f])+str(1)+\
                         str(self.board[f+1:])
        else:
            self.board = str(self.board[:f])+str(1)+\
                         str(self.board[f+1:t])+str(self.board[f])+\
                         str(self.board[t+1:])

if __name__ == "__main__":
    x = Board()
    print x.board
    x.set_board('a8-h3')
    x.set_board('h3-a8')
