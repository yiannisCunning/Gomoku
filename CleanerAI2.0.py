from gomoku import *
## INFO:
# cells     -> [ver, hor, /, \]          --> does not include multicolor cells
# a cell    -> list of format: (_,_,_,_,_,y,x)

# STRATAGY:
# 1) Move hiearchy -> dont even have to bother with 'scores'.
#                     Just need to make sure highest on the list is done
# 2) Go into depth on possible moves: (check higher score first)
#       you go somwhere -> see where board will go with hierchy moves.
#       would then return the final board state score.
#             -> if I go here will they be guaranteed to go somwhere else?
#                    -> no = just return score of that pos
#                    -> yes = make their move for them and recalculate your score


################################################################################
## BOT 4:
def score_from_cells_bot_4(y,x, cells, col, prev, board):
    cells_in = seq_with(y,x, cells)
    gains = [{1:0, 2:0, 3:0}, {1:0, 2:0, 3:0}]# own, enemys
    score = []

    # max of 15 - (unlikely)

    for cell in cells_in:
        t = cell.count(col)
        e = cell.count(" ")
        if t == 4:
            return 100, 100
        if e == 1:
            score = [99]
        else:
            gains[t == 0][5 - e] += 1


    if(gains[0][3] >= 2):
        score.append(98)
    if(gains[1][3] >= 2):
        score.append(97)

    value = (( 300 * gains[0][3] +
             20 * gains[0][2] +
             5  * gains[0][1] +
             90 * gains[1][3] +
             10 * gains[1][2] +
             1 * gains[1][1]
    )/100)

    if(prev[0][0] == [] and score == []):
        future_score = opnt_move_after(board, col, y, x)
        if(future_score != -1):
            return [], future_score


    return score, value
    # once again amount is better


################################################################################
# main

def bot4(board, col):
    ans = [[[],-1], 0, 0]
    cells = make_cells(board)

    for y in range(len(board)):
        for x in range(len(board[1])):
            if(board[y][x] == " "): # for every open square
                score, value = score_from_cells_bot_4(y,x,cells,col, ans, board)
                if(score == 100):
                    return y,x
                if(score > ans[0][0]):
                    ans = [[score,value],y,x]
                elif(score == ans[0][0] and value > ans[0][1]):
                    ans = [[score, value],y,x]

    #print(ans)
    return (ans[1], ans[2])









################################################################################
# returns board after garanteed move or -1 if none
def opnt_move_after(board, col, y, x):
    ans = [[[],0], 0, 0] # [priority, val], y, x

    brd = []
    for i in board:
        brd.append(i.copy())
    brd[y][x] = col
    cells = make_cells(brd)
    col = ['b', 'w'][col == 'b']


    for y in range(len(brd)):
        for x in range(len(brd[1])):
            if(brd[y][x] == " "): # for every open square
                pq, val = score_from_cells_nodep(y, x, cells, col, ans)
                if(pq == 100):
                    return -1
                if(pq > ans[0][0]):
                    ans = [[pq,val],y,x]
                elif(pq == ans[0][0] and val > ans[0][1]):
                    ans = [[pq, val],y,x]

    if(ans[0][0] == []):
        return -1


    brd[ans[1]][ans[2]] = col
    cells = make_cells(brd)
    col = ['b', 'w'][col == 'b']
    ans = [[[],0], 0, 0]

    for y in range(len(brd)):
        for x in range(len(brd[1])):
            if(brd[y][x] == " "): # for every open square
                pq, val = score_from_cells_nodep(y, x, cells, col, ans)
                if(pq == 100):
                    return 100
                if(pq > ans[0][0]):
                    ans = [[pq,val],y,x]
                elif(pq == ans[0][0] and val > ans[0][1]):
                    ans = [[pq, val],y,x]

    if(ans[0][0] == []):
        return ans[0][1]
    elif(ans[0][0][0] == 100 or ans[0][0][0] == 98):
        return ans[0][0][0]
    return -1


def score_from_cells_nodep(y,x, cells, col, prev):
    cells_in = seq_with(y,x, cells)
    gains = [{1:0, 2:0, 3:0}, {1:0, 2:0, 3:0}]# own, enemys
    score = []

    # max of 15 - (unlikely)

    for cell in cells_in:
        t = cell.count(col)
        e = cell.count(" ")
        if t == 4:
            return 100, 100
        if e == 1:
            score = [99]
        else:
            gains[t == 0][5 - e] += 1


    if(gains[0][3] >= 2):
        score.append(98)
    if(gains[1][3] >= 2):
        score.append(97)

    value = (( 300 * gains[0][3] +
             20 * gains[0][2] +
             5  * gains[0][1] +
             90 * gains[1][3] +
             10 * gains[1][2] +
             1 * gains[1][1]
    )/100)

    return score, value


################################################################################