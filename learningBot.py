##SCORE board
from cleanerAI import *
from heapq import *
import cleanerAI

global directs
di = [(1,0), (0,1), (1,-1), (1,1)]





def make_cells(board):
    cells = [[],[],[],[]]

    # Vertical
    for x in range(8):
        for start_y in range(0,4):
            set = []
            for y in range(5):
                set.append(board[start_y + y][x])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_y, x, 0]
                cells[0].append(set)
    # Horrizontal
    for y in range(8):
        for start_x in range(0,4):
            set = []
            for x in range(5):
                set.append(board[y][start_x + x])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [y, start_x, 1]
                cells[1].append(set)
    # /
    for x in range(4, 8):
        for start_x in range(0, x-3):
            set = []
            for i in range(5):
                set.append(board[i+start_x][x-start_x-i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_x, x - start_x, 2]
                cells[2].append(set)
    for y in range(1, 4):
        for start_y in range(0, 4-y):
            set = []
            for i in range(5):
                set.append(board[y + start_y + i][7-start_y -i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [ y + start_y, 7-start_y, 2]
                cells[2].append(set)
    # \

    for x in range(3, -1, -1):
        for start_x in range(0, 4-x):
            set = []
            for i in range(5):
                set.append(board[i+start_x][x+start_x+i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_x, x + start_x, 3]
                cells[3].append(set)
    for y in range(1, 4):
        for start_y in range(0, 4-y):
            set = []
            for i in range(5):
                set.append(board[y + start_y + i][start_y + i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [y + start_y, start_y, 3]
                cells[3].append(set)
    return cells



################################################################################
def seq_with(y,x, cells):
    ans = []

    for ver in cells[0]:
       if(x == ver[-2] and y >= ver[-3] and y < ver[-3] + 5 ):
           ans.append(ver)
    for hor in cells[1]:
       if(y == hor[-3] and x >= hor[-2] and x < hor[-2] + 5 ):
           ans.append(hor)
    for tr in cells[2]:
        dn = y - tr[-3]
        if(dn >= 0 and dn < 5 and dn == tr[-2] - x):
            ans.append(tr)
    for tl in cells[3]:
        dn = y - tl[-3]
        if(dn >= 0 and dn < 5 and dn == x - tl[-2]):
            ans.append(tl)
    return ans



cofs = [187.5, 200.0, 0.0, 0.0075, 187.5, 0.5]
def value1(gains):
    return(( cofs2[0] * gains[0][3] +
             cofs2[1] * gains[0][2] +
             cofs2[2] * gains[0][1] +
             cofs2[3] * gains[1][3] +
             cofs2[4] * gains[1][2] +
             cofs2[5] * gains[1][1]
    )/100)


def cpy_brd(brd):
    ans = []
    for i in brd:
        ans.append(i.copy())
    return ans

##^^^^old
################################################################################
################################################################################
################################################################################









def score_from_cells(y,x, cells, col, board):
    cells_in = seq_with(y,x, cells)
    gains = [{1:0, 2:0, 3:0}, {1:0, 2:0, 3:0}]
    supers = [{3:0},{3:0}]
    score = []

    for cell in cells_in:
        t = cell.count(col)
        e = cell.count(" ")
        if t == 4:
            return [[100], 100]
        if e == 1:
            score = [99]
        else:
            gains[t == 0][5 - e] += 1
            if(5 - e == 2):
                a = is_super(cell,y,x, board) # pos of own super
                if(a):
                    supers[t == 0][3] += 1

    if(gains[0][3] >= 2):
        score.append(98)
    if(gains[0][3] == 1 and supers[0][3] >= 1): # depends if they can make their two fours and take away your four
        score.append(97.5)
    if(gains[1][3] >= 2 or (supers[1][3] >= 1 and gains[1][3] >= 1)):
        score.append(97)
    if(supers[0][3] >= 2):
        score.append(96)
    if(supers[1][3] >= 2):
        score.append(95)
    if(supers[0][3] == 1 or gains[0][3] == 1):#victory contiues thrests is possible
        brd = cpy_brd(board)
        if(vct(brd, y, x, col, 1)):
            score.append(94)


    value = value1(gains)

    return [score, value]


def in_indx(y, x):# returns if x, y is in range of brd
    if(x >= 0 and y >= 0 and x < 8 and y < 8):
        return True
    return False



def is_super(cell, y, x, board):
    cell = cell.copy()
    dy = y - cell[5]
    dx = x - cell[6]
    if(di[cell[7]][0] == 0):
        dy = dx/di[cell[7]][1]
    else:
        dy = dy/di[cell[7]][0]
    cell[int(dy)] = 't'


    y_s, x_s = cell[5] -   di[cell[7]][0], cell[6] -   di[cell[7]][1]
    y_e, x_e = cell[5] + 5*di[cell[7]][0], cell[6] + 5*di[cell[7]][1]

    if(cell[0] != ' ' and cell[4] != ' '):
        return False
    if(cell[0] == ' ' and cell[4] == ' '):
        if(in_indx(y_s, x_s) and board[y_s][x_s] == ' '):
            return True
        if(in_indx(y_e, x_e) and board[y_e][x_e] == ' '):
            return True
    elif(cell[0] != ' '):
        if(in_indx(y_s, x_s) and board[y_s][x_s] == ' '):
            return True
    elif(cell[4] != ' '):
        if(in_indx(y_e, x_e) and board[y_e][x_e] == ' '):
            return True
    return False



# Makes a array of score based on board and col
def score_board(board, col, cells):
    scoreMap = []

    for y in range(8):
        for x in range(8):
            if(board[y][x] == ' '):
                scoreMap.append([score_from_cells(y,x,cells,col, board), y, x])
            else:
                scoreMap.append([[[],-1], y,x])
    return scoreMap


################################################################################
################################################################################
# looking ahead:
# returns true if you will win with continuos threats
def vct(board, y, x, col, depth):
    board[y][x] = col
    cells = make_cells(board)

    is_win = seq_with(y,x,cells)
    seq = {3:0, 4:0}
    for i in is_win:
        if(i.count(col) >= 5):
            return True
        if(i.count(col) == 4 or i.count(col) == 3):
            seq[i.count(col)] += 1
    if((seq[4] < 1 and seq[3] < 1)):
        return False

    if(depth > 3):
        return False

    # find all posible moves the opnt can make -> if unconclusive return false or if they win
    # will only go somwhere with 4/5, or to stop creation of 2 4/5's or to stop
    best_move = 0
    moves = []

    for y in range(8):
        for x in range(8):
            if(board[y][x] == ' '):
                score = special_score_from_cells(y,x,cells,['b','w'][col == 'b'], board)
                if(score == []):
                    continue
                elif(score[0] == 100):
                    return False

                if(score[0] > best_move):
                    best_move = score[0]
                    moves = [[score[0], y, x]]
                if(score[0] == best_move):
                    moves.append([score[0], y, x])

    # you will have a list of moves of value best_move to do
    if(moves == [] or best_move == 98 or best_move == 96 or best_move == 97.5):
        return False

    for move in moves:
        brd = cpy_brd(board)
        brd[move[1]][move[2]] = ['b','w'][col == 'b']
        a = False
        for oy in range(8):
            for ox in range(8):
                if(brd[oy][ox] == ' '):
                    brd2 = cpy_brd(brd)
                    if(vct(brd2,oy,ox,col, depth + 1)):
                        a = True
        if(not a):
            return False


    return True





def special_score_from_cells(y,x, cells, col, board):
    cells_in = seq_with(y,x, cells)
    gains = [{1:0, 2:0, 3:0}, {1:0, 2:0, 3:0}]
    supers = [{3:0},{3:0}]
    score = []

    for cell in cells_in:
        t = cell.count(col)
        e = cell.count(" ")
        if t == 4:
            return [100] # move to win
        if e == 1:
            score = [99]    # move to stop wins
        else:
            gains[t == 0][5 - e] += 1
            if(5 - e == 2):
                a = is_super(cell,y,x, board) # pos of own super
                if(a):
                    supers[t == 0][3] += 1

    if(gains[0][3] >= 2): # move to get 2 4/5's
        score.append(98)
    if(gains[0][3] == 1 and supers[0][3] >= 1): # depends if they can make their two fours and take away your four
        score.append(97.5)
    if(gains[1][3] >= 2):
        score.append(97)
    if(gains[1][3] >= 2 or (supers[1][3] >= 1 and gains[1][3] >= 1)):
        score.append(97)
    if(supers[0][3] >= 2):
        score.append(96)
    if(supers[1][3] >= 2):
        score.append(95)
    return score










################################################################################
def scoreMapBot(board, col):
    cells = make_cells(board)
    scoreMap = score_board(board, col, cells)

    try:
        best = scoreMap[0]
    except:
        return [[[0],0],0,0]
    best = max(scoreMap)
    if(best[0] > [[1],0]):
        return(best)
    return best


    '''
    # looks at score in nearby cells
    top_five_to_check = nlargest(5, scoreMap)
    ans = []
    for move in top_five_to_check:
        seq_in = seq_with(move[1],move[2],cells)
        indxs = []
        for cell in seq_in:
            for i in range(5):
                if(cell[i] == ' '):
                    temp = (cell[5] + i * di[cell[7]][0] )*8 + cell[6] + i * di[cell[7]][1]
                    if(temp not in indxs):
                        indxs.append(temp)
        arnd = 0
        for i in indxs:
            arnd += scoreMap[i][0][1]
        move[0][1] = move[0][1] + arnd#/(len(indxs)+1)
        ans.append(move)

    return max(ans)
    '''

    # looks at the scores around its vicinity
    '''
    top_five_to_check = nlargest(5, scoreMap)
    ans = []
    for move in top_five_to_check:
        for y in range(8):
            for x in range(8):
                dx = abs(x-move[2])
                dy = abs(y-move[2])
                points = 0
                if(dy <= 3 and dx <= 3):
                    if(scoreMap[y*8 + x][0][1] != -1):
                        points += scoreMap[y*8 + x][0][1]
                move[0][0] = move[0][1] + points/10
                ans.append(move)
    return max(ans)
    '''


################################################################################
def bot6(board, col):
    best = scoreMapBot(board, col)
    return(best[1], best[2])

































cofs2 = cofs.copy()
def trainer(iterr):
    global cofs2, cofs
    perc = [0, 0.25, 0.50, 0.75, 1, 1, 1, 1.5, 2, 5, 10]


    for i in range(iterr):
        # apply random multiplyer

        for i in range(len(cofs2)):
            cofs2[i] = cofs[i] * perc[int(random.random()*11)]
        print(cofs2)

        res = cleanerAI.bot_v_bot_n_times(bot6, bot2.bot2, 25)
        if(res[2] < res[1]):

            res = cleanerAI.bot_v_bot_n_times(bot6, bot2.bot2, 100)
            if(res[0] < 190 and res[1] - res[2] > 0):# bot 1 is likely better

                res = cleanerAI.bot_v_bot_n_times(bot6, bot2.bot2, 500)
                if(res[0] < 950 and res[1] - res[2] > 0):# bot 1 is lot likely better

                    res = cleanerAI.bot_v_bot_n_times(bot6, bot2.bot2, 1000)
                    if(res[0] < 1900 and res[1] - res[2] > 0): # bot 1 is lot lot likely better
                        cofs = cofs2.copy()
                        print(cofs)
                        print("HEREHEREHERE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    return cofs