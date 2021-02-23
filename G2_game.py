import math, random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
try:
    from user305_o32FtUyCKk_0 import Vector
except ImportError:
    from pygame.math import Vector2 as Vector

# The canvas dimensions
CANVAS_DIMS = (1280, 720)
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720

##For non-spritesheet based sprites
class Sprite:
    def __init__(self, IMG, IMG_CENTRE, IMG_DIMS):
        self.IMG = IMG
        self.IMG_CENTRE = IMG_CENTRE
        self.IMG_DIMS = IMG_DIMS

        self.img_dest_dim = (self.IMG_DIMS[0]/2, self.IMG_DIMS[1]/2)
        self.img_pos = [CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2]

    #Pos = Position in game world
    def draw(self, canvas, pos):
        canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, [pos[0],pos[1]], self.img_dest_dim, 0)

##Must be edited to handle spritesheets
class Spritesheet(Sprite):
    def __init__(self):#<--- spritesheet variable stuff
        #do stuff
        a = True

##All Entities have: An assigned sprite, Position, Radius (idk what that does), Movement speed, Jump height
class Entity():
    def __init__(self, sprite, pos, radius, movespeed, jumpheight):
        self.sprite = sprite
        
        self.pos = pos
        self.radius = max(radius, 4)

        self.speed = movespeed
        self.jumpheight = jumpheight

        self.velocity = Vector(0,0)
        
    #Drawing is handled by the sprite (so that spritesheets etc can be more easily handled)
    def draw(self, canvas):
        print(self.pos)
        self.sprite.draw(canvas, self.pos)

    def update(self):
        self.pos += self.velocity
        self.velocity *= 0.9

class Clock():
    time = 0

    def tick(self):
        self.time+=1

    def transition(self, frame_duration):
        if (self.time % frame_duration == 0):
            return True
        return False

class Keyboard:
    def __init__(self):
        self.left = False
        self.right = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['d']:
            self.right = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['d']:
            self.right = False

class Interaction:
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard
        
    def draw(self, canvas):
        a = True

    def update(self):
        if self.keyboard.left:
            self.player.pos[0] -= self.player.speed/5
        if self.keyboard.right:
            self.player.pos[0] += self.player.speed/5

def draw(canvas):
    inter.update()
    clock.tick()

    player.update()
    player.draw(canvas)
    
#Defines a sprite!
playerSprite = Sprite(simplegui._load_local_image('.\\sprite folder\\character\\main_chara_spritesheets\\mc_Idle_right.png'), (50, 50), (100, 100))

kbd = Keyboard()
clock = Clock()

player = Entity(playerSprite, (200, 200), 50, 10, 20)
inter = Interaction(player, kbd)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("G2 game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

# Start the frame animation
frame.start()
