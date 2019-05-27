from graphics import *
import sys

width_grid = 45
col = 15
row = 15


list_AI = []  # AI
list_human = []  # human
list_total = []  # total
list_all = []  #All points in play board
optimal_step = [0, 0]  #The optimal next step for AI.
ratio = 1  # Attack coeffiencience


# evaluate score
Score_evaluation_list = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


def AI():
    global cut_count   # count the cut times
    cut_count = 0
    global search_count   # count search times
    search_count = 0
    negative_max(True, DEPTH, -99999999, 99999999)
    print(" Cut times：" + str(cut_count))
    print(" Search times：" + str(search_count))
    return optimal_step[0], optimal_step[1]


# Negative max search, alpha + beta pruning algorithm
def negative_max(is_ai, depth, alpha, beta):
    # game over or search depth is zero
    if game_win(list_AI) or game_win(list_human) or depth == 0:
        return evaluation(is_ai)

    candidate_list = list(set(list_all).difference(set(list_total))) # candidate_list have the nodes in list_all but not in list_total
    order(candidate_list)   # search order sort , increase the efficiency of cutting
    # literate every candidate step
    for next_step in candidate_list:

        global search_count
        search_count += 1

        # it there is no chess besides the evaluate position, then don't evaluate. decrease the calculation
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list_AI.append(next_step)
        else:
            list_human.append(next_step)
        list_total.append(next_step)

        value = -negative_max(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list_AI.remove(next_step)
        else:
            list_human.remove(next_step)
        list_total.remove(next_step)

        if value > alpha:

            print("Current value:"+ str(value) + " Alpha:" + str(alpha) + " Beta:" + str(beta))
            if depth == DEPTH:
                optimal_step[0] = next_step[0]
                optimal_step[1] = next_step[1]
            # alpha + beta cut point
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value
    return alpha


#  the neighbor position of the last step has the most possibility to be optimal
def order(candidate_list):
    last_pt = list_total[-1]
    temp = 0
    while temp < len(candidate_list):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in candidate_list:
                    candidate_list.remove((last_pt[0] + i, last_pt[1] + j))
                    candidate_list.insert(0, (last_pt[0] + i, last_pt[1] + j))
        temp=temp+1


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list_total:
                return True
    return False


# evaluation function
def evaluation(is_ai):
    if is_ai:
        my_list = list_AI
        enemy_list = list_human
    else:
        my_list = list_human
        enemy_list = list_AI

    # calculate own score
    score_all_arr = []  # the position of getting score, if there is intersection, then the score will be double
    current_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        current_score += Score_calculation(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        current_score += Score_calculation(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        current_score += Score_calculation(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        current_score += Score_calculation(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  calculate the enemy's score and minus it.
    score_all_arr_enemy = []
    enecurrent_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enecurrent_score += Score_calculation(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enecurrent_score += Score_calculation(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enecurrent_score += Score_calculation(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enecurrent_score += Score_calculation(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = current_score - enecurrent_score*ratio*0.1

    return total_score


# the score calculation in each direction
def Score_calculation(m, n, x_direction, y_direction, enemy_list, my_list, score_all_arr):
    add_score = 0  # add_score
    # choose the biggest score in one direction
    max_score_shape = (0, None)
    # if there is a score shape in the direction, then don't calculate again.
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_direction == item[2][0] and y_direction == item[2][1]:
                return 0

    # literate left and right of the last step to search score shape
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in Score_evaluation_list:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_direction, n + (0+offset) * y_direction),
                                               (m + (1+offset) * x_direction, n + (1+offset) * y_direction),
                                               (m + (2+offset) * x_direction, n + (2+offset) * y_direction),
                                               (m + (3+offset) * x_direction, n + (3+offset) * y_direction),
                                               (m + (4+offset) * x_direction, n + (4+offset) * y_direction)), (x_direction, y_direction))

    #calculate the intersection, if two live three intersect, increase score
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(list):
    for m in range(col):
        for n in range(row):
            if n < row - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < row - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < row - 4 and n < row - 4 and (m, n) in list and (m + 1, n + 1) in list and (m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < row - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False


def gobangwindow():
    win = GraphWin("AI_project_Gobang_Game", width_grid * col, width_grid * row)
    win.setBackground("green")
    i1 = 0

    while i1 <= width_grid * col:
        l = Line(Point(i1, 0), Point(i1, width_grid * col))
        l.draw(win)
        i1 = i1 + width_grid
    i2 = 0

    while i2 <= width_grid * row:
        l = Line(Point(0, i2), Point(width_grid * row, i2))
        l.draw(win)
        i2 = i2 + width_grid
    return win


def main():
    global DEPTH
    DEPTH=1
    if len(sys.argv) > 1:
        if sys.argv[1] == 'hard':
            DEPTH = 3
    win = gobangwindow()

    for i in range(col+1):
        for j in range(row+1):
            list_all.append((i, j))

    change = 0
    g = 0

    while g == 0:

        if change % 2 == 1:
            pos = AI()

            if pos in list_total:
                message = Text(Point(200, 200), "It is not valid position" + str(pos[0]) + "," + str(pos[1]))
                message.draw(win)
                g = 1

            list_AI.append(pos)
            list_total.append(pos)

            chess = Circle(Point(width_grid * pos[0], width_grid * pos[1]), 16)
            chess.setFill('white')
            chess.draw(win)

            if game_win(list_AI):
                message = Text(Point(120, 100), "AI_Agent win.")
                message.setStyle("bold")
                message.setSize(20)
                message.draw(win)
                g = 1
            change = change + 1

        else:
            p2 = win.getMouse()
            if not ((round((p2.getX()) / width_grid), round((p2.getY()) / width_grid)) in list_total):

                a2 = round((p2.getX()) / width_grid)
                b2 = round((p2.getY()) / width_grid)
                list_human.append((a2, b2))
                list_total.append((a2, b2))

                chess = Circle(Point(width_grid * a2, width_grid * b2), 16)
                chess.setFill('black')
                chess.draw(win)
                if game_win(list_human):
                    message = Text(Point(120, 100), "Human win.")
                    message.setStyle("bold")
                    message.setSize(20)
                    message.draw(win)
                    g = 1

                change = change + 1

    message = Text(Point(120, 140), "Click to quit the Game.")
    message.setStyle("bold")
    message.setSize(15)
    message.draw(win)
    win.getMouse()
    win.close()


main()
