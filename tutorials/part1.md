# Structuring a Game

> <div class="note">
>
> If you’re reading this file in Visual Studio Code, you can right-click it and select 'Open Preview' to get a more readable view.
>
> </div>

Okay, we’re going to make a game in Python. And it’s not important what *kind* of game it is just yet, or what components will be *in* the game. For now, we just want to get the overall structure right.

Before we actually write any code, let’s talk about some of the reasons we’re going to structure it the way we are.

**Reason \#1: Games are really complicated and have so many moving parts!**

It’s just unavoidable! Games are literally build on interactions between various kinds of *things*. And fun games give you a lot of agency, which means there are a lot of different ways stuff can change. It’s almost impossible to wrap your head around every possibility - every variable, every combination of inputs, every combination of game elements smashing into each other.

The only ways to make this *manageable* are:

1.  Minimise the number of things that can change - health, position, velocity, etc. Collectively, we refer to these things as **state**.

2.  Minimise *where* we make changes to the state - so that it’s easier to keep track of for us.

3.  Minimise the number of branching paths in our code - so it’s easier for us to read through and visualise what’s happening under the hood.

**Reason \#2: Humans are fallible! Really, really fallible! Never trust anyone, especially yourself, to write code!**

Again, this is unavoidable. The only way to write good code is to make peace with the fact that you’re mostly going to write *bad* code. Not just when you’re learning either - you are *always* going to write bad code. But don’t despair, because there are very good ways to manage that too!

1.  Keep your code easy to change - so that when you realise you’ve misstepped, you can adjust.

2.  Keep your related code together - so that if there’s a problem with one part of it, you know exactly where to look.

3.  Try really hard to only change one thing at a time, and test the code after each change - so that if you accidentally break something, you know *exactly* what change to the code has caused it.

## The structure:

Bearing all of that in mind (although you don’t have to memorise it) here is how I would roughly structure a game:

1.  Setup

    -   Initialising resources (the game window, loading images etc.)

    -   Defining and initialising the **state**.

2.  Loop (or 'mainloop'), which has three phases:

    -   Input phase: Check for inputs by the player, and update the **input state**.

    -   Update phase: Use the **input state** to update the **game state** accordingly.

    -   Draw phase: Use the **game state** to decide what to draw on-screen.

> Note that I split the state into two parts - input state and game state. This is to allow the Update phase to respond to inputs without having to directly interact with mouse/keyboard/etc. Hopefully this will make more sense later.

Separating the three phases of the mainloop is **super important** for guarding against all the scary issues I talked about before.

-   Knowing that **only** the Input phase deals with input lets you more easily debug problems with the inputs not working - without having to think about the game state or the rendering.

-   Knowing that **only** the Update phase modifies the game state lets you more easily debug problems with game elements moving/changing/etc. - without having to think about inputs or rendering.

-   Knowing that the Draw phase **does not** modify the state at all lets you focus purely on the visuals of things - without having to worry about whether your state or inputs are wrong.

This gives you the following process for adding a new feature to the game, or debugging a problem:

1.  Are the inputs reacting properly? e.g. Does the **input state** seem correct?

2.  Is the game logic updating properly? e.g. Does the **game state** seem correct?

3.  Is the game rendering properly? e.g. Are you seeing the **game state** reflected on-screen the way you would expect?

This can help you significantly narrow down where you need to make changes.

Okay! Sorry for all of those words! Now we’re going to write code.

## The code:

This is going to be a very basic little 'game' where we can make a bird fly up and down. We’ll start with a mostly empty template, then we’ll add one section at a time.

``` python
import pygame

# All the code for our game goes inside this function:
def main():
    # 'pass' is Python for "don't do anything"
    # A function (def) cannot be empty, so we need that if we have
    # nothing else.
    pass

# This is a super weird Python thing. It's not worth stressing
# about, but this is how Python knows to run your 'main()' function
# when you run this file.
if __name__ == "__main__":
    main()
```

