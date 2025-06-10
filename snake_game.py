import pygame
import sys
import random
import math
from pygame.math import Vector2

# 初始化pygame
pygame.init()

# 游戏常量
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 60

# 颜色定义
BACKGROUND = (15, 25, 35)
GRID_COLOR = (30, 45, 60)
SNAKE_HEAD = (50, 180, 100)
SNAKE_BODY = (40, 150, 80)
FOOD_COLOR = (220, 80, 60)
OBSTACLE_COLOR = (120, 90, 200)
TEXT_COLOR = (230, 230, 230)
UI_BG = (10, 20, 30, 180)
UI_BORDER = (60, 140, 200)

# 特殊食物颜色
SPECIAL_FOODS = [
    (255, 200, 60),  # 金色 - 高分数
    (180, 80, 220),  # 紫色 - 特殊效果
    (60, 200, 255)  # 蓝色 - 特殊效果
]


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [Vector2(5, 8), Vector2(4, 8), Vector2(3, 8)]
        self.direction = Vector2(1, 0)
        self.new_direction = Vector2(1, 0)
        self.grow = False
        # self.speed = 8  # 初始速度（每秒移动的格子数）
        self.speed = 4  # 初始速度（每秒移动的格子数）
        self.move_timer = 0
        self.move_delay = 1 / self.speed

    def update(self, dt):
        # 更新移动计时器
        self.move_timer += dt

        # 检查是否应该移动
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.direction = self.new_direction

            # 移动蛇身
            if self.grow:
                new_body = self.body[:]
                new_body.insert(0, self.body[0] + self.direction)
                self.body = new_body
                self.grow = False
            else:
                new_body = self.body[:-1]
                new_body.insert(0, self.body[0] + self.direction)
                self.body = new_body

    ## def change_direction(self, new_direction):
    ##     # 防止180度转向（反向移动），但这段代码逻辑会导致任何垂直方向变化都被阻止（比如上下左右之间的切换），而不仅仅是反向移动：
    ##     if (self.direction.x * new_direction.x + self.direction.y * new_direction.y) == 0:
    ##         return
    ##     self.new_direction = new_direction
    ## 示例：
    ## 如果蛇正在向右 (Vector2(1, 0))，此时按下 W（即向上），该逻辑不会允许改变方向
    ## · 原方向：(1, 0)
    ## · 新方向：(0, -1)
    ## · dot product = 1*0 + 0*(-1) = 0 → 条件成立 → 被拒绝！
    def change_direction(self, new_direction):
        # 只有当新方向与当前方向完全相反时才不允许转向
        if (self.direction.x + new_direction.x == 0 and
                self.direction.y + new_direction.y == 0):
            return
        self.new_direction = new_direction

    def draw(self, screen):
        # 绘制蛇身
        for i, pos in enumerate(self.body):
            # 蛇头
            if i == 0:
                color = SNAKE_HEAD
                rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect, 0, 8)

                # 蛇眼睛
                eye_size = CELL_SIZE // 6
                eye_offset = CELL_SIZE // 4
                if self.direction.x == 1:  # 向右
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + CELL_SIZE - eye_offset),
                                        int(pos.y * CELL_SIZE + eye_offset)), eye_size)
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + CELL_SIZE - eye_offset),
                                        int(pos.y * CELL_SIZE + CELL_SIZE - eye_offset)), eye_size)
                elif self.direction.x == -1:  # 向左
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + eye_offset),
                                        int(pos.y * CELL_SIZE + eye_offset)), eye_size)
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + eye_offset),
                                        int(pos.y * CELL_SIZE + CELL_SIZE - eye_offset)), eye_size)
                elif self.direction.y == 1:  # 向下
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + eye_offset),
                                        int(pos.y * CELL_SIZE + CELL_SIZE - eye_offset)), eye_size)
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + CELL_SIZE - eye_offset),
                                        int(pos.y * CELL_SIZE + CELL_SIZE - eye_offset)), eye_size)
                elif self.direction.y == -1:  # 向上
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + eye_offset),
                                        int(pos.y * CELL_SIZE + eye_offset)), eye_size)
                    pygame.draw.circle(screen, (240, 240, 240),
                                       (int(pos.x * CELL_SIZE + CELL_SIZE - eye_offset),
                                        int(pos.y * CELL_SIZE + eye_offset)), eye_size)
            # 蛇身
            else:
                color = SNAKE_BODY
                # 根据位置渐变颜色
                color_factor = max(0.6, 1.0 - i * 0.03)
                segment_color = (
                    int(color[0] * color_factor),
                    int(color[1] * color_factor),
                    int(color[2] * color_factor)
                )
                rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, segment_color, rect, 0, 5)

                # 蛇身连接处的装饰
                if i < len(self.body) - 1:
                    next_pos = self.body[i + 1]
                    if next_pos.x == pos.x:  # 垂直方向
                        pygame.draw.rect(screen, (30, 110, 60),
                                         (pos.x * CELL_SIZE + CELL_SIZE // 3,
                                          min(pos.y, next_pos.y) * CELL_SIZE + CELL_SIZE - 2,
                                          CELL_SIZE // 3, CELL_SIZE + 4))
                    else:  # 水平方向
                        pygame.draw.rect(screen, (30, 110, 60),
                                         (min(pos.x, next_pos.x) * CELL_SIZE + CELL_SIZE - 2,
                                          pos.y * CELL_SIZE + CELL_SIZE // 3,
                                          CELL_SIZE + 4, CELL_SIZE // 3))


class Food:
    def __init__(self, snake_body, obstacles):
        self.position = self.generate_position(snake_body, obstacles)
        self.type = random.randint(0, 10)  # 0-7普通食物，8-9特殊食物1，10特殊食物2
        self.pulse = 0
        self.rotation = 0

    def generate_position(self, snake_body, obstacles):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = Vector2(x, y)

            # 检查是否与蛇身或障碍物重叠
            if position not in snake_body and position not in obstacles:
                return position

    def draw(self, screen):
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        pulse_size = math.sin(self.pulse) * 0.1 + 1.0

        center_x = self.position.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.position.y * CELL_SIZE + CELL_SIZE // 2

        # 确定食物颜色和类型
        if self.type < 8:  # 普通食物
            color = FOOD_COLOR
            radius = CELL_SIZE // 3
        elif self.type < 10:  # 特殊食物1
            color = SPECIAL_FOODS[0]
            radius = CELL_SIZE // 2
        else:  # 特殊食物2
            color = SPECIAL_FOODS[1]
            radius = CELL_SIZE // 2.5

        # 绘制食物
        pygame.draw.circle(screen, color, (center_x, center_y), radius * pulse_size)

        # 特殊食物的装饰
        if self.type >= 8:
            self.rotation = (self.rotation + 2) % 360
            angle_rad = math.radians(self.rotation)

            # 绘制旋转的三角形
            for i in range(3):
                angle = angle_rad + i * (2 * math.pi / 3)
                start_x = center_x + math.cos(angle) * radius * 0.7
                start_y = center_y + math.sin(angle) * radius * 0.7
                end_x = center_x + math.cos(angle) * radius * 1.4
                end_y = center_y + math.sin(angle) * radius * 1.4
                pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), 2)


class Obstacle:
    def __init__(self, position):
        self.position = position
        self.pulse = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        self.pulse = (self.pulse + 0.03) % (2 * math.pi)
        pulse_value = (math.sin(self.pulse) + 1) / 2  # 0到1之间

        # 创建渐变色
        color = (
            int(OBSTACLE_COLOR[0] * (0.7 + 0.3 * pulse_value)),
            int(OBSTACLE_COLOR[1] * (0.7 + 0.3 * pulse_value)),
            int(OBSTACLE_COLOR[2] * (0.7 + 0.3 * pulse_value))
        )

        rect = pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect, 0, 7)

        # 绘制内部装饰
        inner_rect = pygame.Rect(
            self.position.x * CELL_SIZE + 4,
            self.position.y * CELL_SIZE + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8
        )
        pygame.draw.rect(screen, (180, 160, 220), inner_rect, 0, 5)


class Particle:
    def __init__(self, position, color):
        self.position = Vector2(position)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * random.uniform(50, 150)
        self.color = color
        self.size = random.uniform(2, 5)
        self.lifetime = random.uniform(0.5, 1.0)
        self.timer = 0

    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity.y += 100 * dt  # 重力
        self.timer += dt

    def is_alive(self):
        return self.timer < self.lifetime

    def draw(self, screen):
        alpha = 255 * (1 - self.timer / self.lifetime)
        color = (
            self.color[0],
            self.color[1],
            self.color[2],
            int(alpha)
        )
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), int(self.size))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
      
        # 使用系统默认字体。注意不同操作系统或环境如果没有合适的中文字体，默认字体可能无法渲染中文字符，导致乱码或方块
        # self.font = pygame.font.SysFont(None, 36)
        # self.small_font = pygame.font.SysFont(None, 24)

        # 下载一个中文字体文件（如 SimHei.ttf、NotoSansSC-Regular.otf 等），放在项目目录下。（字体文件需与 snake_game.py 在同一目录，或者填写完整路径。）
        # 修改字体加载方式为使用本地字体文件
        # self.font = pygame.font.Font("SimHei.ttf", 36)  # 替换为你实际的字体文件名
        # self.small_font = pygame.font.Font("SimHei.ttf", 24)

        # 自动查找系统中可用的中文字体（如微软雅黑、黑体等）
        chinese_fonts = [f for f in pygame.font.get_fonts() if 'hei' in f.lower() or 'kai' in f.lower()]
        font_name = chinese_fonts[0] if chinese_fonts else None
        self.font = pygame.font.SysFont(font_name, 36)
        self.small_font = pygame.font.SysFont(font_name, 24)

        self.reset()

    def reset(self):
        self.snake = Snake()
        self.obstacles = self.generate_obstacles()
        self.food = Food(self.snake.body, self.obstacles)
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        self.particles = []

    def generate_obstacles(self):
        obstacles = []
        # 生成一些随机障碍物
        for _ in range(8):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                position = Vector2(x, y)

                # 确保障碍物不会出现在蛇的起始位置
                if position not in self.snake.body:
                    obstacles.append(Obstacle(position))
                    break
        return obstacles

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def create_particles(self, position, count, color):
        for _ in range(count):
            self.particles.append(Particle(position, color))

    def update(self, dt):
        if self.game_over or self.paused:
            return

        # 更新蛇
        self.snake.update(dt)

        # 更新粒子
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)

        # 检查是否吃到食物
        if self.snake.body[0] == self.food.position:
            # 增加分数
            if self.food.type < 8:
                self.score += 1
                self.create_particles((
                    self.food.position.x * CELL_SIZE + CELL_SIZE // 2,
                    self.food.position.y * CELL_SIZE + CELL_SIZE // 2
                ), 15, FOOD_COLOR)
            elif self.food.type < 10:
                self.score += 3
                self.create_particles((
                    self.food.position.x * CELL_SIZE + CELL_SIZE // 2,
                    self.food.position.y * CELL_SIZE + CELL_SIZE // 2
                ), 25, SPECIAL_FOODS[0])
            else:
                self.score += 5
                self.create_particles((
                    self.food.position.x * CELL_SIZE + CELL_SIZE // 2,
                    self.food.position.y * CELL_SIZE + CELL_SIZE // 2
                ), 30, SPECIAL_FOODS[1])

            # 蛇变长
            self.snake.grow = True

            # 生成新食物
            self.food = Food(self.snake.body, self.obstacles)

            # 每得5分增加速度
            if self.score % 5 == 0 and self.snake.speed < 15:
                self.snake.speed += 0.5
                self.snake.move_delay = 1 / self.snake.speed

        # 检查碰撞
        head = self.snake.body[0]

        # 检查是否撞墙
        if (head.x < 0 or head.x >= GRID_WIDTH or
                head.y < 0 or head.y >= GRID_HEIGHT):
            self.game_over = True
            self.create_particles((
                head.x * CELL_SIZE + CELL_SIZE // 2,
                head.y * CELL_SIZE + CELL_SIZE // 2
            ), 30, SNAKE_HEAD)

        # 检查是否撞到自己
        if head in self.snake.body[1:]:
            self.game_over = True
            self.create_particles((
                head.x * CELL_SIZE + CELL_SIZE // 2,
                head.y * CELL_SIZE + CELL_SIZE // 2
            ), 30, SNAKE_HEAD)

        # 检查是否撞到障碍物
        for obstacle in self.obstacles:
            if head == obstacle.position:
                self.game_over = True
                self.create_particles((
                    head.x * CELL_SIZE + CELL_SIZE // 2,
                    head.y * CELL_SIZE + CELL_SIZE // 2
                ), 30, OBSTACLE_COLOR)

        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def draw(self):
        # 绘制背景
        self.screen.fill(BACKGROUND)

        # 绘制网格
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

        # 绘制障碍物
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # 绘制食物
        self.food.draw(self.screen)

        # 绘制蛇
        self.snake.draw(self.screen)

        # 绘制粒子
        for particle in self.particles:
            particle.draw(self.screen)

        # 绘制UI背景
        pygame.draw.rect(self.screen, UI_BG, (0, 0, SCREEN_WIDTH, 40))
        pygame.draw.line(self.screen, UI_BORDER, (0, 40), (SCREEN_WIDTH, 40), 2)

        # 绘制分数
        score_text = self.font.render(f"分数: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 5))

        # 绘制最高分
        high_score_text = self.small_font.render(f"最高分: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 12))

        # 绘制游戏状态
        if self.game_over:
            # 半透明覆盖层
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            # 游戏结束文本
            game_over_text = self.font.render("游戏结束!", True, (220, 80, 80))
            restart_text = self.small_font.render("按 R 键重新开始", True, TEXT_COLOR)
            exit_text = self.small_font.render("按 Esc 键退出游戏", True, TEXT_COLOR)

            self.screen.blit(game_over_text,
                             (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(restart_text,
                             (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(exit_text,
                             (SCREEN_WIDTH // 2 - exit_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 40))

        elif self.paused:
            # 半透明覆盖层
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            # 暂停文本
            pause_text = self.font.render("游戏暂停", True, (100, 180, 255))
            continue_text = self.small_font.render("按空格键继续", True, TEXT_COLOR)

            self.screen.blit(pause_text,
                             (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(continue_text,
                             (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 20))

        # 绘制控制提示
        if not self.game_over:
            controls_text = self.small_font.render("方向键移动 | 空格暂停 | R重新开始 | ESC退出", True, (180, 180, 180))
            self.screen.blit(controls_text,
                             (SCREEN_WIDTH // 2 - controls_text.get_width() // 2,
                              SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def run(self):
        last_time = pygame.time.get_ticks() / 1000.0

        while True:
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time

            pygame.key.stop_text_input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_r:
                        self.reset()

                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.paused = not self.paused

                    # 方向键（上下左右） 和WASD 键盘控制的输入逻辑
                    if not self.paused and not self.game_over:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.snake.change_direction(Vector2(0, -1))
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.snake.change_direction(Vector2(0, 1))
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            self.snake.change_direction(Vector2(-1, 0))
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.snake.change_direction(Vector2(1, 0))

            self.update(dt)
            self.draw()
            self.clock.tick(FPS)


# 运行游戏
if __name__ == "__main__":
    game = Game()
    game.run()
