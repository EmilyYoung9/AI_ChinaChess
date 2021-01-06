import pygame

class Button():
    def __init__(self, screen, msg, left, top):  # msg为要在按钮中显示的文本
        #初始化按钮的属性
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 150, 50
        self.button_color = (72, 61, 139)  # 设置按钮的rect对象颜色为深蓝
        self.text_color = (255, 255, 255)  # 设置文本的颜色为白色
        pygame.font.init()
        self.font = pygame.font.SysFont('kaiti', 20)  # 设置文本为默认字体，字号为40

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.center = self.screen_rect.center  # 创建按钮的rect对象，并使其居中
        self.left = left
        self.top = top

        self.deal_msg(msg)  # 渲染图像

    def deal_msg(self, msg):
        """将msg渲染为图像，并将其在按钮上居中"""
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)  # render将存储在msg的文本转换为图像
        self.msg_img_rect = self.msg_img.get_rect()  # 根据文本图像创建一个rect
        self.msg_img_rect.center = self.rect.center  # 将该rect的center属性设置为按钮的center属性

    def draw_button(self):
        #self.screen.fill(self.button_color, self.rect)  # 填充颜色
        self.screen.blit(self.msg_img, (self.left,self.top))  # 将该图像绘制到屏幕

    def is_click(self):
        point_x, point_y = pygame.mouse.get_pos()
        x = self.left
        y = self.top
        w, h = self.msg_img.get_size()

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y