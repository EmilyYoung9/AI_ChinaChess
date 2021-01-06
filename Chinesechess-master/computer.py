import constants
from pieces import listPiecestoArr
import my_chess as mc

def getPlayInfo(listpieces, from_x, from_y, to_x, to_y, mgInit):
    pieces = movedeep(listpieces ,1 ,constants.player2Color, from_x, from_y, to_x, to_y, mgInit)
    return [pieces[0].x, pieces[0].y, pieces[1], pieces[2]]

def movedeep(listpieces, deepstep, player, x1, y1, x2, y2, mgInit):

    # temp.board.print_board()
    # 专职
    s = mc.step(8 - x1, y1, 8 - x2, y2)
    print('ren')
    print(s)
    mgInit.move_to(s)
    # temp.evaluate(True)
    mgInit.alpha_beta(constants.max_depth, constants.min_val, constants.max_val)
    t = mgInit.best_move
    mgInit.move_to(t)
    print(mgInit.cnt)
    print("diao nao")
    print(t)
    # return t
    arr = listPiecestoArr(listpieces)
    listMoveEnabel = []
    for i in range(0, 9):
        for j in range(0, 10):

            for item in listpieces:

                if item.x == 8 - t.from_x and item.y == t.from_y:

                    listMoveEnabel.append([item, 8 - t.to_x, t.to_y])


    #
    # print(listMoveEnabel)
    piecesbest = listMoveEnabel[0]
    # print(piecesbest)
    # print("test")
    # print(piecesbest[0])
    # print("test")
    return piecesbest





