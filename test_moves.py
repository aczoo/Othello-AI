import strategy as ai

ref = ai.Strategy()
next_board = ref.get_starting_board()
infile = open("moves.txt", "r")
counter = 0
for line in infile.readlines():
    counter += 1
    board, player, move = line.strip().split(" ")
    print("testing line %i" % counter)
    assert(board == next_board)
    next_board = ref.make_move(board, player, int(move))
if counter == 60: print("All Tests Pass!")
infile.close()
