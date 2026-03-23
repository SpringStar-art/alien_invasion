import pygame
import sys
from time import sleep

class Settings:
    """存储游戏所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_speed = 1.0
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1          # 1右 -1左
        self.alien_points = 50

        # 飞船设置
        self.ship_limit = 1               # 为了方便测试，设为1（碰撞一次游戏结束）
        self.ship_speed = 1.0

        # 速度提升系数
        self.speedup_scale = 1.1

        # 调用初始化动态设置的方法
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """重置动态速度为初始值（用于重启游戏）"""
        self.ship_speed = 1.0
        self.bullet_speed = 1.0
        self.alien_speed = 0.5
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit
        self.game_active = True


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 左右移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
        # 上下移动
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中（底部中央）"""
        self.rect.midbottom = self.screen_rect.midbottom


class Bullet(pygame.sprite.Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 创建子弹矩形并设置位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储精确y坐标
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(pygame.sprite.Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 临时用红色矩形代替图像（如有外星人图片可替换）
        self.image = pygame.Surface((60, 60))
        self.image.fill((255, 0, 0))   # 红色
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        """向右或向左移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)

        self._create_fleet()

    def run_game(self):
        """游戏主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_r:
            self._restart_game()

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人用于计算尺寸
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算可容纳的行数
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 手动检测飞船与外星人的碰撞（使用矩形碰撞）
        for alien in self.aliens.sprites():
            if self.ship.rect.colliderect(alien.rect):
                self._ship_hit()
                return   # 碰撞后立即返回，避免多次触发

        # 检查是否有外星人到达屏幕底端
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                return   # 同样，一旦发生立即返回

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 还有生命，减少生命并重置场景
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)   # 短暂暂停，让玩家反应
        else:
            # 没有生命了，游戏结束
            self.stats.game_active = False

    def _update_bullets(self):
        """更新子弹的位置并处理碰撞"""
        self.bullets.update()

        # 删除超出屏幕的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查子弹与外星人的碰撞
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

        # 如果外星人全被消灭，提升速度并进入下一关
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1

    def _restart_game(self):
        """重启游戏（按R键时调用）"""
        # 重置统计信息
        self.stats.reset_stats()
        # 重置动态速度设置
        self.settings.initialize_dynamic_settings()
        # 清空现有外星人和子弹
        self.aliens.empty()
        self.bullets.empty()
        # 创建新的外星人群
        self._create_fleet()
        # 重置飞船位置
        self.ship.center_ship()
        # 确保游戏处于活动状态
        self.stats.game_active = True

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        font = pygame.font.SysFont(None, 48)
        score_str = str(self.stats.score)
        score_image = font.render(score_str, True, (0, 0, 0))
        self.screen.blit(score_image, (10, 10))

        # 显示等级
        level_str = f"Level: {self.stats.level}"
        level_image = font.render(level_str, True, (0, 0, 0))
        self.screen.blit(level_image, (10, 50))

        # 显示剩余飞船数
        ships_str = f"Ships: {self.stats.ships_left}"
        ships_image = font.render(ships_str, True, (0, 0, 0))
        self.screen.blit(ships_image, (10, 90))

        # 如果游戏结束，显示信息（必须在flip之前绘制）
        if not self.stats.game_active:
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_image = game_over_font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_image.get_rect()
            game_over_rect.center = (self.settings.screen_width // 2,
                                     self.settings.screen_height // 2)
            self.screen.blit(game_over_image, game_over_rect)

            restart_font = pygame.font.SysFont(None, 36)
            restart_image = restart_font.render("Press R to restart", True, (0, 0, 0))
            restart_rect = restart_image.get_rect()
            restart_rect.center = (self.settings.screen_width // 2,
                                   self.settings.screen_height // 2 + 60)
            self.screen.blit(restart_image, restart_rect)

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()