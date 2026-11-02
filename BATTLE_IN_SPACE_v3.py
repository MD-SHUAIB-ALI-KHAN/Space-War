# Space War - "Termination"
# FIRST GAME CODED BY SHUAIB
#
# v3 (Python 3 + pygame 2): bug-fixed v2 + player names, lives, game-over screen
# and a MySQL leaderboard (XAMPP). If MySQL isn't running, the game still plays.

import os
import random  # Imp for video games
import time
import tkinter
import turtle

import pygame

try:
    import db  # leaderboard code lives in db.py (needs: pip install mysql-connector-python)
except ImportError:
    db = None  # no connector installed -> play without a leaderboard

# Always run from the game's own folder so the images/sounds are found,
# no matter where the game is launched from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- settings
HIT_RANGE = 20      # how close (in pixels) two objects must be to count as a hit
BORDER = 290        # sprites bounce / missiles vanish beyond this
FRAME_DELAY = 0.05  # seconds per frame (same speed as the original)
PARTICLE_LIFE = 25  # frames an explosion particle lives
START_LIVES = 3     # you lose one life each time an enemy crashes into you

# ---------------------------------------------------------------- sound
pygame.mixer.init()

# ---------------------------------------------------------------- screen
turtle.fd(0)  # moves the turtle in the forward direction by a certain distance
turtle.speed(0)  # Speed of the animation and "not the movement speed" is set to max
turtle.bgcolor("black")  # Colour of the background
turtle.bgpic("realspace.gif")  # BG image
turtle.title("Termination")
turtle.ht()  # Hide turtle
turtle.setundobuffer(1)  # Saves memory
turtle.tracer(0)  # Speeds up the animation


class Sprite(turtle.Turtle):
    """Sprites are the game objects; Turtle gives them all their drawing/moving abilities."""

    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(shape=spriteshape)
        self.speed(0)  # animation speed ('0' is the fastest), NOT movement speed
        self.penup()  # so the turtle doesn't draw while moving
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.velocity = 1  # movement speed (was `self.speed`, which hid turtle's speed())

    def move(self):
        self.fd(self.velocity)

        # Boundary Detection
        if self.xcor() > BORDER:
            self.setx(BORDER)
            self.rt(60)
        if self.xcor() < -BORDER:
            self.setx(-BORDER)
            self.rt(60)
        if self.ycor() > BORDER:
            self.sety(BORDER)
            self.rt(60)
        if self.ycor() < -BORDER:
            self.sety(-BORDER)
            self.rt(60)

    def is_collision(self, other):
        # X is compared with X and Y with Y (the old code compared Y with other.xcor()).
        return (abs(self.xcor() - other.xcor()) <= HIT_RANGE and
                abs(self.ycor() - other.ycor()) <= HIT_RANGE)


class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.4, stretch_len=1.1, outline=None)
        self.velocity = 0

    def turn_left(self):
        self.lt(45)  # lt = left 45 degrees

    def turn_right(self):
        self.rt(45)  # rt = right 45 degrees

    def accelerate(self):
        self.velocity += 1

    def decelerate(self):
        self.velocity -= 1


class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.velocity = 3
        self.setheading(random.randint(0, 360))


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.velocity = 10
        self.shapesize(stretch_wid=0.4, stretch_len=0.4, outline=None)
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.velocity)

        # Boundary Detection (allies turn the other way)
        if self.xcor() > BORDER:
            self.setx(BORDER)
            self.lt(60)
        if self.xcor() < -BORDER:
            self.setx(-BORDER)
            self.lt(60)
        if self.ycor() > BORDER:
            self.sety(BORDER)
            self.lt(60)
        if self.ycor() < -BORDER:
            self.sety(-BORDER)
            self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty, shooter, laser_sound=None):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.velocity = 20
        self.shooter = shooter
        self.laser_sound = laser_sound
        self.park()

    def park(self):
        """Hide the missile off-screen and make it ready to fire again."""
        self.goto(-1000, 1000)
        self.status = "Ready"

    def fire(self):
        if self.status == "Ready":
            # Play the sound
            if self.laser_sound:
                self.laser_sound.play()
            else:
                pygame.mixer.music.load("laser shot.mp3")
                pygame.mixer.music.play()
            self.goto(self.shooter.xcor(), self.shooter.ycor())
            self.setheading(self.shooter.heading())
            self.status = "Firing"

    def move(self):
        if self.status == "Firing":
            self.fd(self.velocity)
            # Border check
            if abs(self.xcor()) > BORDER or abs(self.ycor()) > BORDER:
                self.park()


