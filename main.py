import random
import pygame
from config import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Game Hub")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

player = pygame.Rect((WIDTH // 2 - 25, HEIGHT - 30, 30, 30))
player_movement = 5

gravity = 1
charge_rate = 0.5
yump_minpower = 1
yump_maxpower = 15
yump_power = 0

charging_yump = False
yumping = False
velo_y = 0
velo_x = 0
ground_y = HEIGHT - player.height

facing = 0
standing_on_platform = False
current_plat_top = 0
current_plat_left = 0
current_plat_right = 0




def main():
    global yumping, velo_y, velo_x, yump_power, charging_yump, facing,standing_on_platform,current_plat_top,current_plat_left, current_plat_right

    running = True

    platform_height = 20
    num_platforms = 5
    platform_width = 150

    # Estimate how high a max jump can go (rough guess)
    estimated_jump_height = (yump_maxpower ** 2) // (2 * gravity)
    platform_spacing = int(estimated_jump_height * 0.8)# keep spacing reasonable

    # Ensure platforms stay visible
    max_vertical_range = platform_spacing * (num_platforms - 1)
    start_y = HEIGHT - player.height - platform_height - 20

    # Adjust start_y if needed to avoid platforms going above screen
    if start_y - max_vertical_range < 0:
        start_y = max_vertical_range + 20

    platforms = [
        pygame.Rect(50, HEIGHT - 300, 30, 150),  # Tall vertical platform (left wall)
        pygame.Rect(80, HEIGHT - 100, 120, 20),  # Bottom-right horizontal
        pygame.Rect(140, HEIGHT - 180, 150, 20),  # Middle-right bounce target
        pygame.Rect(80, HEIGHT - 260, 120, 20),  # Higher platform
    ]

    # last_x = None
    # for i in range(num_platforms):
    #     while True:
    #         x = random.randint(0, WIDTH - platform_width)
    #         if last_x is None or abs(x - last_x) > platform_width // 2:
    #             break
    #     last_x = x
    #     y = start_y - (i * platform_spacing)
    #     platforms.append(pygame.Rect(x, y, platform_width, platform_height))


    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen,RED,player)

        for plat in platforms:
            pygame.draw.rect(screen, (0,100,0), plat)

        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and not yumping:
                velo_y = -yump_power
                velo_x = facing * yump_power * 0.7
                yumping = True
                charging_yump = False
                yump_power = 0

        if not yumping:

            if key[pygame.K_LEFT]:
                if not charging_yump:
                    player.x -= player_movement
                    facing = -1
                    if not (current_plat_left + 5 <= player.centerx <= current_plat_right + 5):
                        yumping = True


                else:
                    facing = -1

            elif key[pygame.K_RIGHT]:
                if not charging_yump:
                    player.x += player_movement
                    facing = 1
                    if  not (current_plat_left <= player.centerx <= current_plat_right) :
                        yumping = True


                else:
                    facing = 1
            else:
                facing = 0




        if key[pygame.K_SPACE] and not yumping:
            charging_yump = True
            yump_power += charge_rate
            yump_power  = min(yump_power, yump_maxpower)



        if yumping:
            velo_y += gravity
            player.x += velo_x
            player.y += velo_y

            if player.y > ground_y:
                player.y = ground_y
                yumping = False
                velo_y = 0
                velo_x = 0



            for plat in platforms:
                if player.colliderect(plat):


                    if velo_y > 0 and player.bottom - velo_y <= plat.top and player.bottom >= plat.top:

                        yumping = False
                        current_plat_top = plat.top
                        current_plat_left = plat.left
                        current_plat_right = plat.right
                        player.bottom = plat.top
                        velo_y = 0
                        velo_x = 0
                        break

                    elif velo_y < 0 and player.top <= plat.bottom and player.bottom > plat.bottom and plat.left < player.right and plat.right > player.left:
                        player.top = plat.bottom
                        velo_y = 0

                        break


                    elif velo_x > 0 and player.right > plat.left and player.left < plat.left:

                        player.right = plat.left
                        velo_y = -abs(velo_y)
                        velo_x = -abs(velo_x)

                        break


                    elif velo_x < 0 and player.left < plat.right and player.right > plat.right:

                        player.left = plat.right

                        velo_y = -abs(velo_y)
                        velo_x = abs(velo_x)

                        break


        player.x = max(0, min(WIDTH - player.width, player.x))
        player.y = max(0, min(HEIGHT - player.height, player.y))

        clock.tick(FPS)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