This code should run and successfully do nothing without crashing. Incredible! Now let’s do the Setup part:

``` python
def main():
    pygame.init()

    screen = pygame.display.set_mode((256, 144))

    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/images/bg.png")
    bird = pygame.image.load("assets/images/bird.png")
```

We’re also going to define some constants that our game will use. (Where a constant is just a variable that shouldn’t change while the game’s running.)

``` python
    # Constants
    gravity = 200
    flight_speed = 100
```

Next, we’re going to initialise the **input state**. In our game, there’s only one thing we can do: either fly, or not-fly. So we can do that with one variable:

``` python
    # Input state
    flying = False
```

And then to finish our Setup, we need to initialise the **game state** too. This, for us, is just the state of the bird itself:

``` python
    # Game state
    bird_y = 0
    bird_velocity = 0
```

Now if you run the game, it should *still* do nothing (although a window might flicker open for a second). But we’re ready to make our loop.

(We also have to get ahead of ourselves a tiny bit and include the input to quit, otherwise closing the window will be a pain.)

``` python
    # Loop
    while True:
        dt = clock.tick(60) / 1000

        # Input phase
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        # And we call this at the end to finish rendering our
        # current frame and display it in the window.
        pygame.display.flip()
```

Now when you run the game, you should have a tiny empty window. All you can do for now is close it.

So now we have three phases to implement within the loop: Input, Update, Draw. There’s nothing stopping you from coding each of them together so that you have something visual straight away - but for now, I’m going to cover them one at a time so we get a sense for how we might debug any problems.

Starting with the Input phase - all we want to be able to do is make our bird fly. If we’re holding space, it should be flying. If we’re *not* holding space, it should *not* be flying. So we’re going to check the space key, and update our **input state**:

``` python
        # Input phase
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        keys = pygame.key.get_pressed()

        flying = keys[pygame.K_SPACE]

        # Let's test the input state before we move on.
        # This line of code should show you whether the value is
        # correct. Press and release the space key to test it.
        print(f"flying = {flying}")
```

When you run the game, you should see a constant repeating line of `flying = False` in the terminal. But if you hold the space key while the game window is in focus, you should see it change to `flying = True` until you let go.

Now that we have confidence in our input, we can move to the Update phase. Here, we want our bird to fall with gravity. But, if we’re currently flying, we want to go up instead:

``` python
        # Update phase

        bird_velocity += gravity * dt

        if flying:
            bird_velocity = -flight_speed

        bird_y += bird_velocity * dt

        # Now we can validate our game state by seeing how these
        # variables change.
        # They should go up constantly, unless you hold space, then
        # the bird_y should decrease,
        # and the bird_velocity should stay fixed at -100.
        print(f"bird_velocity = {bird_velocity}")
        print(f"bird_y = {bird_y}")
```

And now that we have our game state, and hopefully it seems correct based on the `print` statements we added, we can move on to the Draw phase.

``` python
        # Draw phase

        screen.blit(bg, (0, 0))

        screen.blit(bird, (112, bird_y))
```

Finally, hopefully, we have a bird in our window! It should fall (possibly off the bottom of the screen) and you should be able to hold space to bring it back up again!

This may not be the most *exciting* output, but hopefully it illustrates how each phase is separate, and how they feed very *carefully* into each other. We don’t call `screen.blit` in the Update phase, and we don’t check `pygame.key.get_pressed` in the Draw phase - and this kind of separation makes it easier to ensure we know what’s going on at each point in the program.

## Optional extra credit - Keeping the bird on-screen:

This isn’t vital to the rest of things, but it was bothering me and it might be bothering you too. Plus it’s a good opportunity to *edit* our code, and debug it with `print` if anything seems like it doesn’t work.

Firstly, let’s add some new constants to set the floor and ceiling heights (`0` is the top, and `120` is just a little above the bottom, to account for the height of the bird itself):

