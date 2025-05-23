
#Space_war_game_FIRST_GAME_CODED_BY_SHUAIB

import os
import random #Imp for video games
import pygame
import time 

# Initialize pygame mixer
pygame.mixer.init()

#importing the turtle model

import turtle
turtle.fd(0)  #moves the turtle in the forward direction by a certain distance
turtle.speed(0) #Speed of the animation and "not the movement speed" is set to max
turtle.bgcolor("black")#Colour of the background
turtle.bgpic("realspace.gif") #BG image
turtle.title("Termination")
turtle.ht() #Hide turtle
turtle.setundobuffer(1)#Saves memory #Ignores the repeated taps
turtle.tracer(0) #Speeds up the animation

class Sprite(turtle.Turtle): #Sprite are the objects and Turtle is a class in turtle module , by this step the sprite will inherit all the abilities of turtle cls
    def __init__(self , spriteshape , color , startx , starty): #Defining its Constructer
        super(Sprite,self).__init__(shape=spriteshape)
        self.speed(0) #Speed of the animation and "not the movement speed"||NOTE: '0' is the fastest
        self.penup() #the pen is up so the turtle doesn't draw while moving , use pen down for turtle to draw
        self.color(color) #Whatever color we give to sprites 
        self.fd(0)
        self.goto(startx,starty) #Go to a start point
        self.speed = 1 #movement speed of the sprites
    def move(self):
        self.fd(self.speed)
        

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290) #sets the limit of x coordinate to 290
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290) #sets the limit of -x coordinate to -290
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290) #sets the limit of y coordinate to 290
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290) #sets the limit of -y coordinate to -290
            self.rt(60)
    def is_collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.xcor() - 20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self , spriteshape , color , startx , starty): #Defining its Constructer
        super(Player,self).__init__(spriteshape , color , startx , starty)
        self.shapesize(stretch_wid=0.4,stretch_len=1.1,outline=None)
        self.speed = 0
        self.lives = 3
    def turn_left(self):
        self.lt(45) #lt = left 45 degrees
    def turn_right(self):
        self.rt(45) #rt = right 45 degrees
    def accelerate(self):
        self.speed += 1
    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self , spriteshape , color , startx , starty): #Defining its Constructer
        super(Enemy,self).__init__(spriteshape , color , startx , starty)
        self.speed = 3
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super(Ally, self).__init__(spriteshape, color, startx, starty)
        self.speed = 10
        self.shapesize(stretch_wid = 0.4,stretch_len = 0.4, outline = None)
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290) #sets the limit of x coordinate to 290
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290) #sets the limit of -x coordinate to -290
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290) #sets the limit of y coordinate to 290
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290) #sets the limit of -y coordinate to -290
            self.lt(60)
        
class Missile(Sprite):
    def __init__(self , spriteshape , color , startx , starty): #Defining its Constructer
        super(Missile,self).__init__(spriteshape , color , startx , starty)
        self.shapesize(stretch_wid = 0.2,stretch_len = 0.4, outline = None)
        self.speed = 20
        self.status = "Ready"
        self.goto(-1000,1000)
    def fire(self):
        if self.status == "Ready":
            # Play the sound
            pygame.mixer.music.load("laser shot.mp3")
            pygame.mixer.music.play()
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "Firing"
    def move(self):
        if self.status == "ready":
            self.goto(-1000,1000)
            
        if self.status == "Firing":
            self.fd(self.speed)

        #Border_check
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000,1000)
            self.status = "Ready"

class Particle(Sprite):
    def __init__(self , spriteshape , color , startx , starty): #Defining its Constructer
        super(Particle,self).__init__(spriteshape , color , startx , starty)
        self.shapesize(stretch_wid = 0.1,stretch_len = 0.1, outline = None)
        self.goto(-1000,1000)
        self.frame = 0
    def explode(self,startx,starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(10)
            
class Game():
    def __init__(self):
        self.level = 1
        self.lives = 3
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("Blue")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300 , 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht() #hide turtle
        self.pen.pendown()
        
    def show_status(self):
        self.pen.undo()
        msg = "Score %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg , font =("Arial",16,"normal")) #Size = 16
        
#CREATION of Game Objects
        
game = Game()

#Draw game border

game.draw_border()

#Show Game status

game.show_status()
 
#CREATION of sprites

player = Player("triangle","white",0,0)
missile = Missile("triangle","yellow",0,0)

enemies = []
for i in range(4):
    enemies.append(Enemy("circle","red",-100,0))

allies = []
for i in range(4):
    allies.append(Ally("square","blue",100,0))

particles = []
for i in range(60):
    particles.append(Particle("circle","orange",0,0))
    
#Keyboard Bindings

turtle.onkey(player.turn_left , "Left") #event listener that binds a player to a specific keyboard key
turtle.onkey(player.turn_right , "Right")
turtle.onkey(player.accelerate , "Up")
turtle.onkey(player.decelerate , "Down")
turtle.onkey(missile.fire , "space")
turtle.listen() #Starts listening for keyboard events like if LEFT key is clicked it listens and turns the turtle left

#Main Game Loop

# Load sound effects
explosion_sound = pygame.mixer.Sound("explosion.ogg")
sniper_rifle_sound = pygame.mixer.Sound("sniper rifle.ogg")
error_sound = pygame.mixer.Sound("windows error sound effect.ogg")

while True:
    turtle.update()
    time.sleep(0.05)
    
    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()
        #Check for collision b/w player and enemy
        if player.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            # Play the sound
            explosion_sound.play()
            game.score -= 10
            game.show_status()
    
        #Check for collision b/w missile & enemy
        if  missile.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            # Play the sound
            sniper_rifle_sound.play()
            missile.status = "ready"
            #Increase the score
            game.score += 55
            game.show_status()
            #Do explosion
            for particle in particles:
                particle.goto(missile.xcor(),missile.ycor())
                particle.setheading(random.randint(0,360))
    for ally in allies:
        ally.move()
        #Check for collision b/w missile & ally
        if  missile.is_collision(ally):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            ally.goto(x,y)
            # Play the sound
            error_sound.play()
            missile.status = "ready"
             #Decrease the score
            game.score -= 5
            game.show_status()

    for particle in particles:
        particle.move()
        
delay = raw_input("Press Enter to finish>>")
