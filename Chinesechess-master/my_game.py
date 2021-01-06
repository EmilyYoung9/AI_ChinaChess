import my_chess as mc
import constants
import history_heuristic as hh
import sqlite3

class relation:
    def __init__(self):
        self.chess_type = 0

        self.num_attack = 0
        self.num_guard = 0
        self.num_attacked = 0
        self.num_guarded = 0

        self.attack = [0, 0, 0, 0, 0, 0]
        self.attacked = [0, 0, 0, 0, 0, 0]
        self.guard = [0, 0, 0, 0, 0, 0]
        self.guarded = [0, 0, 0, 0, 0, 0]


class my_game:
    def __init__(self):
        self.board = mc.chess_board()
        self.max_depth = constants.max_depth
        self.history_table = hh.history_table()
        self.best_move = mc.step()
        self.cnt = 0

    # alpha-beta剪枝，alpha是大可能下界，beta是最小可能上界
    def alpha_beta(self, depth, alpha, beta):
        who = (self.max_depth - depth) % 2  # 那个玩家

        if self.is_game_over(who):  # 判断是否游戏结束，如果结束了就不用搜了
            return constants.min_val
        if depth == 1:  # 搜到指定深度了，也不用搜了
            return self.evaluate(who)
        move_list = self.board.generate_move(who)  # 返回所有能走的方法

        # 利用历史表0
        for i in range(len(move_list)):
            move_list[i].score = self.history_table.get_history_score(who, move_list[i])
        move_list.sort()  # 为了让更容易剪枝利用历史表得分进行排序

        best_step = move_list[0]
        score_list = []
        for step in move_list:
            temp = self.move_to(step)
            score = -self.alpha_beta(depth - 1, -beta, -alpha)  # 因为是一层选最大一层选最小，所以利用取负号来实现
            score_list.append(score)
            self.undo_move(step, temp)
            if score > alpha:
                alpha = score
                if depth == self.max_depth:
                    self.best_move = step
                best_step = step
            if alpha >= beta:
                best_step = step
                break

        # 更新历史表
        if best_step.from_x != -1:
            self.history_table.add_history_score(who, best_step, depth)
        return alpha

    def evaluate(self, who):  # who表示该谁走，返回评分值
        self.cnt += 1
        # print('====================================================================================')
        relation_list = self.init_relation_list()
        base_val = [0, 0]
        pos_val = [0, 0]
        mobile_val = [0, 0]
        relation_val = [0, 0]
        for x in range(9):
            for y in range(10):
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                if type == 0:
                    continue
                # now = 0 if who else 1
                now = now_chess.belong
                pos = x * 9 + y
                temp_move_list = self.board.get_chess_move(x, y, now, True)
                #计算基础价值
                base_val[now] += constants.base_val[type]
                # 计算位置价值
                if now == 0:  # 如果是要求最大值的玩家
                    pos_val[now] += constants.pos_val[type][pos]
                else:
                    pos_val[now] += constants.pos_val[type][89 - pos]
                # 计算机动性价值，记录关系信息
                for item in temp_move_list:
                    # print('----------------')
                    # print(item)
                    temp_chess = self.board.board[item.to_x][item.to_y]  # 目的位置的棋子

                    if temp_chess.chess_type == constants.kong:  # 如果是空，那么加上机动性值
                        # print('ok')
                        mobile_val[now] += constants.mobile_val[type]
                        # print(mobile_val[now])
                        continue
                    elif temp_chess.belong != now:  # 如果不是自己一方的棋子
                        # print('ok1')
                        if temp_chess.chess_type == constants.jiang:  # 如果能吃了对方的将，那么就赢了
                            if temp_chess.belong != who:
                                # print(self.board.board[item.from_x][item.from_y])
                                # print(temp_chess)
                                # print(item)
                                # print('bug here')
                                return constants.max_val
                            else:
                                relation_val[1 - now] -= 20  # 如果不能，那么就相当于被将军，对方要减分
                                continue
                        # 记录攻击了谁
                        relation_list[x][y].attack[relation_list[x][y].num_attack] = temp_chess.chess_type
                        relation_list[x][y].num_attack += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        # print(item)
                        # 记录被谁攻击
                        # if item.to_x == 4 and item.to_y == 1:
                        #     print('--------------')
                        #     print(now_chess.chess_type)
                        #     print(item.from_x, item.from_y)
                        #     print('*************')
                        #     print(temp_chess.chess_type)
                        #     print(item.to_x, item.to_y)
                        #     print(relation_list[item.to_x][item.to_y].num_attacked)
                        #     print([relation_list[item.to_x][item.to_y].attacked[j] for j in range(relation_list[item.to_x][item.to_y].num_attacked)])
                        #     if relation_list[item.to_x][item.to_y].num_attacked == 5:
                        #         print('###################')
                        #         self.board.print_board()
                        #         print('###################')

                        relation_list[item.to_x][item.to_y].attacked[
                            relation_list[item.to_x][item.to_y].num_attacked] = type
                        relation_list[item.to_x][item.to_y].num_attacked += 1
                    elif temp_chess.belong == now:
                        # print('ok2')
                        if temp_chess.chess_type == constants.jiang:  # 保护自己的将没有意义，直接跳过
                            continue
                        # 记录关系信息-guard
                        # print(item)
                        # if item.to_x == 4 and item.to_y == 1:
                        #     print('--------------')
                        #     print(now_chess.chess_type)
                        #     print(item)
                        #     print('*************')
                        #     print(temp_chess.chess_type)
                        #     print(relation_list[item.to_x][item.to_y].num_guarded)
                        #     print([relation_list[item.to_x][item.to_y].guarded[j] for j in range(relation_list[item.to_x][item.to_y].num_guarded)])
                        #     if relation_list[item.to_x][item.to_y].num_guarded == 5:
                        #         print('###################')
                        #         print(x, y, who)
                        #         self.board.print_board(True)
                        #         print('###################')
                        relation_list[x][y].guard[relation_list[x][y].num_guard] = temp_chess
                        relation_list[x][y].num_guard += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        relation_list[item.to_x][item.to_y].guarded[relation_list[item.to_x][item.to_y].num_guarded] = type
                        relation_list[item.to_x][item.to_y].num_guarded += 1
                    # relation_list[x][y].chess_type = type
        for x in range(9):
            for y in range(10):
                num_attacked = relation_list[x][y].num_attacked
                num_guarded = relation_list[x][y].num_guarded
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                now = now_chess.belong
                unit_val = constants.base_val[now_chess.chess_type] >> 3
                sum_attack = 0  # 被攻击总子力
                sum_guard = 0
                min_attack = 999  # 最小的攻击者
                max_attack = 0  # 最大的攻击者
                max_guard = 0
                flag = 999  # 有没有比这个子的子力小的
                if type == constants.kong:
                    continue
                # 统计攻击方的子力
                for i in range(num_attacked):
                    temp = constants.base_val[relation_list[x][y].attacked[i]]
                    flag = min(flag, min(temp, constants.base_val[type]))
                    min_attack = min(min_attack, temp)
                    max_attack = max(max_attack, temp)
                    sum_attack += temp
                # 统计防守方的子力
                for i in range(num_guarded):
                    temp = constants.base_val[relation_list[x][y].guarded[i]]
                    max_guard = max(max_guard, temp)
                    sum_guard += temp
                if num_attacked == 0:
                    relation_val[now] += 5 * relation_list[x][y].num_guarded
                else:
                    muti_val = 5 if who != now else 1
                    if num_guarded == 0:  # 如果没有保护
                        relation_val[now] -= muti_val * unit_val
                    else:  # 如果有保护
                        if flag != 999:  # 存在攻击者子力小于被攻击者子力,对方将愿意换子
                            relation_val[now] -= muti_val * unit_val
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # 如果是二换一, 并且最小子力小于被攻击者子力与保护者子力之和, 则对方可能以一子换两子
                        elif num_guarded == 1 and num_attacked > 1 and min_attack < constants.base_val[type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # 如果是三换二并且攻击者子力较小的二者之和小于被攻击者子力与保护者子力之和,则对方可能以两子换三子
                        elif num_guarded == 2 and num_attacked == 3 and sum_attack - max_attack < constants.base_val[type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * ((sum_attack - max_attack) >> 3)
                        # 如果是n换n，攻击方与保护方数量相同并且攻击者子力小于被攻击者子力与保护者子力之和再减去保护者中最大子力,则对方可能以n子换n子
                        elif num_guarded == num_attacked and sum_attack < constants.base_val[now_chess.chess_type] + sum_guard - max_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * ((sum_guard - max_guard) >> 3)
                            relation_val[1 - now] -= sum_attack >> 3
        # print('-------------------------')
        # print(base_val[0], pos_val[0], mobile_val[0], relation_val[0])
        # print(base_val[1], pos_val[1], mobile_val[1], relation_val[1])
        my_max_val = base_val[0] + pos_val[0] + mobile_val[0] + relation_val[0]
        my_min_val = base_val[1] + pos_val[1] + mobile_val[1] + relation_val[1]
        if who == 0:
            return my_max_val - my_min_val
        else:
            return my_min_val - my_max_val

    def init_relation_list(self):
        res_list = []
        for i in range(9):
            res_list.append([])
            for j in range(10):
                res_list[i].append(relation())
        return res_list

    def init_lib(self):
        conn = sqlite3.connect("./init_lib/chess.db")
        cursor = conn.cursor()
        # sql = """select name from sqlite_master where type='table' order by name"""
        sql = "select * from chess"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        print(type(result))
        conn.close()

    def is_game_over(self, who):  # 判断游戏是否结束
        for i in range(9):
            for j in range(10):
                if self.board.board[i][j].chess_type == constants.jiang:
                    if self.board.board[i][j].belong == who:
                        return False
        return True

    def move_to(self, step, flag = False):  # 移动棋子
        belong = self.board.board[step.to_x][step.to_y].belong
        chess_type = self.board.board[step.to_x][step.to_y].chess_type
        temp = mc.chess(belong, chess_type)
        # if flag:
        #     self.board.print_board()
        #     print(self.board.board[step.to_x][step.to_y].chess_type)
        self.board.board[step.to_x][step.to_y].chess_type = self.board.board[step.from_x][step.from_y].chess_type
        # if flag:
        #     print(self.board.board[step.from_x][step.from_y].chess_type)
        #     print(self.board.board[step.to_x][step.to_y].chess_type)
        #     print(step.to_x, step.to_y)
        self.board.board[step.to_x][step.to_y].belong = self.board.board[step.from_x][step.from_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = constants.kong
        self.board.board[step.from_x][step.from_y].belong = -1
        return temp

    def undo_move(self, step, chess):  # 恢复棋子
        self.board.board[step.from_x][step.from_y].belong = self.board.board[step.to_x][step.to_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = self.board.board[step.to_x][step.to_y].chess_type
        self.board.board[step.to_x][step.to_y].belong = chess.belong
        self.board.board[step.to_x][step.to_y].chess_type = chess.chess_type



if __name__ == "__main__":
    game = my_game()
    # game.board.print_board()
    while(True):
        from_x = int(input())
        from_y = int(input())
        to_x = int(input())
        to_y = int(input())
        s = mc.step(from_x, from_y, to_x, to_y)
        # game.board.print_board()

        game.alpha_beta(game.max_depth, constants.min_val, constants.max_val)
        print(game.best_move)
        game.move_to(game.best_move)


    game.move_to(s)
    # game.board.print_board()
