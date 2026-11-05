#------------Arak University------------#
#------------Computer Engineering------------#


import pygame
import random

# تنظیمات اصلی
Grid_size = 15
Cell_size = 40 #اندازه هر خانه شبکه 40 پیکسل
Window_size = Grid_size * Cell_size
Target_count = 30 #تعداد نقاط حساس
Camera_range = 1 #شعاع دید هر دوربین
Max_camera = 5
Max_obstacles = 5 #حداکثر تعداد مانع
Max_obstacles_length = 3 #حداکثر طول مانع

# رنگ‌ها
White = (255, 255, 255)
Gray = (200, 200, 200)
Red = (255, 0, 0)
Blue = (0, 0, 255)
DarkGreen = (173, 255, 47)
Black = (0, 0, 0)
ButtonColor = (100, 100, 255)
ButtonHover = (150, 150, 255)
ObstaclesColor = (120, 120, 120)
SelectedColor = (255, 215, 0)

# مقداردهی pygame
pygame.init()
screen = pygame.display.set_mode((Window_size, Window_size + 140))
pygame.display.set_caption("Camera Coverage with Obstacles")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# متغیرهای مورد نیاز برای نگهداری وضعیت برنامه
Target_points = set()
Camera_positions = []
Covered_points = set()
Obstacle_lines = []
Obstacle_cells = set()
Clicks = []

# تولید کردن نقاط هدف به صورت تصادفی
def generate_targets():
    global Target_points, Camera_positions, Covered_points, Obstacle_lines, Obstacle_cells, Clicks
    Target_points = set()
    while len(Target_points) < Target_count:
        x = random.randint(0, Grid_size - 1)
        y = random.randint(0, Grid_size - 1)
        Target_points.add((x, y))

    #سایر وضعیت‌ها پاکسازی میشوند
    Camera_positions = []
    Covered_points = set()
    Obstacle_lines = []
    Obstacle_cells = set()
    Clicks = []

#وقتی برنامه اجرا میشود یک بار این تابع صدا میشود تا نقاط تصادفی تولید بشوند
generate_targets()

#موقعیت یک خانه که دوربین در آن است را میگیرد و ناحیه تحت پوشش دوربین را برمیگرداند
def get_coverage(x, y):
    coverage = set()
    for dx in range(-Camera_range, Camera_range + 1):
        for dy in range(-Camera_range, Camera_range + 1):
            nx = x + dx
            ny = y + dy
            if 0 <= nx < Grid_size and 0 <= ny < Grid_size:
                if (nx, ny) not in Obstacle_cells:
                    coverage.add((nx, ny))
    return coverage


# الگوریتم حریصانه
def greedy_camera_placement():
    global Covered_points, Camera_positions
    uncovered_targets = Target_points.copy()
    while uncovered_targets and len(Camera_positions) < Max_camera:
        best_pos = None
        best_coverage = set()
        for x in range(Grid_size):
            for y in range(Grid_size):
                if (x, y) in Obstacle_cells:
                    continue
                coverage = get_coverage(x, y)
                covered_targets = coverage & uncovered_targets
                if len(covered_targets) > len(best_coverage):
                    best_coverage = covered_targets
                    best_pos = (x, y)
        if best_pos:
            Camera_positions.append(best_pos)
            Covered_points.update(get_coverage(*best_pos))
            uncovered_targets -= best_coverage
        else:
            break

# الگوریتم *A
def astar_camera_placement():
    global Covered_points, Camera_positions
    uncovered_targets = Target_points.copy()
    while uncovered_targets and len(Camera_positions) < Max_camera:
        best_pos = None
        best_score = float('inf')
        for x in range(Grid_size):
            for y in range(Grid_size):
                if (x, y) in Obstacle_cells:
                    continue
                coverage = get_coverage(x, y)
                covered_targets = coverage & uncovered_targets
                if not covered_targets:
                    continue
                g = len(Camera_positions) + 1
                h = len(uncovered_targets - covered_targets)
                f = g + h
                if f < best_score:
                    best_score = f
                    best_pos = (x, y)
        if best_pos:
            Camera_positions.append(best_pos)
            Covered_points.update(get_coverage(*best_pos))
            uncovered_targets -= get_coverage(*best_pos)
        else:
            break

# رسم مانع
def handle_obstacle_click(pos):
    global Clicks, Obstacle_cells, Obstacle_lines
    x, y = pos[0] // Cell_size, pos[1] // Cell_size
    if not (0 <= x < Grid_size and 0 <= y < Grid_size):
        return
    if len(Clicks) == 0:
        Clicks.append((x, y))
    elif len(Clicks) == 1:
        x1, y1 = Clicks[0]
        if x == x1 or y == y1:
            length = abs(x - x1 + y - y1) + 1
            if length <= Max_obstacles_length and len(Obstacle_lines) < Max_obstacles:
                points = []
                if x == x1:
                    for dy in range(min(y, y1), max(y, y1) + 1):
                        points.append((x, dy))
                else:
                    for dx in range(min(x, x1), max(x, x1) + 1):
                        points.append((dx, y))
                Obstacle_lines.append(points)
                Obstacle_cells.update(points)
        Clicks.clear()

# رسم تصویری شبکه روی صفحه گرافیکی
def draw_grid():
    for x in range(Grid_size):
        for y in range(Grid_size):
            rect = pygame.Rect(x * Cell_size, y * Cell_size, Cell_size, Cell_size)
            pygame.draw.rect(screen, DarkGreen if (x, y) in Covered_points else White, rect)
            if (x, y) in Obstacle_cells:
                pygame.draw.rect(screen, ObstaclesColor, rect)
            if (x, y) in Target_points:
                pygame.draw.circle(screen, Red, (x * Cell_size + Cell_size // 2, y * Cell_size + Cell_size // 2), Cell_size // 4)
            if (x, y) in Camera_positions:
                pygame.draw.circle(screen, Blue, (x * Cell_size + Cell_size // 2, y * Cell_size + Cell_size // 2), Cell_size // 6)
            pygame.draw.rect(screen, Gray, rect, 1)
    for point in Clicks:
        rect = pygame.Rect(point[0] * Cell_size, point[1] * Cell_size, Cell_size, Cell_size)
        pygame.draw.rect(screen, SelectedColor, rect, 3)

# رسم دکمه‌های پایین صفحه
def draw_button(x, y, w, h, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, ButtonHover if rect.collidepoint(mouse) else ButtonColor, rect)
    pygame.draw.rect(screen, Black, rect, 2)
    label = font.render(text, True, Black)
    screen.blit(label, (x + 6, y + 6))
    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.delay(150)
        if action:
            action()

# نشان دادن آمار کلی برنامه
def draw_stats():
    lines = [
        f"Cameras: {len(Camera_positions)} / {Max_camera}",
        f"Covered: {len(Covered_points & Target_points)} / {len(Target_points)}",
        f"Obstacles: {len(Obstacle_lines)} / {Max_obstacles}"
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, Black), (10, Window_size + 10 + i * 20))

# حلقه اصلی برنامه
running = True
while running:
    screen.fill(Gray)
    draw_grid()
    draw_stats()
    draw_button(Window_size - 130, Window_size + 10, 110, 30, "Greedy", greedy_camera_placement)
    draw_button(Window_size - 130, Window_size + 50, 110, 30, "A*", astar_camera_placement)
    draw_button(Window_size - 130, Window_size + 90, 110, 30, "Reset", generate_targets)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] < Window_size:
            handle_obstacle_click(event.pos)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
