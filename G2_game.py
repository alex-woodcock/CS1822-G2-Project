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
CANVAS_DIMS = (854, 480)
CANVAS_WIDTH = 854
CANVAS_HEIGHT = 480
#Background sprite
BACKDROP_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/backdrop.png')

#Bullet sound
bullet_sound = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/bullet_shot.mp3')
bullet_sound.set_volume(0.5)

##For non-spritesheet based sprites
class Sprite:
    def __init__(self, IMG, IMG_CENTRE, IMG_DIMS):
        self.IMG = IMG
        self.IMG_CENTRE = IMG_CENTRE
        self.IMG_DIMS = IMG_DIMS
        self.img_dest_dim = (self.IMG_DIMS[0]*0.75, self.IMG_DIMS[1]*0.75)
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
    def __init__(self, sprite, pos, radius, speed, jumpheight, frame_duration):
        self.sprite = sprite      
        self.pos = pos
        self.radius = max(radius, 4)
        self.speed = speed
        self.jumpheight = jumpheight
        self.velocity = Vector(0,0)
        self.frame_duration = frame_duration
        self.is_dead = False
        
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
        
class Zombie(Entity):
    def update(self):
        if self.is_dead == False:
            self.pos.add(Vector(-0.1,0))
            if clock.transition(self.frame_duration):
                img_centre_x = self.sprite.IMG_CENTRE[0]
                if (img_centre_x + 101.6) > 508:
                    img_centre_x = 50.8            
                self.sprite.IMG_CENTRE = (img_centre_x+101.6,55*3)
"""
#bullet hitting zombie not working
        else:
            for i in bullets:
                if i.pos.x == self.pos.x:
                    self.is_dead = True
"""


#Extends Entity
class Bullet(Entity):
    ##Presets variables instead of needing them custom set, because it knows its a bullet
    ##Maybe add custom variable to initialiser for damage, speed? For different guns?
    def __init__(self):
        self.sprite = bulletSprite
        ##Seems silly to do it like this, but direct referencing means shared position!
        self.pos = Vector(player.pos.x+30, player.pos.y)
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
        self.last_key = ''
        self.left = False
        self.right = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.last_key = 'a'
            self.left = True
            self.any_input = True
        if key == simplegui.KEY_MAP['d']:
            self.last_key = 'd'
            self.right = True
            self.any_input = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        if key == simplegui.KEY_MAP['f']:
            player.shoot()
            bullet_sound.play()
            bullet_sound.rewind()
            bullet_sound.play()
        else:
            self.any_input = True
            

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.last_key = 'a'
            self.left = False
        if key == simplegui.KEY_MAP['d']:
            self.last_key = 'd'
            self.right = False            
        if key == simplegui.KEY_MAP['space']:
            self.space = False
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
            self.player.velocity.add(Vector(-0.6, 0))
        if self.keyboard.right:
            self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6)*5)
            self.player.velocity.add(Vector(0.6, 0))
        if self.keyboard.space:
            self.player.sprite.IMG_CENTRE = ((610/12)*7,(329/6))
            self.player.velocity.add(Vector(0, -1.5))
        if self.keyboard.any_input == False and self.keyboard.last_key == 'd':
            self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6))
        if self.keyboard.any_input == False and self.keyboard.last_key == 'a':
            self.player.sprite.IMG_CENTRE = ((610/12),(329/6))          
        ##Jump mechanic needs fixing, dosent work with short presses and player falls too slow
        if self.player.pos.y+70 <= 480 and self.keyboard.space == False:
            self.player.velocity.add(Vector(0,1))
        
            
            
            

def draw(canvas):
    ##temporary drawing of background, maybe add parallax
    canvas.draw_image(BACKDROP_SPRITE, 
                      (1280/2,720/2), 
                      (1280,720), 
                      (854/2,480/2), 
                      (854,480), 
                      0)
    inter.update()
    clock.tick()
    player.update()
    player.draw(canvas)
    zombie.update()
    zombie.draw(canvas)
    

    for i in bullets:
        i.update()
        i.draw(canvas)
    
#Defines a sprite!
SHEET_URL = "http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"
##player sheet dimensions 610 x 329

zombieSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))
bulletSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/bullet_sprite.png"), (50, 50), (100, 100))
playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheet.png"), ((610/12)*3, 329/6), (610/6, 329/3))

kbd = Keyboard()
clock = Clock()

player = Player(playerSprite, Vector(100, 450), 50, 10, 20, 30)
zombie = Zombie(zombieSprite, Vector(700, 441), 50, 10, 20, 10)
inter = Interaction(player, kbd)

bullets = []
zombies = []


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("G2 game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

# Start the frame animation
frame.start()