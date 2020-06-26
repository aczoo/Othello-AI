import random
import math
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
N,S,E,W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N,NE,E,SE,S,SW,W,NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}
best = {BLACK: max, WHITE: min}
SCORE=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 150, -20, 20, 5, 5, 20, -20,150, 0,
 0, -20, -20, -5, -5, -5, -5, -20, -20, 0,
 0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
 0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
 0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
 0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
 0, -20, -20, -5, -5, -5, -5, -20, -20, 0,
 0, 150, -20, 20, 5, 5, 20, -20, 150, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

class Node:
   def __init__(self,state,player, move,score):
      self.state =state
      self.score= score
      self.move = move
      self.player = player
      self.children=[]
   def __lt__(self, other):
      return self.score<other.score
class Strategy():

    def __init__(self):
        pass

    def get_starting_board(self):
        return("???????????........??........??........??...o@...??...@o...??........??........??........???????????")

    def get_pretty_board(self, board):
        temp  = ""
        for x in range(10):
            temp+= board[x*10:x*10+10]+"\n"
        return temp

    def opponent(self, player):
        p = ["@", "o"]
        return p[(p.index(player)+1)%2]

    def find_match(self, board, player, square, direction):
        marker = square+direction
        case =False
        while board[marker]==self.opponent(player):
            marker+=direction
            case = True
        if case ==True and board[marker] =='.':
            return marker
        return False
    def make_move(self, board, player, move):
        board="".join(board[:move])+player+"".join(board[move+1:])
        for x in DIRECTIONS:
            temp=move
            while board[temp+x]==self.opponent(player):
                temp+=x
            if board[temp+x]==player:
                while board[temp]==self.opponent(player):
                    board="".join(board[:temp])+player+"".join(board[temp+1:])
                    temp-=x
        return board
    def get_valid_moves(self, board, player):
        valid = set()
        empty = [x for x in range(len(board)) if board[x]==player]
        for x in empty:
            for y in DIRECTIONS:
               valid.add(self.find_match( board, player, x, y))
        valid.discard(False)
        
        return list(valid)
    def has_any_valid_moves(self, board, player):
        if len(self.get_valid_moves( board, player)):
            return True
        return False
    def next_player(self, board, prev_player):
        opp=self.opponent(prev_player)
        if self.has_any_valid_moves(board, opp):
            return opp
        elif self.has_any_valid_moves(board, prev_player):
            return prev_player
        return None
    def score(self, board, player=BLACK):
        return board.count("@")- board.count("o") 
    def weightedscore(self, board, matrix):
        temp1=0
        temp2=0
        for x in range(100):
           if board[x]==BLACK:
              temp1+=matrix[x]
           elif board[x]==WHITE:
              temp2+=matrix[x]
        return temp1-temp2
              
    def game_over(self, board, player):
        if self.next_player(board, player)== None:
            return True
        return False
    def updateMatrix(self,board, player, move, prevmatrix):
        for x in [a for a in range(len(prevmatrix)) if prevmatrix[a]==150]:
           if move==x and ((player in (board[x-10], board[x+10] ,board[x+1] ,board[x-1])) or (x in (11,18,81,88))):
              for y in DIRECTIONS:
                 if prevmatrix[x+y]>0:
                    prevmatrix[x+y]=150
        return prevmatrix
                    
    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    def minmax_strategy(self, board, player, depth=4, m = None):
        nodeboard = Node(board, player,None, None)
        if depth == 0:
           nodeboard.score= self.score(board)
           return nodeboard
        else:
           my_moves = self.get_valid_moves(board, player)
           children = []
           for move in my_moves:
              next_board = self.make_move(board, player, move)
              next_player = self.next_player(next_board, player)
              if next_player ==None :
                 c =  Node(next_board, player, move,1000*self.score(next_board))
                 children.append(c)
              else:
                 c = Node(next_board,player, move, None)
                 c.score = self.minmax_strategy(next_board, next_player,depth-1, move).score
                 children.append(c)
           winner = best[player](children)
           return winner
    def alphabetapruning(self, board, player, depth, m =None,alpha=-math.inf, beta=math.inf, parent=None, matrix = SCORE):
        nodeboard = Node(board, player,m, None)
        if depth == 0:
           nodeboard.score= self.weightedscore(board, matrix)
           return nodeboard
        else:
           my_moves = self.get_valid_moves(board, player)
           children = []
           for move in my_moves:
              next_board = self.make_move(board, player, move)
              next_player = self.next_player(next_board, player)
              if next_player ==None :
                 c =  Node(next_board, player, move,1000*self.score(next_board))
                 children.append(c)
              else:
                 c = Node(next_board,player, move, None)
                 newscorematrix = self.updateMatrix(board, player, move, matrix);
                 c.score = self.alphabetapruning(next_board, next_player,depth-1,move,alpha, beta, player,newscorematrix).score
                 children.append(c)
              if best[player]==max:
                 alpha = max(alpha, c.score)
              elif best[player]==min:
                 beta = min(beta, c.score)
              if alpha>=beta:
                 break
           winner = best[player](children)
           return winner
         
    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))
      
    
    def alphabetapruning3(self, board, player, depth, m =None,alpha=-math.inf, beta=math.inf, parent=None, matrix = SCORE):
        nodeboard = Node(board, player,m, None)
        if depth == 0:
           nodeboard.score = self.weightedscore(board, matrix)
           if parent == self.next_player(board, player):
              if parent =="@":
                 nodeboard.score+=len(self.get_valid_moves(board, parent))*3
              else:
                 nodeboard.score-=len(self.get_valid_moves(board, parent))*3
           else:
              op = self.opponent(parent)
              if parent =="@":
                 nodeboard.score-=len(self.get_valid_moves(board, op))*3
              else:
                 nodeboard.score+=len(self.get_valid_moves(board, op))*3
           return nodeboard
        else:
           my_moves = self.get_valid_moves(board, player)
           children = []
           for move in my_moves:
              next_board = self.make_move(board, player, move)
              next_player = self.next_player(next_board, player)
              if next_player ==None :
                 c =  Node(next_board, player, move,1000*self.score(next_board))
                 children.append(c)
              else:
                 c = Node(next_board,player, move, None)
                 newscorematrix = self.updateMatrix(board, player, move, matrix);
                 c.score = self.alphabetapruning3(next_board, next_player,depth-1,move,alpha, beta, player,newscorematrix).score
                 children.append(c)
              if best[player]==max:
                 alpha = max(alpha, c.score)
              elif best[player]==min:
                 beta = min(beta, c.score)
              if alpha>=beta:
                 break
           winner = best[player](children)
           return winner


         
    def best_strategy(self, board, player, best_move, still_running):
        depth = 3
        while(True):
            best_move.value = self.alphabetapruning3(board, player, depth).move
            depth += 1

    standard_strategy = alphabetapruning3
import time
from multiprocessing import Value, Process
import os, signal
silent = False


#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################
class StandardPlayer():
    def __init__(self):
        pass

    def play(self):
        ### create 2 opponent objects and one referee to play the game
        ### these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.alphabetapruning3, WHITE: white.minmax_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player).move
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.score(board))
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board)>0 else "White"))



#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer():

    def __init__(self, time_limit = 5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK
                    

        print("Playing Parallel Game")
        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.best_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent: print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent:print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent: print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))

if __name__ == "__main__":
    # game =  ParallelPlayer(0.1)
    game = StandardPlayer()
    game.play()
