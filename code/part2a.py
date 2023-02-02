import pygame


def main():
    pygame.init()

    screen = pygame.display.set_mode((256, 144))

    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/images/bg.png")
    bird = pygame.image.load("assets/images/bird.png")
    life_empty = pygame.image.load("assets/images/life_empty.png")
    life_full = pygame.image.load("assets/images/life_full.png")

    font = pygame.font.SysFont("arial", 24, True)

    # Constants
    gravity = 200
    flight_speed = 100
    ceiling_y = 0
    floor_y = 120

    # Input state
    flying = False

    # Game state
    bird_y = 72
    bird_velocity = 0
    lives = 3
    lives = 3
    score = 0

    # Loop
    while True:
        dt = clock.tick(60) / 1000


        # Input phase

        keys = pygame.key.get_pressed()

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        flying = keys[pygame.K_SPACE]


        # Update phase

        bird_velocity += gravity * dt

        if flying:
            bird_velocity = -flight_speed

        bird_y += bird_velocity * dt
        score += int(abs(bird_velocity) * dt)

        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0
            lives -= 1
            bird_y = 72

        if lives <= 0:
            lives = 3
            score = 0


        # Draw phase

        screen.blit(bg, (0, 0))

        screen.blit(bird, (112, bird_y))

        for index in range(3):
            x_position = index * 32
            image = life_full if lives > index else life_empty
            screen.blit(image, (x_position, 0))

        score_label = font.render(str(score), True, (32, 32, 32))
        screen.blit(score_label, (160, 0))


        pygame.display.flip()


if __name__ == "__main__":
    main()