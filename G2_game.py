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
        self.img_dest_dim = (self.IMG_DIMS[0]*0.50, self.IMG_DIMS[1]*0.50)
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
    def __init__(self, sprite, pos, radius, speed, jumpheight, frame_duration, health):
        self.sprite = sprite      
        self.pos = pos
        self.radius = max(radius, 4)
        self.speed = speed
        self.jumpheight = jumpheight
        self.velocity = Vector(0,0)
        self.frame_duration = frame_duration
        self.is_dead = False
        self.health = health
        self.on_ground = True        
    #Drawing is handled by the sprite (so that spritesheets etc can be more easily handled)
    def draw(self, canvas):
        self.sprite.draw(canvas, self.pos)

    def update(self):
        self.pos.add(self.velocity)
        self.velocity *= 0.85
        if (self.health < 0):
            self.is_dead = True
            
            
#Extends Entity
class Player(Entity):
    def shoot(self, coords):
        aimAt = Vector(self.pos.x - coords[0], self.pos.y - coords[1])
        inter.bullets.append(Bullet(aimAt))
    
    def hitByEnemy(self, enemy):
        distance = self.pos.copy().subtract(enemy.pos).length()
        if (distance - enemy.radius <= self.radius and isinstance(enemy, Enemy)):
            print("ive been hit")
            self.health -= 1
    
##Creation of Enemy class as subclass of Entity should let us
##add a "hit by bullet" function? Or maybe that should be entity as default
class Enemy(Entity):
    def hitByBullet(self, bullet):
        distance = self.pos.copy().subtract(bullet.pos).length()
        if (distance - bullet.radius <= self.radius and isinstance(bullet, Bullet)):
            print("enemy who is me has been hit")
            self.health -= 1
            bullet.toDelete = True

#zombie = Zombie(zombieSprite, Vector(800, 347), 50, 10, 20, 20, 10)      
class Zombie(Enemy):
    def __init__(self, pos):
        self.sprite = zombieSprite      
        self.pos = pos
        self.radius = max(50, 4)
        self.speed = 10
        self.jumpheight = 20
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 10
        self.on_ground = True
        
    def update(self):
        if self.health == 0:
            self.is_dead = True
        if self.is_dead == False:
            self.pos.add(Vector(-0.05,0))
            if clock.transition(self.frame_duration):
                img_centre_x = self.sprite.IMG_CENTRE[0]
                if (img_centre_x + 101.6) > 508:
                    img_centre_x = 50.8            
                self.sprite.IMG_CENTRE = (img_centre_x+101.6,55*3)
        if self.is_dead == True:
            if clock.transition(self.frame_duration):
                img_centre_x = self.sprite.IMG_CENTRE[0]
                if img_centre_x != 614.6 or img_centre_x > 614.6:
                    self.sprite.IMG_CENTRE = (img_centre_x+101.6,55)
                    
           
#Extends Entity
class Bullet(Entity):
    ##Presets variables instead of needing them custom set, because it knows its a bullet
    ##Maybe add custom variable to initialiser for damage, speed? For different guns?
    def __init__(self, aimAt):
        self.sprite = bulletSprite
        ##Seems silly to do it like this, but direct referencing means shared position!
        self.pos = Vector(player.pos.x, player.pos.y)
        self.radius = max(4, 4)
        
        aimAt.normalize();
        #No cool 180 spinz :(
        self.velocity = -aimAt*10
        
        self.toDelete = False
        
        
    #Draw inhereted from Entity
    def update(self):
        self.pos.add(self.velocity)
        
        if self.toDelete == True:
            self.pos = Vector (-1000, -1000)
            self.velocity = self.velocity * 0
        
            
class Platform():
    def __init__(self,colour):
        if colour=="gray":
            self.sprite = gray_rooftopSprite
            self.pos = Vector(155,305)
            self.ground_level = 407
            self.left = 5
            self.right = 340
        elif colour=="green":
            self.sprite = green_rooftopSprite
            self.pos = Vector(550,305)
            self.ground_level = 325
            self.left = 400
            self.right = 627
        else:
            self.sprite = red_rooftopSprite
            self.pos = Vector(790,320)
            self.ground_level = 370
            self.left = 720
            self.right = 810
            
    def draw(self,canvas):
        self.sprite.draw(canvas,self.pos)
    
    def on_platform(self,player_pos):
        if player_pos>=self.left and player_pos<=self.right:
            #this means he's on the rooftop
            return True
        else:
            #means he either jumped in a gap/so he's dead,or he's changed platforms
            return False
        
        
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
        self.last_direction = 'd'
        self.left = False
        self.right = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.last_direction = 'a'
            self.left = True
            self.any_input = True
        if key == simplegui.KEY_MAP['d']:
            self.last_direction = 'd'
            self.right = True
            self.any_input = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
            self.any_input = True
            
        #if key == simplegui.KEY_MAP['f']:
        #    player.shoot()
        #    bullet_sound.play()
        #    bullet_sound.rewind()
        #    bullet_sound.play()
            
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['a']:     
            self.left = False
        if key == simplegui.KEY_MAP['d']:         
            self.right = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False    
        else:
            self.any_input = False
            

class Mouse:
    def __init__(self):
        self.mouseClick = None
    
    def clickHandler(self, mouseClick):
        self.mouseClick = mouseClick

    def clickPos(self):
        temp = self.mouseClick
        self.mouseClick = None
        return temp  
      
