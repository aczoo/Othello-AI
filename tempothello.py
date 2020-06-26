import random
import math

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
N,S,E,W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N,NE,E,SE,S,SW,W,NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}
class Strategy():

    def __init__(self):
        pass

    def get_starting_board(self):
        return("?"*10+("?"+"."*8+"?")*3+("?"+"."*3+"@o"+"."*3+"?")+("?"+"."*3+"o@"+"."*3+"?")+("?"+"."*8+"?")*3+"?"*10)

    def get_pretty_board(self, board):
        for x in range(10):
            print (board[x*10:x*10+10])

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
    'def is_move_valid(self, board, player, move):'
    def make_move(self, board, player, move):
        board[move] =player
        return board
    def get_valid_moves(self, board, player):
        valid = set()
        filled = [x for x in range(len(board)) if board[x]==player]
        for x in filled:
            for y in DIRECTIONS:
                valid.add(self.find_match( board, player, x, y))
        valid.discard(None)
        return valid
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

    def score(self, board, player=BLACK):
        return board.count("@")- board.count("o") 

    def game_over(self, board, player):
        if self.next_player(board, player)== None:
            return True
        return False
    
    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    def minmax_search(self, board, player, depth):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        pass

    def minmax_strategy(self, board, player, depth):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        pass
    
    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        depth = 1
        while(True):
            ## doing random in a loop is pointless but it's just an example
            best_move.value = self.random_strategy(board, player)
            depth += 1

    standard_strategy = random_strategy


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
        strategy = {BLACK: black.standard_strategy, WHITE: white.standard_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
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

