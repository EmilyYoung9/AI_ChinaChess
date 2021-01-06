'''
所有的常量都写在这个文件里
'''

import pygame


'''
关于UI的常量
'''
SCREEN_WIDTH = 800      #屏幕宽度
SCREEN_HEIGHT = 650     #屏幕高度
# 起始位置
Start_X = 50
Start_Y = 50
# 每一格的长度
Line_Span = 60

player1Color = 1
player2Color = 2
overColor = 3

BG_COLOR = pygame.Color(213, 176, 146)      #背景颜色
Line_COLOR = pygame.Color(255, 255, 200)    #线条颜色
TEXT_COLOR = pygame.Color(255, 0, 0)        #文字颜色

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

repeat = 0

# 棋子的图片
pieces_images = {
    #黑棋
    'b_jiang': pygame.image.load("imgs/black/b_j.gif"),      #黑将
    'b_che': pygame.image.load("imgs/black/b_c.gif"),      #黑车
    'b_ma': pygame.image.load("imgs/black/b_m.gif"),     #黑马
    'b_pao': pygame.image.load("imgs/black/b_p.gif"),    #黑炮
    'b_xiang': pygame.image.load("imgs/black/b_x.gif"),  #黑象
    'b_shi': pygame.image.load("imgs/black/b_s.gif"),  #黑士
    'b_bing': pygame.image.load("imgs/black/b_z.gif"),      #黑卒

    #红棋
    'r_jiang': pygame.image.load("imgs/red/r_j.gif"),        #红帅
    'r_che': pygame.image.load("imgs/red/r_c.gif"),        #红车
    'r_ma': pygame.image.load("imgs/red/r_m.gif"),       #红马
    'r_pao': pygame.image.load("imgs/red/r_p.gif"),      #红炮
    'r_xiang': pygame.image.load("imgs/red/r_x.gif"),    #红相
    'r_shi': pygame.image.load("imgs/red/r_s.gif"),    #红士
    'r_bing': pygame.image.load("imgs/red/r_z.gif"),        #红兵
}

'''
关于中国象棋设置的常量
'''
# 两个玩家
my_max = True
my_min = False

# 八个棋子
kong = 0
jiang = 1
che = 2
ma = 3
pao = 4
xiang = 5
shi = 6
bing = 7

# 初始化的棋盘
init_borad = [
    [  che, kong, kong, bing, kong, kong, bing, kong, kong,   che],
    [   ma, kong,  pao, kong, kong, kong, kong,  pao, kong,    ma],
    [xiang, kong, kong, bing, kong, kong, bing, kong, kong, xiang],
    [  shi, kong, kong, kong, kong, kong, kong, kong, kong,   shi],
    [jiang, kong, kong, bing, kong, kong, bing, kong, kong, jiang],
    [  shi, kong, kong, kong, kong, kong, kong, kong, kong,   shi],
    [xiang, kong, kong, bing, kong, kong, bing, kong, kong, xiang],
    [   ma, kong,  pao, kong, kong, kong, kong,  pao, kong,    ma],
    [  che, kong, kong, bing, kong, kong, bing, kong, kong,   che]
]

# 最大步数
max_depth = 4

# 最大值，最小值
max_val = 1000000
min_val = -1000000

# 评估方法
base_val   = [0, 0, 500, 300, 300, 250, 250, 80]
mobile_val = [0, 0,   6,  12,   6,   1,   1, 15]
pos_val = [
    [  # 空
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # 将
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        5, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
        0,  0,  0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # 车
        -6,  5, -2,  4,  8,  8,  6,  6,  6,  6,
         6,  8,  8,  9, 12, 11, 13,  8, 12,  8,
         4,  6,  4,  4, 12, 11, 13,  7,  9,  7,
        12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
         0,  0, 12, 14, 15, 15, 16, 16, 33, 14,
        12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
         4,  6,  4,  4, 12, 11, 13,  7,  9,  7,
         6,  8,  8,  9, 12, 11, 13,  8, 12,  8,
        -6,  5, -2,  4,  8,  8,  6,  6,  6,  6
    ],
    [  # 马
         0,  -3, 5,  4,  2,  2,  5,  4,  2, 2,
        -3,   2, 4,  6, 10, 12, 20, 10,  8, 2,
         2,   4, 6, 10, 13, 11, 12, 11, 15, 2,
         0,   5, 7,  7, 14, 15, 19, 15,  9, 8,
         2, -10, 4, 10, 15, 16, 12, 11,  6, 2,
         0,   5, 7,  7, 14, 15, 19, 15,  9, 8,
         2,   4, 6, 10, 13, 11, 12, 11, 15, 2,
        -3,   2, 4,  6, 10, 12, 20, 10,  8, 2,
         0,  -3, 5,  4,  2,  2,  5,  4,  2, 2
    ],
    [  # 炮
        0, 0, 1, 0, -1, 0, 0,  1,  2,  4,
        0, 1, 0, 0,  0, 0, 3,  1,  2,  4,
        1, 2, 4, 0,  3, 0, 3,  0,  0,  0,
        3, 2, 3, 0,  0, 0, 2, -5, -4, -5,
        3, 2, 5, 0,  4, 4, 4, -4, -7, -6,
        3, 2, 3, 0,  0, 0, 2, -5, -4, -5,
        1, 2, 4, 0,  3, 0, 3,  0,  0,  0,
        0, 1, 0, 0,  0, 0, 3,  1,  2,  4,
        0, 0, 1, 0, -1, 0, 0,  1,  2,  4
    ],
    [  # 相
        0, 0, -2, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  3, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,  0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, -2, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # 士
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # 兵
        0, 0, 0, -2, 3, 10, 20, 20, 20, 0,
        0, 0, 0,  0, 0, 18, 27, 30, 30, 0,
        0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
        0, 0, 0,  0, 0, 35, 40, 55, 65, 2,
        0, 0, 0,  6, 7, 40, 42, 55, 70, 4,
        0, 0, 0,  0, 0, 35, 40, 55, 65, 2,
        0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
        0, 0, 0,  0, 0, 18, 27, 30, 30, 0,
        0, 0, 0, -2, 3, 10, 20, 20, 20, 0
    ]
]