class Interaction:
    def __init__(self, player, keyboard, platform_list, mouseObject):
        self.player = player
        self.keyboard = keyboard
        self.platform_list = platform_list
        
        #self.entities = [Zombie(Vector(800, 347))]
        self.entities = ExampleStageOne
        self.bullets = []
        
        self.mouse = mouseObject
        
        #this variable keeps track of which platform the player is moving  
        #it gets initialised with 0 , cause the player starts from the first rooftop
        self.pl = 0
        self.stage = 0
        self.background_x = 854/2
        
    def draw(self, canvas):
        canvas.draw_image(BACKDROP_SPRITE, 
                          (2130/2,1200/2), 
                          (2130,1200), 
                          (self.background_x-10,480/2), 
                          (854,480), 
                          0)
        canvas.draw_image(BACKDROP_SPRITE, 
                          (2130/2,1200/2), 
                          (2130,1200), 
                          (self.background_x+844,480/2), 
                          (854,480), 
                          0)
        inter.update()
        clock.tick()
        
        i=0
        while i<=2:
            self.platform_list[i].draw(canvas)
            i+=1
            
        #this lne is just for measuring it will be deleted later 
        #canvas.draw_line((720, 370), (810, 370), 1, 'Red')
        
        player.draw(canvas)
        
        for x in self.entities:
            x.draw(canvas)
        for i in self.bullets:
            i.draw(canvas)
        #player.update()
        #player.draw(canvas)
        #zombie.update()
        #zombie.draw(canvas)
        
        mouseReturn = self.mouse.clickPos()
        if mouseReturn != None:
            player.shoot(mouseReturn)
    

    def update(self):
        if self.stage == 0:
            if self.player.pos.x <= 0:
                self.player.pos.x = 0
        if self.stage != 0:
            if self.player.pos.x <= 0:
                self.stage -= 1
                self.player.pos.x = 854
        if self.player.pos.x > 854:
            self.stage += 1
            self.player.pos.x = 0

               
        if self.keyboard.left:
            if self.stage == 0 and self.player.pos.x <= 0:
                self.background_x += 0
            else:
                self.background_x += 0.05
            self.player.velocity.add(Vector(-0.3, 0))
            if clock.transition(self.player.frame_duration):
                img_centre_x = self.player.sprite.IMG_CENTRE[0]
                if (img_centre_x + 101.6) > 610:
                            img_centre_x = 50.8
                self.player.sprite.IMG_CENTRE = (img_centre_x+101.6,(329/6)*3)            
        if self.keyboard.right:
            self.background_x -= 0.05
            self.player.velocity.add(Vector(0.3, 0))
            if clock.transition(self.player.frame_duration):
                img_centre_x = self.player.sprite.IMG_CENTRE[0]
                if (img_centre_x + 101.6) > 610:
                    img_centre_x = 50.8
                self.player.sprite.IMG_CENTRE = (img_centre_x+101.6,(329/6)*5)
        if self.keyboard.space and self.player.on_ground:
            if self.keyboard.last_direction == 'a':
                self.player.sprite.IMG_CENTRE = ((610/12)*5,(329/6))
            if self.keyboard.last_direction == 'd':
                self.player.sprite.IMG_CENTRE = ((610/12)*7,(329/6))
            self.player.on_ground = False
            self.player.velocity.add(Vector(0, -5))
        if self.keyboard.any_input == False and self.keyboard.last_direction == 'd':
            self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6))
        if self.keyboard.any_input == False and self.keyboard.last_direction == 'a':
            self.player.sprite.IMG_CENTRE = ((610/12),(329/6))
        if self.player.on_ground == False:
            self.player.velocity.add(Vector(0, 1))
        #Below code checks if player is on floor, should change for platform
        if self.player.pos.y+70 > 480:
            self.player.on_ground = True
        player.update()
        
        for i in self.bullets:
            i.update()
        
        for x in self.entities:
            x.update()
            player.hitByEnemy(x)
            if (isinstance(x, Enemy)):
                for b in self.bullets:
                    x.hitByBullet(b)
                    
        
#Defining sprites
zombieSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))
bulletSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/bullet_sprite.png"), (50, 50), (100, 100))
playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheetV2.png"), ((610/12)*3, 329/6), (610/6, 329/3))

gray_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/gray_rooftop.png"),(697 / 2, 697 / 2) ,(697, 697))
green_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/green_rooftop.png"),(754/2,754/2),(754,754))
red_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/red_rooftop.png"),(800/2,800/2),(800,800))

gray_rooftop = Platform("gray")
green_rooftop = Platform("green")
red_rooftop = Platform("red")

#creating a list to store the platforms
platform_list = []
platform_list.append(gray_rooftop)
platform_list.append(green_rooftop)
platform_list.append(red_rooftop)

kbd = Keyboard()
clock = Clock()

player = Player(playerSprite, Vector(115, 380), 50, 10, 20, 5, 3)

ExampleStageOne = [Zombie(Vector(800, 347)), Zombie(Vector(600, 300))]

inter = Interaction(player, kbd, platform_list, Mouse())

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("G2 game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.set_mouseclick_handler(inter.mouse.clickHandler)
# Start the frame animation
frame.start()