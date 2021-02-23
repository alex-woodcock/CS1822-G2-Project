from pygame.math import Vector2 as Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os, math

CANVAS_DIMS = (900, 900)

img_pos = [CANVAS_DIMS[0]/2, 2*CANVAS_DIMS[1]/3]

def getAngleOfVector(vectorIn):
    toReturn = math.tan(vectorIn[1]/vectorIn[0])
    return toReturn


class Sprite:
    def __init__(self, IMG, IMG_CENTRE, IMG_DIMS):
        self.IMG = IMG
        self.IMG_CENTRE = IMG_CENTRE
        self.IMG_DIMS = IMG_DIMS

        self.img_dest_dim = (self.IMG_DIMS[0]/2, self.IMG_DIMS[1]/2)
        self.img_pos = [CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2]

    def draw(self, canvas, x, y, direction):
        canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, [x, y], self.img_dest_dim, math.radians(direction))

class Clock():
    time = 0

    def tick(self):
        self.time+=1

    def transition(self, frame_duration):
        if (self.time % frame_duration == 0):
            return True
        return False

class Entity:
    def __init__(self, pos, radius, acceleration, agility, momentum, sprite):
        self.pos = pos
        self.radius = max(radius, 4)

        self.velocity = Vector(3, 0)
        self.direction = 0
        
        self.acceleration = acceleration
        self.agility = agility
        self.momentum = momentum
        self.acceleration/=self.momentum**2
        self.sprite = sprite
        
    def draw(self, canvas):
        self.sprite.draw(canvas, self.pos[0], self.pos[1], self.direction)
    
    def update(self):
        if (self.pos[0] > CANVAS_DIMS[0]):
            self.velocity += Vector(0, -5).rotate(270)
            self.direction = getAngleOfVector(self.velocity.rotate(self.direction))
        if (self.pos[0] < 0):
            self.velocity += Vector(0, -5).rotate(90)
            self.direction = getAngleOfVector(self.velocity.rotate(self.direction))
        if (self.pos[1] > CANVAS_DIMS[1]):
            self.velocity += Vector(0, -5).rotate(0)
            self.direction = getAngleOfVector(self.velocity.rotate(self.direction))
        if (self.pos[1] < 0):
            self.velocity += Vector(0, -5).rotate(180)
            self.direction = getAngleOfVector(self.velocity.rotate(self.direction))
            
        self.pos += self.velocity
        self.velocity*=self.momentum

class Enemy(Entity):
    def __init__(self, pos, radius, acceleration, agility, momentum, sprite):
        self.pos = pos
        self.radius = max(radius, 4)

        self.velocity = Vector(3, 0)
        self.direction = 0
        
        self.acceleration = acceleration
        self.agility = agility
        self.momentum = momentum
        self.acceleration/=self.momentum**2
        self.sprite = sprite

    def update(self):
        self.move()

        if self.pos[0] > CANVAS_DIMS[0]:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = CANVAS_DIMS[0]
        if self.pos[1] > CANVAS_DIMS[1]:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = CANVAS_DIMS[1]
            
        self.pos += self.velocity
        self.velocity*=self.momentum
        
    def move(self):
        #self.pos = (500, 500)

        self.velocity+=Vector(0, -self.acceleration).rotate(self.direction)
        if (math.radians(self.velocity.angle_to((0, 0))) + math.atan2(player.pos[1] - self.pos[1], player.pos[0] - self.pos[0])> 0):
            self.direction+=self.agility
        else:
            self.direction-=self.agility

class SmallZombie(Enemy):
    def __init__(self, pos):
        self.pos = pos
        self.radius = max(32, 4)

        self.velocity = Vector(3, 0)
        self.direction = 0
        
        self.acceleration = 0.45
        self.agility = 2.2
        self.momentum = 0.9
        self.acceleration/=self.momentum**2
        self.sprite = smallZombie

class LargeZombie(Enemy):
    def __init__(self, pos):
        print("test")
        self.pos = pos
        self.radius = max(128, 4)

        self.velocity = Vector(3, 0)
        self.direction = 0
        
        self.acceleration = 0.02
        self.agility = 0.3
        self.momentum = 0.98
        self.acceleration/=self.momentum**2
        self.sprite = largeZombie

class Keyboard:
    def __init__(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['w']:
            self.up = True
        if key == simplegui.KEY_MAP['s']:
            self.down = True
        if key == simplegui.KEY_MAP['d']:
            self.right = True
        if key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['w']:
            self.up = False
        if key == simplegui.KEY_MAP['s']:
            self.down = False
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False

class Interaction:
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.up:
            self.player.velocity+=Vector(0, -self.player.acceleration).rotate(self.player.direction)
        if self.keyboard.left:
            self.player.direction-=self.player.agility
        if self.keyboard.right:
            self.player.direction+=self.player.agility

def draw(canvas):
    inter.update()
    clock.tick()

    player.update()
    player.draw(canvas)
    
    for i in enemyEntitys:
        i.update()
        i.draw(canvas)

        if i.radius == 128:
            if clock.transition(200):
                enemyEntitys.append(Enemy((i.pos[0], i.pos[1]), 32, 0.45, 2.2, 0.9, smallZombie))
        
playerEntity = Sprite(simplegui._load_local_image('.\\Assets\\player.png'), (64, 64), (128, 128))
smallZombie = Sprite(simplegui._load_local_image('.\\Assets\\zombie.png'), (64, 64), (128, 128))
largeZombie = Sprite(simplegui._load_local_image('.\\Assets\\bigzombie.png'), (128, 128), (256, 256))

enemyEntitys = [SmallZombie((500,500)), SmallZombie((600,500)), SmallZombie((500,600)), LargeZombie((800, 800))]

kbd = Keyboard()
clock = Clock()

player = Entity(img_pos, 40, 0.45, 2.2, 0.9, playerEntity)
inter = Interaction(player, kbd)

frame = simplegui.create_frame('Interactions', CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
