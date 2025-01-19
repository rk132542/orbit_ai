import pygame
import numpy as np
import game

WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.init()

GRAVITY_ACC = 9.8


def set_player_gravity_accleration(player):
    center = np.array([WIDTH / 2, HEIGHT / 2])
    direction = center - player.position

    player.acceleration = direction / np.linalg.norm(direction) * GRAVITY_ACC
    # print("a: ", player.acceleration)
    # print("v: ", player.velocity)

def control_player_direction(player):
    mouse_pos = np.array(pygame.mouse.get_pos())
    direction = mouse_pos - player.position
    player.angle = np.arctan2(direction[1], direction[0]) + np.pi / 2

def draw_slider(window, player):
    padding = 10
    
    slider_container_height = 150
    slider_container_width = 30
    
    pygame.draw.rect(window, (255, 255, 255), (padding, HEIGHT - slider_container_height -
                     padding, slider_container_width, slider_container_height))
    slider_height = player.level * slider_container_height
    pygame.draw.rect(window, (0, 255, 0), (padding, HEIGHT -
                     slider_height - padding, slider_container_width, slider_height))

def main():
    time_warp = 1.0
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True

    game_instance = game.Game(WIDTH, HEIGHT)
    player = game.GameObject(500.0, 200.0, 10, 30)#, angle=3.14/4)

    player_velocity = np.array([0.0, 25.0])
    player_acceleration = np.array([9.8, 29.8])
    player.velocity = player_velocity
    player.acceleration = player_acceleration
    game_instance.add_object(player)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player.level = 0
                if event.key == pygame.K_z:
                    player.level = 1
                if event.key == pygame.K_RIGHT:
                    time_warp *= 2
                if event.key == pygame.K_LEFT:
                    time_warp /= 2
            if event.type == pygame.QUIT:
                running = False

        window.fill((0, 0, 0))
        clock.tick(FPS)
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LSHIFT]:
            player.level = min(1, player.level+0.01)
        if key_pressed[pygame.K_LCTRL]:
            player.level = max(0, player.level-0.01)
        
        draw_slider(window, player)
        
        planet = pygame.draw.circle(window, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), 80)
        control_player_direction(player)
        

        
        #if player within circle 
        if ((player.position[0] - WIDTH//2)**2 + (player.position[1] - HEIGHT//2)**2 < 80**2):
            print("Player inside planet")
            player.acceleration = np.array([0.0, 0.0])
            player.velocity = np.array([0.0, 0.0])
        else:
            set_player_gravity_accleration(player)

        
        
        thrust_level = player.level * 100
        thrust = np.array([0, -thrust_level])
        rotation = np.array([
            [np.cos(player.angle), -np.sin(player.angle)],
            [np.sin(player.angle), np.cos(player.angle)]
        ])
        thrust = np.dot(rotation, thrust)
        
        player.apply_force(thrust)

        game_instance.update(time_warp / FPS)
        game_instance.display_board(window)

        pygame.display.set_caption(
            f"FPS: {round(clock.get_fps())}, Time warp: {time_warp}")
    pygame.quit()


if __name__ == "__main__":
    main()
