
def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
# ^----- setup and print -----^
# ------------------------------------------------------------------------------







# puts sequence on board
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

# checks if board is empty
def is_empty(board):
    for row in board:
        if(row.count(" ") != len(row)):
            return False
    return True

# checks if board is full
def is_full(board):
    for row in board:
        if(row.count(" ") != 0):
            return False
    return True

# returns opposite col
def op_col(col):
    if col == "b":
        return "w"
    else:
        return "b"

# if x, y is in board
def in_indx(brd, x, y):# returns if x, y is in range of brd
    if(x >= 0 and y >= 0 and x < len(brd[0]) and y < len(brd[0])):
        return True
    return False





# ^------- easy functions -------^
# ------------------------------------------------------------------------------





# returns if seq is open/semi/closed
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    color = board[y_end][x_end]
    empty = 2
    temp_y = y_end - length*d_y
    temp_x = x_end - length*d_x
    if(in_indx(board, temp_x, temp_y) == True):
        if(board[temp_y][temp_x] != " "):
            empty-=1
    else:
        empty -= 1

    temp_y = y_end + d_y
    temp_x = x_end + d_x
    if(in_indx(board, temp_x, temp_y) == True):
        if(board[temp_y][temp_x] != " "):
            empty -= 1
    else:
        empty -= 1

    return ["CLOSED","SEMIOPEN","OPEN"][empty]



# counts simi/open in 'row'
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    ans = {"OPEN":0, "CLOSED":0, "SEMIOPEN":0} # open, semiopen
    temp_x = x_start
    temp_y = y_start
    curRun = 0

    while(in_indx(board, temp_x, temp_y) == True):
        if(board[temp_y][temp_x] == col):
            curRun +=1
        else:
            if(curRun == length):
                ans[is_bounded(board, temp_y-d_y, temp_x-d_x, length, d_y, d_x)] += 1
            curRun = 0
        temp_y += d_y
        temp_x += d_x

    if(curRun == length):
        ans[is_bounded(board, temp_y-d_y, temp_x-d_x, length, d_y, d_x)] += 1

    return (ans["OPEN"], ans["SEMIOPEN"])




# counts total open/semi-open on whole board
def detect_rows(board, col, length):
    color = col
    ans = [0,0,0]#closed, semi, open
    directions = [[1,0], [0,1], [1,1], [1,-1]]

    for y in range(len(board)):
        for x in range(len(board[1])):

            # for each tile of 'color'
            if(board[y][x] == color):
                for dxdy in directions:

                    # first check if there is seq of 'color' in direction, with length
                    cond1 = True
                    for i in range(1, length):
                        temp_y = y + dxdy[0]*i
                        temp_x = x + dxdy[1]*i
                        if(in_indx(board, temp_x, temp_y) == True):
                            if(board[temp_y][temp_x] != color):
                                cond1 = False
                                break
                        else:
                            cond1 = False
                            break

                    if(cond1 == False):
                        continue


                    # Next look at square before and after to see if its open/semi/closed
                    empty = 2
                    temp_y = y - dxdy[0]
                    temp_x = x - dxdy[1]
                    if(in_indx(board, temp_x, temp_y) == True):
                        sqr_before = board[temp_y][temp_x]
                    else:
                        sqr_before = op_col(color)

                    temp_y = y + length*dxdy[0]
                    temp_x = x + length*dxdy[1]
                    if(in_indx(board, temp_x, temp_y) == True):
                        sqr_after = board[temp_y][temp_x]
                    else:
                        sqr_after = op_col(color)




                    if(sqr_before == color or sqr_after == color):
                        continue
                    if(sqr_before == op_col(color)):
                        empty -=1
                    if(sqr_after == op_col(color)):
                        empty -=1

                    ans[empty] += 1

    return ((ans[2],ans[1]))


# ------------------------------------------------------------------------------






# returns if somone won
def is_win(board):
    for col in ["w", "b"]:
        for k in range(5, len(board)+1):
            temp = open_closed(board, k, col)
            if(temp.count(0) < 3 and col == "w"):
                return "White won"
            if(temp.count(0) < 3 and col == "b"):
                return "Black won"

    if(is_full(board) == True):
        return "Draw"

    return "Continue playing"


# Returns number of [closed, open] seq of 'color' and 'length'
def open_closed(board, length, color):
    ans = [0,0,0]#closed, semi, open
    correct = " " + color*length + " "
    directions = [[1,0], [0,1], [1,1], [1,-1]]


    for y in range(len(board)):
        for x in range(len(board[1])):

            # for each tile of 'color'
            if(board[y][x] == color):
                for dxdy in directions:

                    # first check if there is seq of 'color' in direction, with length
                    cond1 = True
                    for i in range(1, length):
                        temp_y = y + dxdy[0]*i
                        temp_x = x + dxdy[1]*i
                        if(in_indx(board, temp_x, temp_y) == True):
                            if(board[temp_y][temp_x] != color):
                                cond1 = False
                                break
                        else:
                            cond1 = False
                            break

                    if(cond1 == False):
                        continue


                    # Next look at square before and after to see if its open/semi/closed
                    empty = 2
                    temp_y = y - dxdy[0]
                    temp_x = x - dxdy[1]
                    if(in_indx(board, temp_x, temp_y) == True):
                        sqr_before = board[temp_y][temp_x]
                    else:
                        sqr_before = op_col(color)

                    temp_y = y + length*dxdy[0]
                    temp_x = x + length*dxdy[1]
                    if(in_indx(board, temp_x, temp_y) == True):
                        sqr_after = board[temp_y][temp_x]
                    else:
                        sqr_after = op_col(color)




                    if(sqr_before == color or sqr_after == color):
                        continue
                    if(sqr_before == op_col(color)):
                        empty -=1
                    if(sqr_after == op_col(color)):
                        empty -=1

                    #print(x,y)
                    ans[empty] += 1

    return ans




# ------------------------------------------------------------------------------


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))




