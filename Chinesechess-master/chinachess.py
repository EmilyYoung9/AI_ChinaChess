import pygame
import time
import constants
from button import Button
import pieces
import computer
import my_game as mg

class ChinaChess():
    window = None
    Start_X = constants.Start_X
    Start_Y = constants.Start_Y
    Line_Span = constants.Line_Span
    Max_X = Start_X + 8 * Line_Span
    Max_Y = Start_Y + 9 * Line_Span
    from_x = 0
    from_y = 0
    to_x = 0
    to_y = 0
    clickx = -1
    clicky = -1

    mgInit = mg.my_game()
    player1Color = constants.player1Color
    player2Color = constants.player2Color
    Putdownflag = player1Color
    piecesSelected = None

    button_go = None
    piecesList = []

    def start_game(self):
        #主界面
        ChinaChess.window = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
        pygame.display.set_caption("test")
        ChinaChess.button_go = Button(ChinaChess.window, "重新开始", constants.SCREEN_WIDTH - 100, 300)  # 创建开始按钮
        self.piecesInit()

        while True:
            time.sleep(0.1)
            # 获取事件
            ChinaChess.window.fill(constants.BG_COLOR)
            self.drawChessboard()
            #MainGame.button_go.draw_button()
            self.piecesDisplay()
            self.VictoryOrDefeat()
            self.Computerplay()
            self.getEvent()
            pygame.display.update()
            pygame.display.flip()

    def drawChessboard(self):
        mid_end_y = ChinaChess.Start_Y + 4 * ChinaChess.Line_Span
        min_start_y = ChinaChess.Start_Y + 5 * ChinaChess.Line_Span
        for i in range(0, 9):
            x = ChinaChess.Start_X + i * ChinaChess.Line_Span
            if i == 0 or i == 8:
                y = ChinaChess.Start_Y + i * ChinaChess.Line_Span
                pygame.draw.line(ChinaChess.window, constants.BLACK, [x, ChinaChess.Start_Y], [x, ChinaChess.Max_Y], 1)
            else:
                pygame.draw.line(ChinaChess.window, constants.BLACK, [x, ChinaChess.Start_Y], [x, mid_end_y], 1)
                pygame.draw.line(ChinaChess.window, constants.BLACK, [x, min_start_y], [x, ChinaChess.Max_Y], 1)

        for i in range(0, 10):
            x = ChinaChess.Start_X + i * ChinaChess.Line_Span
            y = ChinaChess.Start_Y + i * ChinaChess.Line_Span
            pygame.draw.line(ChinaChess.window, constants.BLACK, [ChinaChess.Start_X, y], [ChinaChess.Max_X, y], 1)

        speed_dial_start_x =  ChinaChess.Start_X + 3 * ChinaChess.Line_Span
        speed_dial_end_x =  ChinaChess.Start_X + 5 * ChinaChess.Line_Span
        speed_dial_y1 = ChinaChess.Start_Y + 0 * ChinaChess.Line_Span
        speed_dial_y2 = ChinaChess.Start_Y + 2 * ChinaChess.Line_Span
        speed_dial_y3 = ChinaChess.Start_Y + 7 * ChinaChess.Line_Span
        speed_dial_y4 = ChinaChess.Start_Y + 9 * ChinaChess.Line_Span

        pygame.draw.line(ChinaChess.window, constants.BLACK, [speed_dial_start_x, speed_dial_y1], [speed_dial_end_x, speed_dial_y2], 1)
        pygame.draw.line(ChinaChess.window, constants.BLACK, [speed_dial_start_x, speed_dial_y2],
                         [speed_dial_end_x, speed_dial_y1], 1)
        pygame.draw.line(ChinaChess.window, constants.BLACK, [speed_dial_start_x, speed_dial_y3],
                         [speed_dial_end_x, speed_dial_y4], 1)
        pygame.draw.line(ChinaChess.window, constants.BLACK, [speed_dial_start_x, speed_dial_y4],
                         [speed_dial_end_x, speed_dial_y3], 1)

    def piecesInit(self):
        ChinaChess.piecesList.append(pieces.Rooks(ChinaChess.player2Color, 0,0))
        ChinaChess.piecesList.append(pieces.Rooks(ChinaChess.player2Color,  8, 0))
        ChinaChess.piecesList.append(pieces.Elephants(ChinaChess.player2Color,  2, 0))
        ChinaChess.piecesList.append(pieces.Elephants(ChinaChess.player2Color,  6, 0))
        ChinaChess.piecesList.append(pieces.King(ChinaChess.player2Color, 4, 0))
        ChinaChess.piecesList.append(pieces.Knighs(ChinaChess.player2Color,  1, 0))
        ChinaChess.piecesList.append(pieces.Knighs(ChinaChess.player2Color,  7, 0))
        ChinaChess.piecesList.append(pieces.Cannons(ChinaChess.player2Color,  1, 2))
        ChinaChess.piecesList.append(pieces.Cannons(ChinaChess.player2Color, 7, 2))
        ChinaChess.piecesList.append(pieces.Mandarins(ChinaChess.player2Color,  3, 0))
        ChinaChess.piecesList.append(pieces.Mandarins(ChinaChess.player2Color, 5, 0))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player2Color, 0, 3))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player2Color, 2, 3))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player2Color, 4, 3))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player2Color, 6, 3))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player2Color, 8, 3))

        ChinaChess.piecesList.append(pieces.Rooks(ChinaChess.player1Color,  0, 9))
        ChinaChess.piecesList.append(pieces.Rooks(ChinaChess.player1Color,  8, 9))
        ChinaChess.piecesList.append(pieces.Elephants(ChinaChess.player1Color, 2, 9))
        ChinaChess.piecesList.append(pieces.Elephants(ChinaChess.player1Color, 6, 9))
        ChinaChess.piecesList.append(pieces.King(ChinaChess.player1Color,  4, 9))
        ChinaChess.piecesList.append(pieces.Knighs(ChinaChess.player1Color, 1, 9))
        ChinaChess.piecesList.append(pieces.Knighs(ChinaChess.player1Color, 7, 9))
        ChinaChess.piecesList.append(pieces.Cannons(ChinaChess.player1Color,  1, 7))
        ChinaChess.piecesList.append(pieces.Cannons(ChinaChess.player1Color,  7, 7))
        ChinaChess.piecesList.append(pieces.Mandarins(ChinaChess.player1Color,  3, 9))
        ChinaChess.piecesList.append(pieces.Mandarins(ChinaChess.player1Color,  5, 9))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player1Color, 0, 6))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player1Color, 2, 6))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player1Color, 4, 6))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player1Color, 6, 6))
        ChinaChess.piecesList.append(pieces.Pawns(ChinaChess.player1Color, 8, 6))

    def piecesDisplay(self):
        for item in ChinaChess.piecesList:
            item.displaypieces(ChinaChess.window)


    def getEvent(self):
        # 获取所有的事件
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                if (
                        mouse_x > ChinaChess.Start_X - ChinaChess.Line_Span / 2 and mouse_x < ChinaChess.Max_X + ChinaChess.Line_Span / 2) and (
                        mouse_y > ChinaChess.Start_Y - ChinaChess.Line_Span / 2 and mouse_y < ChinaChess.Max_Y + ChinaChess.Line_Span / 2):
                    # print( str(mouse_x) + "" + str(mouse_y))
                    # print(str(MainGame.Putdownflag))
                    if ChinaChess.Putdownflag != ChinaChess.player1Color:
                        return

                    click_x = round((mouse_x - ChinaChess.Start_X) / ChinaChess.Line_Span)
                    click_y = round((mouse_y - ChinaChess.Start_Y) / ChinaChess.Line_Span)
                    click_mod_x = (mouse_x - ChinaChess.Start_X) % ChinaChess.Line_Span
                    click_mod_y = (mouse_y - ChinaChess.Start_Y) % ChinaChess.Line_Span
                    if abs(click_mod_x - ChinaChess.Line_Span / 2) >= 5 and abs(
                            click_mod_y - ChinaChess.Line_Span / 2) >= 5:
                        # print("有效点：x="+str(click_x)+" y="+str(click_y))
                        # 有效点击点
                        self.from_x = ChinaChess.clickx
                        self.from_y = ChinaChess.clicky
                        self.to_x = click_x
                        self.to_y = click_y
                        print(self.from_x)
                        print(self.from_y)
                        ChinaChess.clickx=click_x
                        ChinaChess.clicky=click_y
                        self.PutdownPieces(ChinaChess.player1Color, click_x, click_y)

                else:
                    print("out")
                if ChinaChess.button_go.is_click():
                    #self.restart()
                    print("button_go click")
                else:
                    print("button_go click out")

    def PutdownPieces(self, t, x, y):
        selectfilter = list(filter(lambda cm: cm.x == x and cm.y == y and cm.player == ChinaChess.player1Color,ChinaChess.piecesList))
        if len(selectfilter):
            ChinaChess.piecesSelected = selectfilter[0]
            return

        if ChinaChess.piecesSelected :
            arr = pieces.listPiecestoArr(ChinaChess.piecesList)
            if ChinaChess.piecesSelected.canmove(arr, x, y):
                self.PiecesMove(ChinaChess.piecesSelected, x, y)
                ChinaChess.Putdownflag = ChinaChess.player2Color
        else:
            fi = filter(lambda p: p.x == x and p.y == y, ChinaChess.piecesList)
            listfi = list(fi)
            if len(listfi) != 0:
                ChinaChess.piecesSelected = listfi[0]

    def PiecesMove(self,pieces,  x , y):
        for item in ChinaChess.piecesList:
            if item.x == x and item.y == y:
                ChinaChess.piecesList.remove(item)
        pieces.x = x
        pieces.y = y
        print("move to " + str(x) + " " + str(y))
        return True

    def Computerplay(self):
        if ChinaChess.Putdownflag == ChinaChess.player2Color:
            print("轮到电脑了")

            computermove = computer.getPlayInfo(ChinaChess.piecesList, self.from_x, self.from_y, self.to_x, self.to_y, self.mgInit)
            if computer==None:
                return
            piecemove = None
            for item in ChinaChess.piecesList:
                if item.x == computermove[0] and item.y == computermove[1]:
                    piecemove= item

            self.PiecesMove(piecemove, computermove[2], computermove[3])
            ChinaChess.Putdownflag = ChinaChess.player1Color

    #判断游戏胜利
    def VictoryOrDefeat(self):
        txt = ""
        result = [ChinaChess.player1Color, ChinaChess.player2Color]
        for item in ChinaChess.piecesList:
            if type(item) == pieces.King:
                if item.player == ChinaChess.player1Color:
                    result.remove(ChinaChess.player1Color)
                if item.player == ChinaChess.player2Color:
                    result.remove(ChinaChess.player2Color)

        if len(result) == 0:
            return
        if result[0] == ChinaChess.player1Color :
            txt = "失败！"
        else:
            txt = "胜利！"
        ChinaChess.window.blit(self.getTextSuface("%s" % txt), (constants.SCREEN_WIDTH - 100, 200))
        ChinaChess.Putdownflag = constants.overColor

    def getTextSuface(self, text):
        pygame.font.init()
        # print(pygame.font.get_fonts())
        font = pygame.font.SysFont('kaiti', 18)
        txt = font.render(text, True, constants.TEXT_COLOR)
        return txt

    def endGame(self):
        print("exit")
        exit()



if __name__ == '__main__':
    ChinaChess().start_game()