``` python
    # Constants
    gravity = 200
    flight_speed = 100
    ceiling_y = 0
    floor_y = 120
```

And then in the Update phase, to keep our bird on-screen:

1.  If `bird_y` is less than `ceiling_y`, it’s too high and we cap it at `ceiling_y`.

2.  If `bird_y` is more than `floor_y`, it’s too low, and we cap it at `floor_y`.

3.  If we had to cap it at all, we want to reset `bird_velocity` to `0` - since it should lose all its speed if it bonks.

The most straightforward way to do that is probably:

``` python
        # We're back in the Update phase
        ...

        bird_y += bird_velocity * dt

        if bird_y < ceiling_y:
            bird_y = ceiling_y
            bird_velocity = 0

        if bird_y > floor_y:
            bird_y = floor_y
            bird_velocity = 0
```

Which totally works! But a slightly more elegant way to do the same thing might be:

``` python
        # We're back in the Update phase
        ...

        bird_y += bird_velocity * dt

        # Combine both checks to stop the velocity
        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0

        # And then I'll explain this in a... hmm... hold on...
        bird_y = min( max(floor_y, bird_y), ceiling_y)
```

That last line looks complicated, but how it works is this: the `min` function gives you the lowest of the two things you pass in. The `max` function gives the *highest* of the two things you pass in. Combining them (by passing the output of `max` as one of the inputs to `min`) will clamp a value *between* two end points.

But wait…​ why isn’t this working? The `max` function should prevent it from going below the floor, and the `min` function should prevent it from going above the ceiling.

Let me just…​ split that complicated line up and check in between…​

``` python
        # Combine both checks to stop the velocity
        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0

        # Split floor and ceiling caps, checking the value in between
        print("start")
        print(f"bird_y = {bird_y}")
        bird_y = max(floor_y, bird_y)
        print(f"bird_y = {bird_y}")
        bird_y = min(bird_y, ceiling_y)
        print(f"bird_y = {bird_y}")
        print("end")
```

``` text
start
bird_y = 16.398199999999946
bird_y = 120
bird_y = 0
end
```

Riiight okay, so I mixed up the floor and ceiling here! Because zero is at the top, the floor is the *higher* number, not the lower!

So when I say `max(floor_y, bird_y)` it *always* gives me back `floor_y`. And vice versa for the `min`. And because the `min` comes second, it *always* results in `ceiling_y`.

This isn’t a contrived example either, I legitimately made this mistake and included debugging it.

Here’s the fixed version:

``` python
        # We're back in the Update phase
        ...

        bird_y += bird_velocity * dt

        if bird_y < ceiling_y or bird_y > floor_y:
            bird_velocity = 0

        bird_y = min( max(ceiling_y, bird_y), floor_y)
```

So wait, my "elegant" version ended up with me writing a bug. *And* the code seems harder to understand…​ Was this a bad move? Maybe! It’s a very personal choice.

We’ve experienced the downsides of it first-hand, but there *are* upsides in my opinion. Specifically:

1.  We *always* clamp the `bird_y` without checking the floor or ceiling. (It’s not inside the `if` statement.) This is *really good* because code that *always* runs is less likely to surprise you in weird edge-cases. We are definitively saying "please set `bird_y` to this value", and if we get the value right, no other condition is going to screw it up.

2.  We aren’t duplicating the `bird_velocity = 0` code anymore. Before, we included it in two separate `if` statements. That’s not *inherently* bad? But repeating code in multiple places makes it harder to change later. You have to remember to change it in *every* place. Not only that, but I could have easily forgotten to put it in one of those two branches, and confuse myself later when the velocity only *sometimes* resets.

Don’t worry too much about this part though. I’m explaining my own thought process, but I cannot stress enough: either approach works and neither is wrong. Pick the one that’s easiest for you unless you find a good reason to change.
