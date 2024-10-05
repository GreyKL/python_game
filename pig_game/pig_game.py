import pygame
import random
import time

# 初始化pygame
pygame.init()

# 设置游戏屏幕的宽和高
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("抓猪猪咯")

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)

# 加载小猪和葱的图像
pig_image = pygame.image.load('pig.png')
scallion_image = pygame.image.load('scallion.png')
images = {'pig': pig_image, 'scallion': scallion_image}

# 加载支持中文的字体
font_path = 'SourceHanSansSC-VF.otf'
font = pygame.font.Font(font_path, 36)

# 记录得分和游戏时间
score = 0
start_time = time.time()
game_duration = 60  # 游戏持续时间为60秒
# font = pygame.font.Font(None, 36)

# 元素列表，用于存储屏幕上的元素
elements = []

# 游戏状态
game_active = True
game_over_reason = ""

# 每1秒生成一个新元素
spawn_interval = 1
last_spawn_time = time.time()

# 游戏循环
running = True
while running:
    screen.fill(white)
    current_time = time.time()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                for element in elements[:]:
                    if element['rect'].collidepoint(event.pos):
                        if element['type'] == 'pig':
                            score += 1
                            elements.remove(element)
                        elif element['type'] == 'scallion':
                            game_active = False
                            game_over_reason = "你咋点着聪了？!"
            else:
                # 点击重玩按钮时重新开始游戏
                if restart_rect.collidepoint(event.pos):
                    game_active = True
                    score = 0
                    start_time = time.time()
                    elements.clear()
                    game_over_reason = ""

    if game_active:
        # 检查时间是否结束
        if current_time - start_time >= game_duration:
            game_active = False
            game_over_reason = "时间到了哥!"

        # 每隔1秒生成一个新元素
        if current_time - last_spawn_time >= spawn_interval:
            item_type = random.choice(['pig', 'scallion'])
            item_rect = images[item_type].get_rect()
            item_rect.x = random.randint(0, screen_width - item_rect.width)
            item_rect.y = random.randint(0, screen_height - item_rect.height)
            item_speed_x = random.choice([-6, -5, -4, 4, 5, 6])  # 增加移动速度
            item_speed_y = random.choice([-6, -5, -4, 4, 5, 6])  # 增加移动速度
            spawn_time = current_time
            elements.append({'type': item_type, 'rect': item_rect, 'speed_x': item_speed_x, 'speed_y': item_speed_y, 'spawn_time': spawn_time})
            last_spawn_time = current_time

        # 更新并绘制元素
        for element in elements[:]:
            # 移动元素
            element['rect'].x += element['speed_x']
            element['rect'].y += element['speed_y']

            # 检查元素是否碰到边界并反弹
            if element['rect'].left <= 0 or element['rect'].right >= screen_width:
                element['speed_x'] = -element['speed_x']
            if element['rect'].top <= 0 or element['rect'].bottom >= screen_height:
                element['speed_y'] = -element['speed_y']

            # 绘制元素
            screen.blit(images[element['type']], element['rect'])

            # 检查元素是否存在超过5秒
            if current_time - element['spawn_time'] >= 5:
                elements.remove(element)

        # 显示得分和剩余时间
        score_text = font.render(f"您的得分: {score}", True, black)
        time_left = max(0, int(game_duration - (current_time - start_time)))
        time_text = font.render(f"剩余时间: {time_left}s", True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

    else:
        # 根据得分显示不同的消息
        if score < 10:
            end_message = "不是吧就这？"
        elif 10 <= score <= 20:
            end_message = "我的评价是非常一般"
        elif 21 <= score <= 30:
            end_message = "你还是很可以的"
        else:
            end_message = "您就是抓猪滴神！"

        # 显示游戏结束信息和得分
        game_over_text = font.render(game_over_reason, True, black)
        final_score_text = font.render(f"最后得分=: {score} -       {end_message}", True, black)
        restart_text = font.render("我要重抓", True, (255, 0, 0))

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 70))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 - 30))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(restart_text, restart_rect.topleft)

    # 更新显示
    pygame.display.flip()

    # 设置帧率
    pygame.time.Clock().tick(60)

# 退出游戏
pygame.quit()