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

#Background sprite
BACKDROP_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/backdrop.png')

##For non-spritesheet based sprites
class Sprite:
    def __init__(self, IMG, IMG_CENTRE, IMG_DIMS):
        self.IMG = IMG
        self.IMG_CENTRE = IMG_CENTRE
        self.IMG_DIMS = IMG_DIMS
        self.img_dest_dim = (self.IMG_DIMS[0], self.IMG_DIMS[1])
        self.img_pos = [CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2]

    #Pos = Position in game world
    def draw(self, canvas, pos):
        canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, [pos.x,pos.y], self.img_dest_dim, 0)

##Must be edited to handle spritesheets
class Spritesheet(Sprite):
    def __init__(self):#<--- spritesheet variable stuff
        #do stuff
        a = True

##All Entities have: An assigned sprite, Position, Radius (idk what that does), Movement speed, Jump height
class Entity():
    def __init__(self, sprite, pos, radius, speed, jumpheight):
        self.sprite = sprite
        
        self.pos = pos
        self.radius = max(radius, 4)

        self.speed = speed
        self.jumpheight = jumpheight

        self.velocity = Vector(0,0)
        
    #Drawing is handled by the sprite (so that spritesheets etc can be more easily handled)
    def draw(self, canvas):
        self.sprite.draw(canvas, self.pos)

    def update(self):
        self.pos.add(self.velocity)
        self.velocity *= 0.85

#Extends Entity
class Player(Entity):
    def shoot(self):
        bullets.append(Bullet())

#Extends Entity
class Bullet(Entity):
    ##Presets variables instead of needing them custom set, because it knows its a bullet
    ##Maybe add custom variable to initialiser for damage, speed? For different guns?
    def __init__(self):
        self.sprite = bulletSprite
        ##Seems silly to do it like this, but direct referencing means shared position!
        self.pos = Vector(player.pos.x, player.pos.y)
        self.radius = max(4, 4)

        self.velocity = Vector(10, 0)

    #Draw inhereted from Entity

    def update(self):
        self.pos.add(self.velocity)
        ##bullets dont slow down!

        ##If bullet touching thing, then do damage and stuff!
        #if (touching thing):
            #do damage
            #remove self from bullets list

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
        self.any_input = False
        self.last_key = 'w'
        self.left = False
        self.right = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.left = True
            self.any_input = True
        if key == simplegui.KEY_MAP['d']:
            self.right = True
            self.any_input = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
            self.any_input = True
        if key == simplegui.KEY_MAP['f']:
            player.shoot()
            

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.left = False
            self.last_key = 'a'
        if key == simplegui.KEY_MAP['d']:
            self.right = False
            self.last_key = 'd'
        if key == simplegui.KEY_MAP['space']:
            self.space = False
            self.last_key = 'space'
        else:
            self.any_input = False
            

class Interaction:
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard
        
    def draw(self, canvas):
        a = True

    def update(self):
        ##need to animate walking animations
        if self.keyboard.left:
            self.player.sprite.IMG_CENTRE = ((610/12),(329/6)*3)
            self.player.velocity.add(Vector(-1, 0))
        if self.keyboard.right:
            self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6)*5)
            self.player.velocity.add(Vector(1, 0))
        if self.keyboard.space:
            self.player.sprite.IMG_CENTRE = ((610/12)*7,(329/6))
            self.player.velocity.add(Vector(0, -2))
        if self.keyboard.any_input == False and self.keyboard.last_key == 'd':
            self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6))
        if self.keyboard.any_input == False and self.keyboard.last_key == 'a':
            self.player.sprite.IMG_CENTRE = ((610/12),(329/6))
          
        ##Jump mechanic needs fixing, dosent work with short presses and player falls too slow
        if self.player.pos.y+70 <= 700 and self.keyboard.space == False:
            self.player.velocity.add(Vector(0,1))
            
            
            

def draw(canvas):
    ##temporary drawing of background, maybe add parallax
    canvas.draw_image(BACKDROP_SPRITE, 
                      (1280/2,720/2), 
                      (1280,720), 
                      (1280/2,720/2), 
                      (1280,720), 
                      0)
    inter.update()
    clock.tick()
    player.update()
    player.draw(canvas)

    for i in bullets:
        i.update()
        i.draw(canvas)
    
#Defines a sprite!
SHEET_URL = "http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"
##player sheet dimensions 610 x 329

playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"), (150, 329/6), (100, 100))
###NEED BULLET SPRITE PLS TY
bulletSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"), (150, 329/6), (100, 100))

playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"), ((610/12)*3, 329/6), (610/6, 329/3))

kbd = Keyboard()
clock = Clock()

player = Player(playerSprite, Vector(200, 650), 50, 10, 20)
inter = Interaction(player, kbd)

bullets = []

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("G2 game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

# Start the frame animation
frame.start()