class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, 1000)
        self.life = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.life = PARTICLE_LIFE

    def hide(self):
        self.life = 0
        self.goto(-1000, 1000)

    def move(self):
        # Particles only move while alive, then hide again.
        if self.life > 0:
            self.fd(10)
            self.life -= 1
            if self.life == 0:
                self.hide()


class Game:
    def __init__(self):
        self.level = 1
        self.lives = START_LIVES
        self.score = 0
        self.state = "playing"      # "playing" or "gameover"
        self.player_name = "Player"
        self.want = None            # set by the keyboard on the game-over screen
        self.pen = turtle.Turtle()  # draws the border
        self.pen.ht()
        self.score_pen = turtle.Turtle()  # draws the status line (name / score / lives)
        self.score_pen.ht()
        self.score_pen.penup()
        self.score_pen.color("Blue")
        self.overlay_pen = turtle.Turtle()  # draws the game-over panel
        self.overlay_pen.ht()
        self.overlay_pen.speed(0)
        self.overlay_pen.penup()

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("Blue")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def show_status(self):
        self.score_pen.clear()
        self.score_pen.goto(-300, 310)
        msg = "%s   Score %s   Lives %s" % (self.player_name, self.score, max(self.lives, 0))
        self.score_pen.write(msg, font=("Arial", 16, "normal"))

    def show_game_over(self, rows, leaderboard_ok):
        p = self.overlay_pen
        p.clear()
        # black panel with a blue edge
        p.color("Blue", "black")
        p.pensize(3)
        p.goto(-170, 160)
        p.pendown()
        p.begin_fill()
        for _ in range(2):
            p.fd(340)
            p.rt(90)
            p.fd(320)
            p.rt(90)
        p.end_fill()
        p.penup()

        p.color("red")
        p.goto(0, 105)
        p.write("GAME OVER", align="center", font=("Arial", 28, "bold"))
        p.color("white")
        p.goto(0, 68)
        p.write("%s scored %s" % (self.player_name, self.score),
                align="center", font=("Arial", 16, "normal"))
        p.color("yellow")
        p.goto(0, 30)
        p.write("TOP 5", align="center", font=("Arial", 14, "bold"))
        p.color("white")
        if leaderboard_ok:
            for place, (name, score) in enumerate(rows, start=1):
                p.goto(0, 5 - (place - 1) * 25)
                p.write("%d. %-12s %5d" % (place, name[:12], score),
                        align="center", font=("Courier", 14, "normal"))
        else:
            p.goto(0, -20)
            p.write("Leaderboard offline - score not saved",
                    align="center", font=("Arial", 11, "normal"))
        p.color("light gray")
        p.goto(0, -145)
        p.write("Enter: play again     N: new player",
                align="center", font=("Arial", 11, "normal"))

    def clear_overlay(self):
        self.overlay_pen.clear()


def random_spot_away_from(target, min_distance=3 * HIT_RANGE):
    """Pick a random spot inside the border that is not right on top of `target`,
    so a respawned enemy can't instantly hit the player."""
    while True:
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        if abs(x - target.xcor()) > min_distance or abs(y - target.ycor()) > min_distance:
            return x, y


def ask_name(default="Player"):
    answer = turtle.textinput("Space War", "Enter your name:")
    turtle.listen()  # the pop-up steals keyboard focus; take it back
    name = (answer or default).strip()[:20]
    return name or default


