'''
任务需求：返回所有可以走的步法--step类型的list，score不用管
'''
import constants

class chess:
    def __init__(self, belong, chess_type):
        self.belong = belong  # 属于那方
        self.chess_type = chess_type  # 是什么棋

    def can_move(self, to_x, to_y):  # 返回能不能往哪个地方走
        return False



class step:  # 走法类
    def __init__(self, from_x = -1, from_y = -1, to_x = -1, to_y = -1):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.score = 0

    def __cmp__(self, other):
        return self.score < other.score

    def __lt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, ",".join("{}={}".format(k, getattr(self, k)) for k in self.__dict__.keys()))


class chess_board:
    def __init__(self):
        self.board = []  # 棋盘
        self.flag = False
        for i in range(9):
            self.board.append([])
            for j in range(10):
                if(constants.init_borad[i][j] == 0):
                    self.board[i].append(chess(-1, constants.init_borad[i][j]))
                else:
                    self.board[i].append(chess(0 if j < 5 else 1, constants.init_borad[i][j]))

    def print_board(self, flag = False):
        for i in range(9):
            strr = ""
            for j in range(10):
                strr = strr + " " + str(self.board[i][j].chess_type)
            print(strr)
        if flag:
            for i in range(9):
                strr = ""
                for j in range(10):
                    strr = strr + " " + str(self.board[i][j].belong)
                print(strr)

    def IsKingFaceToFace(self, x, y, who):
        a = False
        if who == 1:
            for i in range(9, 6, -1):
                if self.board[x][i].chess_type == constants.jiang:
                    a = True
                    b = i
            if not a:
                return a
            for j in range(y + 1, b):
                if self.board[x][j].chess_type != constants.kong:
                    return False
            return b
        else:
            for i in range(0, 3):
                if self.board[x][i].chess_type == constants.jiang:
                    a = True
                    b = i
            if not a:
                return a
            for j in range(y - 1, b, -1):
                if self.board[x][j].chess_type != constants.kong:
                    return False
            return b

    def HaveFriend(self, x, y, who):
        if self.flag:
            return False
        if self.board[x][y].chess_type == 0:
            return False
        return self.board[x][y].belong == who

    def HaveMan(self, x, y):
        return self.board[x][y].chess_type != 0

    # 返回所有可行的走法, 一个step类型的list
    def generate_move(self, who):
        res_list = []
        for x in range(9):
            for y in range(10):
                if self.board[x][y].chess_type != 0:
                    if self.board[x][y].belong != who:
                        continue
                    list2 = self.get_chess_move(x, y, who)
                    res_list = res_list + list2
        return res_list

    def get_chess_move(self, x, y, who, tag=False):
        self.flag = tag
        list3 = []
        if self.board[x][y].chess_type == 1 and who == 0:
            i = self.IsKingFaceToFace(x, y, who)
            if i:
                list3.append(step(x, y, x, i))
            # 纵向
            x1 = x
            # 向前
            y1 = y + 1
            if y1 <= 2 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向后
            y1 = y - 1
            if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 横向
            y1 = y
            # 向左
            x1 = x - 1
            if x1 >= 3 and (not self.HaveFriend(x1, y1, who))and self.IsKingFaceToFace(x1, y1, who) == False:
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右
            x1 = x + 1
            if x1 <= 5 and (not self.HaveFriend(x1, y1, who))and self.IsKingFaceToFace(x1, y1, who) == False:
                s = step(x, y, x1, y1)
                list3.append(s)
        elif self.board[x][y].chess_type == 1 and (not who == 0):
            i = self.IsKingFaceToFace(x, y, who)
            if i:
                list3.append(step(x, y, x, i))
            # 纵向
            x1 = x
            # 向前
            y1 = y - 1
            if y1 >= 7 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向后
            y1 = y + 1
            if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 横向
            y1 = y
            # 向左
            x1 = x + 1
            if x1 <= 5 and (not self.HaveFriend(x1, y1, who))and self.IsKingFaceToFace(x1, y1, who) == False:
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右
            x1 = x - 1
            if x1 >= 3 and (not self.HaveFriend(x1, y1, who))and self.IsKingFaceToFace(x1, y1, who) == False:
                s = step(x, y, x1, y1)
                list3.append(s)
        elif self.board[x][y].chess_type == 2 and (not who == 0):
            # 纵向
            x1 = x
            # 向前
            for y1 in range(y-1, -1,-1):
                if self.HaveMan(x1, y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向后
            for y1 in range(y+1, 10):
                if self.HaveMan(x1, y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 横向
            y1 = y
            # 向左
            for x1 in range(x+1, 9):
                if self.HaveMan(x1, y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向右
            for x1 in range(x-1, -1, -1):
                if self.HaveMan(x1,y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
        elif self.board[x][y].chess_type == 2 and who == 0:
            # 纵向
            x1 = x
            # 向前
            for y1 in range(y+1, 10):
                if self.HaveMan(x1, y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向后
            for y1 in range(y-1, -1, -1):
                if self.HaveMan(x1, y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 横向
            y1 = y
            # 向左
            for x1 in range(x-1, -1, -1):
                if self.HaveMan(x1,y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向右
            for x1 in range(x+1, 9):
                if self.HaveMan(x1,y1):
                    if not self.HaveFriend(x1, y1, who):
                        s = step(x, y, x1, y1)
                        list3.append(s)
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
        elif self.board[x][y].chess_type == 3 and who == 0:
            #x2,y2是用来判断是否有蹩脚的
            x2 = x + 1
            y2 = y
            if x2 <= 7 and (not self.HaveMan(x2, y2)):
                # 横着向右上
                y1 = y + 1
                x1 = x + 2
                if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向右下
                y1 = y - 1
                x1 = x + 2
                if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x - 1
            y2 = y
            if x2 >= 1 and (not self.HaveMan(x2, y2)):
                # 横着向左上
                y1 = y + 1
                x1 = x - 2
                if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左下
                y1 = y - 1
                x1 = x - 2
                if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x
            y2 = y + 1
            if y2 <= 8 and (not self.HaveMan(x2, y2)):
                # 竖着向右上
                y1 = y + 2
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左上
                y1 = y + 2
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x
            y2 = y - 1
            if y2 >= 1 and (not self.HaveMan(x2, y2)):
                # 横着向右下
                y1 = y - 2
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左下
                y1 = y - 2
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
        elif self.board[x][y].chess_type == 3 and (not who == 0):
            # x2,y2用来判断是否有蹩脚的
            x2 = x - 1
            y2 = y
            if x2 >= 1 and (not self.HaveMan(x2, y2)):
                # 横着向右上
                y1 = y - 1
                x1 = x - 2
                if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向右下
                y1 = y + 1
                x1 = x - 2
                if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x + 1
            y2 = y
            if x2 <= 7 and (not self.HaveMan(x2, y2)):
                # 横着向左上
                y1 = y - 1
                x1 = x + 2
                if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左下
                y1 = y + 1
                x1 = x + 2
                if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x
            y2 = y + 1
            if y2 <= 8 and (not self.HaveMan(x2, y2)):
                # 竖着向右下
                y1 = y + 2
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左下
                y1 = y + 2
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)

            x2 = x
            y2 = y - 1
            if y2 >= 1 and (not self.HaveMan(x2, y2)):
                # 横着向右上
                y1 = y - 2
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 横着向左上
                y1 = y - 2
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
        elif self.board[x][y].chess_type == 4 and who == 0:
            # 纵向
            x1 = x
            # 向前
            for y1 in range(y+1, 10):
                if self.HaveMan(x1,y1):
                    for y2 in range(y1+1, 10):
                        if (not self.HaveFriend(x1, y2, who)) and self.HaveMan(x1, y2):
                            s = step(x, y, x1, y2)
                            list3.append(s)
                            break
                        if self.HaveFriend(x1, y2, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向后
            for y1 in range(y-1, -1, -1):
                if self.HaveMan(x1, y1):
                    for y2 in range(y1-1, -1, -1):
                        if (not self.HaveFriend(x1, y2, who)) and self.HaveMan(x1, y2):
                            s = step(x, y, x1, y2)
                            list3.append(s)
                            break
                        if self.HaveFriend(x1, y2, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 横向
            y1 = y
            # 向左
            for x1 in range(x-1, -1, -1):
                if self.HaveMan(x1, y1):
                    for x2 in range(x1-1, -1, -1):
                        if (not self.HaveFriend(x2, y1, who)) and self.HaveMan(x2, y1):
                            s = step(x, y, x2, y1)
                            list3.append(s)
                            break
                        if self.HaveFriend(x2, y1, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向右
            for x1 in range(x+1, 9):
                if self.HaveMan(x1, y1):
                    for x2 in range(x1+1, 9):
                        if (not self.HaveFriend(x2, y1, who)) and self.HaveMan(x2, y1):
                            s = step(x, y, x2, y1)
                            list3.append(s)
                            break
                        if self.HaveFriend(x2, y1, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
        elif self.board[x][y].chess_type == 4 and (not who == 0):
            # 纵向
            x1 = x
            # 向前
            for y1 in range(y-1, -1, -1):
                if self.HaveMan(x1, y1):
                    for y2 in range(y1-1, -1, -1):
                        if (not self.HaveFriend(x1, y2, who)) and self.HaveMan(x1, y2):
                            s = step(x, y, x1, y2)
                            list3.append(s)
                            break
                        if self.HaveFriend(x1, y2, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向后
            for y1 in range(y+1, 10):
                if self.HaveMan(x1, y1):
                    for y2 in range(y1+1, 10):
                        if (not self.HaveFriend(x1, y2, who)) and self.HaveMan(x1, y2):
                            s = step(x, y, x1, y2)
                            list3.append(s)
                            break
                        if self.HaveFriend(x1, y2, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 横向
            y1 = y
            # 向左
            for x1 in range(x+1, 9):
                if self.HaveMan(x1, y1):
                    for x2 in range(x1+1, 9):
                        if (not self.HaveFriend(x2, y1, who)) and self.HaveMan(x2, y1):
                            s = step(x, y, x2, y1)
                            list3.append(s)
                            break
                        if self.HaveFriend(x2, y1, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
            # 向右
            for x1 in range(x-1, -1, -1):
                if self.HaveMan(x1, y1):
                    for x2 in range(x1-1, -1, -1):
                        if (not self.HaveFriend(x2, y1, who)) and self.HaveMan(x2, y1):
                            s = step(x, y, x2, y1)
                            list3.append(s)
                            break
                        if self.HaveFriend(x2, y1, who):
                            break
                    break
                s1 = step(x, y, x1, y1)
                list3.append(s1)
        elif self.board[x][y].chess_type == 5 and who == 0:
            # 向左上
            x1 = x - 2
            y1 = y + 2
            if y1 <= 4 and x1 >= 0 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x-1, y+1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右上
            x1 = x + 2
            y1 = y + 2
            if y1 <= 4 and x1 <= 8 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x+1, y+1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向左下
            x1 = x - 2
            y1 = y - 2
            if y1 >= 0 and x1 >= 0 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x-1, y-1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右下
            x1 = x + 2
            y1 = y - 2
            if y1 >= 0 and x1 <= 8 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x+1, y-1)):
                s = step(x, y, x1, y1)
                list3.append(s)
        elif self.board[x][y].chess_type == 5 and (not who == 0):
            # 向左上
            x1 = x + 2
            y1 = y - 2
            if y1 >= 5 and x1 <= 8 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x+1, y-1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右上
            x1 = x - 2
            y1 = y - 2
            if y1 >= 5 and x1 >= 0 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x-1, y-1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向左下
            x1 = x + 2
            y1 = y + 2
            if y1 <= 9 and x1 <= 8 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x+1, y+1)):
                s = step(x, y, x1, y1)
                list3.append(s)
            # 向右下
            x1 = x - 2
            y1 = y + 2
            if y1 <= 9 and x1 >= 0 and (not self.HaveFriend(x1, y1, who)) and (not self.HaveMan(x-1, y+1)):
                s = step(x, y, x1, y1)
                list3.append(s)
        elif self.board[x][y].chess_type == 6 and who == 0:
            if x == 3:
                if not self.HaveFriend(4, 1, who):
                    s = step(x, y, 4, 1)
                    list3.append(s)
            elif x == 4:
                if not self.HaveFriend(3, 0, who):
                    s = step(x, y, 3, 0)
                    list3.append(s)
                if not self.HaveFriend(3, 2, who):
                    s = step(x, y, 3, 2)
                    list3.append(s)
                if not self.HaveFriend(5, 0, who):
                    s = step(x, y, 5, 0)
                    list3.append(s)
                if not self.HaveFriend(5, 2, who):
                    s = step(x, y, 5, 2)
                    list3.append(s)
            else:
                if not self.HaveFriend(4, 1, who):
                    s = step(x, y, 4, 1)
                    list3.append(s)
        elif self.board[x][y].chess_type == 6 and (not who == 0):
            if x == 3:
                if not self.HaveFriend(4, 8, who):
                    s = step(x, y, 4, 8)
                    list3.append(s)
            elif x == 4:
                if not self.HaveFriend(3, 9, who):
                    s = step(x, y, 3, 9)
                    list3.append(s)
                if not self.HaveFriend(3, 7, who):
                    s = step(x, y, 3, 7)
                    list3.append(s)
                if not self.HaveFriend(5, 9, who):
                    s = step(x, y, 5, 9)
                    list3.append(s)
                if not self.HaveFriend(5, 7, who):
                    s = step(x, y, 5, 7)
                    list3.append(s)
            else:
                if not self.HaveFriend(4, 8, who):
                    s = step(x, y, 4, 8)
                    list3.append(s)
        elif self.board[x][y].chess_type == 7 and who == 0:
            # 向前
            x1 = x
            y1 = y+1
            if y1 <= 9 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            if y >= 5:
                y1 = y
                # 向左
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 向右
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
        elif self.board[x][y].chess_type == 7 and (not who == 0):
            # 向前
            x1 = x
            y1 = y-1
            if y1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                s = step(x, y, x1, y1)
                list3.append(s)
            if y <= 4:
                y1 = y
                # 向左
                x1 = x + 1
                if x1 <= 8 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
                # 向右
                x1 = x - 1
                if x1 >= 0 and (not self.HaveFriend(x1, y1, who)):
                    s = step(x, y, x1, y1)
                    list3.append(s)
        return list3



if __name__ == "__main__":
    t = chess_board()
    # t.print_board()
    t.generate_move(True)
