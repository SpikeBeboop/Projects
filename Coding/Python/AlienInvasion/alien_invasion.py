import sys

import pygame

from src.settings import Settings
from src.ship import Ship
from src.bullet import Bullet


class AlienInvasion:
    # 管理游戏资源和行为的类
    def __init__(self):
        # 初始化游戏并创建游戏资源
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    #检查按键按下事件
    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    #检查按键弹起事件
    def _check_keyup_events(self,event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #更新屏幕
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def run_game(self):
        # 开始游戏的主循环
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()