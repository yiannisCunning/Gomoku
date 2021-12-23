##SCORE board
from cleanerAI import *
from heapq import *
import cleanerAI
import bot2

def make_cells(board):
    cells = [[],[],[],[]]

    # Vertical
    for x in range(8):
        for start_y in range(0,4):
            set = []
            for y in range(5):
                set.append(board[start_y + y][x])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_y, x]
                cells[0].append(set)
    # Horrizontal
    for y in range(8):
        for start_x in range(0,4):
            set = []
            for x in range(5):
                set.append(board[y][start_x + x])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [y, start_x]
                cells[1].append(set)
    # /
    for x in range(4, 8):
        for start_x in range(0, x-3):
            set = []
            for i in range(5):
                set.append(board[i+start_x][x-start_x-i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_x, x - start_x]
                cells[2].append(set)
    for y in range(1, 4):
        for start_y in range(0, 4-y):
            set = []
            for i in range(5):
                set.append(board[y + start_y + i][7-start_y -i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [ y + start_y, 7-start_y]
                cells[2].append(set)
    # \

    for x in range(3, -1, -1):
        for start_x in range(0, 4-x):
            set = []
            for i in range(5):
                set.append(board[i+start_x][x+start_x+i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [start_x, x + start_x]
                cells[3].append(set)
    for y in range(3, 0, -1):
        for start_y in range(0, 4-y):
            set = []
            for i in range(5):
                set.append(board[y + start_y + i][start_y + i])
            if(set != [" "," "," "," "," "] and (set.count("b") == 0 or set.count("w") == 0)):
                set = set + [y + start_y, start_y]
                cells[3].append(set)
    return cells


def seq_with(y,x, cells):
    ans = []

    for ver in cells[0]:
       if(x == ver[-1] and y >= ver[-2] and y < ver[-2] + 5 ):
           ans.append(ver)
    for hor in cells[1]:
       if(y == hor[-2] and x >= hor[-1] and x < hor[-1] + 5 ):
           ans.append(hor)
    for tr in cells[2]:
        dn = y - tr[-2]
        if(dn >= 0 and dn < 5 and dn == tr[-1] - x):
            ans.append(tr)
    for tl in cells[3]:
        dn = y - tl[-2]
        if(dn >= 0 and dn < 5 and dn == x - tl[-1]):
            ans.append(tl)
    return ans


cofs = [187.5, 200.0, 0.01, 0.0075, 187.5, 0.5]
def value1(gains):
    return(( cofs[0] * gains[0][3] +
             cofs[1] * gains[0][2] +
             cofs[2] * gains[0][1] +
             cofs[3] * gains[1][3] +
             cofs[4] * gains[1][2] +
             cofs[5] * gains[1][1]
    )/100)




##^^^^old
################################################################################
def score_from_cells(y,x, cells, col):
    cells_in = seq_with(y,x, cells)
    gains = [{1:0, 2:0, 3:0}, {1:0, 2:0, 3:0}]
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

    if(gains[0][3] >= 2):
        score.append(98)
    if(gains[1][3] >= 2):
        score.append(97)
    value = value1(gains)

    return [score, value]




## Makes a array of score based on board and col
def score_board(board, col):
    scoreMap = []

    # could also use a array -> to make copy/find easyer
    # could also store the opnts scores in the brd

    cells = make_cells(board)
    for y in range(8):
        for x in range(8):
            if(board[y][x] == ' '):
                #heappush(scoreMap, (score_from_cells(y,x,cells,col),y,x))
                scoreMap.append([score_from_cells(y,x,cells,col),y,x])
    return scoreMap


def copy_brd(board):
    ans = []
    for i in board:
        ans.append(i.copy())
    return ans





def scoreMapBot(board, col, first):
    scoreMap = score_board(board, col)
    try:
        best = scoreMap[0]
    except:
        return [[[0],0],0,0]


    best = max(scoreMap)
    if(best[0] > [[1],0]):
        return(best)

    if(not first):
        return best

    top_five_to_check = nlargest(5, scoreMap)

    # if(top_five_to_check[0][0] == ([], 0)):
    #     return top_five_to_check[0]


    top_five = []
    for i in top_five_to_check:
        brd = copy_brd(board)
        brd[i[1]][i[2]] = col
        a = scoreMapBot(brd, ['b', 'w'][col == 'b'], False)

        if(a[0] > [[1],0]):
            brd[a[1]][a[2]] = ['b', 'w'][col == 'b']
            new_score = scoreMapBot(brd, col, True)

            if(new_score[0] > [[1],0]):

                top_p = new_score[0][0][0]
                if(top_p == 100):
                    i[0][0] = [100]
                    i[0][1] = i[0][1] - a[0][1] + new_score[0][1]
                    top_five.append(i)
                    continue
                if(top_p == 98):
                    i[0][0] = [98]
                    top_five.append(i)
                    i[0][1] = i[0][1] - a[0][1] + new_score[0][1]
                    continue

            i[0][1] = i[0][1] - a[0][1] + new_score[0][1]
            top_five.append(i)

        else:
            i[0][1] = i[0][1] - a[0][1]
            top_five.append(i)

    return max(top_five)





def bot5(board, col):
    best = scoreMapBot(board, col, True)
    return(best[1], best[2])























global cofs2
cofs2 = cofs.copy()
def trainer(iterr):
    global cofs2, cofs
    perc = [0, 0.25, 0.50, 0.75, 1, 1, 1, 1.5, 2, 5, 10]


    for i in range(iterr):
        # apply random multiplyer

        for i in range(len(cofs2)):
            cofs2[i] = cofs[i] * perc[int(random.random()*11)]
        print(cofs2)

        res = bot_v_bot_n_times(bot5, bot2.bot2, 25)
        if(res[2] < res[1]):

            res = bot_v_bot_n_times(bot5, bot2.bot2, 100)
            if(res[0] < 190 and res[1] - res[2] > 0):# bot 1 is likely better

                res = bot_v_bot_n_times(bot5, bot2.bot2, 500)
                if(res[0] < 950 and res[1] - res[2] > 0):# bot 1 is lot likely better

                    res = bot_v_bot_n_times(bot5, bot2.bot2, 1000)
                    if(res[0] < 1900 and res[1] - res[2] > 0): # bot 1 is lot lot likely better
                        cofs = cofs2.copy()
                        print(cofs)
                        print("sdffffffff<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    return cofs