def main(max_frames=None):
    # ------------------------------------------------------ sound effects
    explosion_sound = pygame.mixer.Sound("explosion.ogg")
    sniper_rifle_sound = pygame.mixer.Sound("sniper rifle.ogg")
    error_sound = pygame.mixer.Sound("windows error sound effect.ogg")
    try:
        laser_sound = pygame.mixer.Sound("laser shot.mp3")  # loaded once, not on every shot
    except pygame.error:
        laser_sound = None  # falls back to pygame.mixer.music in Missile.fire

    # ------------------------------------------------------ game objects
    game = Game()
    game.player_name = ask_name()
    game.draw_border()
    game.show_status()

    player = Player("triangle", "white", 0, 0)
    missile = Missile("triangle", "yellow", 0, 0, player, laser_sound)

    enemies = [Enemy("circle", "red", -100, 0) for _ in range(4)]
    allies = [Ally("square", "blue", 100, 0) for _ in range(4)]
    particles = [Particle("circle", "orange", 0, 0) for _ in range(60)]

    # ------------------------------------------------------ leaderboard (database)
    state = {"db_ready": False}

    def connect_db():
        """Try to reach MySQL. The game must NEVER crash because of the database,
        so every problem is caught and the game simply plays without a leaderboard."""
        if db is None:
            print("Leaderboard off: run  py -3.12 -m pip install mysql-connector-python")
            return False
        try:
            db.init_db()
            state["db_ready"] = True
        except Exception as err:
            print("Leaderboard offline (is MySQL started in XAMPP?):", err)
            state["db_ready"] = False
        return state["db_ready"]

    connect_db()

    # turtle always draws sprites on top of everything else, so while the game-over
    # panel is showing we hide them all; they come back on restart.
    all_sprites = [player, missile] + enemies + allies + particles

    def end_round():
        game.state = "gameover"
        for sprite in all_sprites:
            sprite.ht()
        rows, saved = [], False
        if state["db_ready"] or connect_db():
            try:
                db.save_score(game.player_name, game.score)
                rows = db.top_scores(5)
                saved = True
            except Exception as err:
                print("Could not save the score:", err)
                state["db_ready"] = False
        game.show_game_over(rows, saved)

    def reset_round():
        game.score = 0
        game.lives = START_LIVES
        game.state = "playing"
        game.clear_overlay()
        for sprite in all_sprites:
            sprite.st()
        player.goto(0, 0)
        player.setheading(0)
        player.velocity = 0
        missile.park()
        for enemy in enemies:
            enemy.goto(*random_spot_away_from(player))
            enemy.setheading(random.randint(0, 360))
        for ally in allies:
            ally.goto(*random_spot_away_from(player))
            ally.setheading(random.randint(0, 360))
        for particle in particles:
            particle.hide()
        game.show_status()

    # ------------------------------------------------------ keyboard bindings
    def play_again():
        if game.state == "gameover":
            game.want = "again"

    def new_player():
        if game.state == "gameover":
            game.want = "new"

    turtle.onkey(player.turn_left, "Left")
    turtle.onkey(player.turn_right, "Right")
    turtle.onkey(player.accelerate, "Up")
    turtle.onkey(player.decelerate, "Down")
    turtle.onkey(missile.fire, "space")
    turtle.onkey(play_again, "Return")
    turtle.onkey(new_player, "n")
    turtle.onkey(new_player, "N")
    turtle.listen()  # start listening for keyboard events

    # ------------------------------------------------------ main game loop
    frames = 0
    try:
        while max_frames is None or frames < max_frames:
            frames += 1
            turtle.update()
            time.sleep(FRAME_DELAY)

            # Game-over screen: the world is frozen, we only wait for a key.
            if game.state == "gameover":
                missile.park()
                if game.want == "new":
                    game.player_name = ask_name(game.player_name)
                if game.want:
                    game.want = None
                    reset_round()
                continue

            player.move()
            missile.move()

            for enemy in enemies:
                enemy.move()

                # Collision b/w player and enemy: lose points AND a life
                if player.is_collision(enemy):
                    enemy.goto(*random_spot_away_from(player))
                    explosion_sound.play()
                    game.score -= 10
                    game.lives -= 1
                    game.show_status()
                    if game.lives <= 0:
                        end_round()
                        break

                # Collision b/w missile & enemy (only while the missile is flying)
                if missile.status == "Firing" and missile.is_collision(enemy):
                    hit_x, hit_y = missile.xcor(), missile.ycor()
                    enemy.goto(*random_spot_away_from(player))
                    sniper_rifle_sound.play()
                    game.score += 55
                    game.show_status()
                    # Do explosion
                    for particle in particles:
                        particle.explode(hit_x, hit_y)
                    missile.park()  # one missile = one kill

            if game.state == "gameover":
                continue  # the round just ended; skip the rest of this frame

            for ally in allies:
                ally.move()

                # Collision b/w missile & ally
                if missile.status == "Firing" and missile.is_collision(ally):
                    ally.goto(*random_spot_away_from(player))
                    error_sound.play()
                    game.score -= 5
                    game.show_status()
                    missile.park()

            for particle in particles:
                particle.move()
    except (turtle.Terminator, tkinter.TclError):
        pass  # the game window was closed - exit quietly instead of showing an error
    finally:
        pygame.mixer.quit()

    return game, player, missile, enemies, allies, particles


if __name__ == "__main__":
    main()
