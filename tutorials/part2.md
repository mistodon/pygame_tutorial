# Modes

## Life counter for a lose condition

``` python
    bg = pygame.image.load("assets/images/bg.png")
    bird = pygame.image.load("assets/images/bird.png")

    # Two new images to load:
    life_empty = pygame.image.load("assets/images/life_empty.png")
    life_full = pygame.image.load("assets/images/life_full.png")
```

``` python
    bird_y = 72
    bird_velocity = 0

    # Two new images to load:
    lives = 3
```

``` python
    bird_y = 0
    bird_velocity = 0

    # Two new images to load:
    lives = 3
```

Update this:

``` python
        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0
```

to this:

``` python
        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0
            lives -= 1
            bird_y = 72

        print(f"lives = {lives}")
```

Now drawing those lives:

``` python
        screen.blit(life_full, (0, 0))
        screen.blit(life_full, (32, 0))
        screen.blit(life_full, (64, 0))
```

``` python
        image = life_full if lives > 0 else life_empty
        screen.blit(image, (0, 0))

        image = life_full if lives > 1 else life_empty
        screen.blit(image, (32, 0))

        image = life_full if lives > 2 else life_empty
        screen.blit(image, (64, 0))
```

``` python
        for index in range(3):
            x_position = index * 32
            image = life_full if lives > index else life_empty
            screen.blit(image, (x_position, 0))
```

## Just for fun: scoring

``` python
    font = pygame.font.SysFont("arial", 24, True)
```

``` python
    bird_y = 0
    bird_velocity = 0
    lives = 3

    # This
    score = 0
```

``` python
        bird_y += bird_velocity * dt

        # Add score based on speed:
        score += int(abs(bird_velocity) * dt)

        print(f"score = {score}")
```

``` python
        score_label = font.render(str(score), True, (32, 32, 32))
        screen.blit(score_label, (160, 0))
```

Now finally, let’s reset the score and lives on a game over.

``` python
        if lives <= 0:
            lives = 3
            score = 0
```

But that’s really jarring! Let’s make some changes.

## Three Modes

> Note: We’re switching to part2b.py

Three modes:

1.  Waiting to start.

2.  Playing.

3.  Game over.

``` python
WAITING_MODE = 0
PLAYING_MODE = 1
GAMEOVER_MODE = 2
```

``` python
    current_mode = WAITING_MODE
```

``` python
    # Input state
    button_held = False
    button_pressed = False
```

``` python
        # Input phase
        keys = pygame.key.get_pressed()

        # We're renaming 'flying' to 'button_held'
        button_held = keys[pygame.K_SPACE]

        # And we need 'button_pressed' defaults to False
        button_pressed = False

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            button_pressed = True
```

``` python
        # Make sure you update this elsewhere!
        if button_held:
            bird_velocity = -flight_speed
```

Now we want to make our controls/gravity *only* work during play mode:

``` python
        # Update phase
        if current_mode == PLAYING_MODE:
            bird_velocity += gravity * dt

            if button_held:
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
```

But we started in waiting mode, so this won’t do anything! Let’s add another branch in our update, specifically for handling waiting mode:

``` python
        # Update phase
        if current_mode == WAITING_MODE:
            if button_pressed:
                current_mode = PLAYING_MODE

        elif current_mode == PLAYING_MODE:
            bird_velocity += gravity * dt

            if button_held:
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
```

Okay now let’s go to a game over when we run out of lives, instead of resetting straight away:

``` python
            if lives <= 0:
                current_mode = GAMEOVER_MODE
```

Let’s draw something when we get a game over too:

``` python
        if current_mode == GAMEOVER_MODE:
            gameover_label = font.render("GAME OVER", True, (250, 32, 32))
            screen.blit(gameover_label, (50, 60))
```

And then one last change to let us get out of game over mode:

``` python
        # Update phase
        if current_mode == WAITING_MODE:
            if button_pressed:
                current_mode = PLAYING_MODE

        elif current_mode == PLAYING_MODE:
            bird_velocity += gravity * dt

            if button_held:
                bird_velocity = -flight_speed

            bird_y += bird_velocity * dt
            score += int(abs(bird_velocity) * dt)

            if bird_y < ceiling_y or bird_y > floor_y:
                bird_velocity = 0
                lives -= 1
                bird_y = 72

            if lives <= 0:
                current_mode = GAMEOVER_MODE

        elif current_mode == GAMEOVER_MODE:
            if button_pressed:
                current_mode = WAITING_MODE
                lives = 3
                score = 0
```
