import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((256, 144))

    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/images/bg.png")
    bird = pygame.image.load("assets/images/bird.png")

    # Constants
    gravity = 200
    flight_speed = 100
    ceiling_y = 0
    floor_y = 120

    # Input state
    flying = False

    # Game state
    bird_y = 0
    bird_velocity = 0

    # Loop
    while True:
        dt = clock.tick(60) / 1000


        # Input phase
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        keys = pygame.key.get_pressed()

        flying = keys[pygame.K_SPACE]


        # Update phase

        bird_velocity += gravity * dt

        if flying:
            bird_velocity = -flight_speed

        bird_y += bird_velocity * dt

        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0

        bird_y = min( max(ceiling_y, bird_y), floor_y)


        # Draw phase

        screen.blit(bg, (0, 0))

        screen.blit(bird, (112, bird_y))


        pygame.display.flip()


if __name__ == "__main__":
    main()