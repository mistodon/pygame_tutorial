import pygame

def main():
    # Pygame wants u to always do this.
    pygame.init()

    # Opens a window
    screen = pygame.display.set_mode((256, 144))

    # Keeps our game running at a consistent FPS
    clock = pygame.time.Clock()

    # Load some images
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
        # We ask the game to aim for 60fps and it tells us
        # how many milliseconds have passed since last frame.
        # We convert it to seconds (divide by 1000) because
        # they're easier to work with.
        dt = clock.tick(60) / 1000


        # Input phase
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        # Gives us a mapping of whether each key is being pressed.
        keys = pygame.key.get_pressed()

        # `flying = True` only if space is pressed
        flying = keys[pygame.K_SPACE]


        # Update phase

        # Apply gravity to the bird's velocity (scaled by time)
        bird_velocity += gravity * dt

        # If we're flying, set the velocity to go up instead
        if flying:
            bird_velocity = -flight_speed

        # Apply the velocity to the bird's position (scaled by time)
        bird_y += bird_velocity * dt

        # Stop the velocity if the bird is off-screen
        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0

        # Clamp the bird's position to be on-screen
        bird_y = min( max(ceiling_y, bird_y), floor_y)


        # Draw phase

        # Draw the background with it's top-left corner at the
        # top-left of the window.
        screen.blit(bg, (0, 0))

        # Draw the bird at 112px from the left, and its Y-position
        # based on the game state.
        screen.blit(bird, (112, bird_y))


        pygame.display.flip()


if __name__ == "__main__":
    main()