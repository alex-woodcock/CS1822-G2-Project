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
#Background sprites
BACKDROP_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/backdrop.png') 
STARTMENU_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/start_menu.png') 
STORY5_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story5.png') 
#sounds
bullet_sound = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/bullet_shot.mp3')
bullet_sound.set_volume(0.5)
gun_reload = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/gun_reload.mp3')
gun_reload.set_volume(0.5)
menu_music = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/menu_music.mp3')
menu_music.set_volume(0.5)
zombie_death = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/zombie_death.mp3')
zombie_death.set_volume(0.5)
player_hit = simplegui.load_sound('http://personal.rhul.ac.uk/zhac/315/player_hit.mp3')
player_hit.set_volume(0.5)


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
        
        self.ammo = 7
        self.can_shoot = True
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
        self.ammo = 7
        self.ammo_capacity = 21
        self.can_shoot = True
        self.can_reload = True
        self.lifes = 3
        self.game_over = False
        
    def shoot(self, coords):
        if self.ammo > 0:
            self.can_shoot = True
        if self.ammo == 0:
            self.can_shoot = False
        if self.can_shoot == True:
            bullet_sound.play()
            bullet_sound.rewind()
            bullet_sound.play()
            aimAt = Vector(self.pos.x - coords[0], self.pos.y - coords[1])
            inter.bullets.append(Bullet(aimAt))
            self.ammo -= 1
    
    def hitByEnemy(self, enemy):
        distance = self.pos.copy().subtract(enemy.pos).length()
        if (distance - enemy.radius <= self.radius and isinstance(enemy, Enemy)):
            print("ive been hit")
            player_hit.play()
            player_hit.rewind()
            player_hit.play()
            self.health -= 1
        #need to add invulnerability
        if self.health <= 0:
            if self.lifes == 0:
                self.game_over = True
            else:
                self.lifes -= 1
                self.pos = Vector(115, 380)
                #temporary health
                self.health = 10
                self.ammo = 7
                self.ammo_capacity = 21
                
    def run_right(self):
        self.velocity.add(Vector(0.3, 0))
        if clock.transition(self.frame_duration):
            img_centre_x = self.sprite.IMG_CENTRE[0]
            if (img_centre_x + 101.6) > 610:
                img_centre_x = 50.8
            self.sprite.IMG_CENTRE = (img_centre_x+101.6,(329/6)*5)   
    
    def run_left(self):
        self.velocity.add(Vector(-0.3, 0))
        if clock.transition(self.frame_duration):
            img_centre_x = self.sprite.IMG_CENTRE[0]
            if (img_centre_x + 101.6) > 610:
                img_centre_x = 50.8
            self.sprite.IMG_CENTRE = (img_centre_x+101.6,(329/6)*3)      
    
    def reload(self):
        if self.ammo_capacity <= 0:
            self.can_reload = False
        if self.can_reload:
            gun_reload.play()
            ##Shoot timer handled by Interaction instead of player?
            inter.shoot_timer=60
            if self.ammo == 0:
                if self.ammo_capacity <= 7:
                    self.ammo = self.ammo_capacity
                    self.ammo_capacity = 0
                else:
                    self.ammo_capacity -= 7
                    self.ammo = 7
            else:
                ammo_used = 7-self.ammo
                if self.ammo_capacity - ammo_used < 0:
                    self.ammo += self.ammo_capacity
                    self.ammo_capacity = 0
                else:
                    self.ammo_capacity -= ammo_used
                    self.ammo = 7
    
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
        self.sprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))     
        self.pos = pos
        self.radius = max(25, 4)
        self.speed = 10
        self.jumpheight = 20
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 5
        self.on_ground = True
        self.left_right = 'left'
        
    def update(self):
        if self.health > 0:
            if clock.transition(self.frame_duration*5):  
                if self.left_right == 'left':
                    self.left_right = 'right'
                if self.left_right == 'right':
                    self.left_right = 'left'  
                    
            if self.left_right == 'left':
                self.pos.add(Vector(-0.05* self.speed/10,0) )
                if clock.transition(self.frame_duration):
                    img_centre_x = self.sprite.IMG_CENTRE[0]
                    if (img_centre_x + 101.6) > 508:
                        img_centre_x = 50.8            
                    self.sprite.IMG_CENTRE = (img_centre_x+101.6,55*3)
            if self.left_right == 'right':
                self.pos.add(Vector(0.05* self.speed/10,0))
                if clock.transition(self.frame_duration):
                    img_centre_x = self.sprite.IMG_CENTRE[0]
                    if (img_centre_x + 101.6) > 508:
                        img_centre_x = 50.8            
                    self.sprite.IMG_CENTRE = (img_centre_x+101.6,55*5)                                
        if self.health <= 0:
            zombie_death.play()
            if clock.transition(self.frame_duration):
                img_centre_x = self.sprite.IMG_CENTRE[0]
                if not img_centre_x+101.6 > 610:
                    self.sprite.IMG_CENTRE = (img_centre_x+101.6,55)
                else:
                    self.is_dead = True

class BossZombie(Zombie):
    def __init__(self, pos):
        self.sprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))  
        self.sprite.img_dest_dim = (self.sprite.IMG_DIMS[0]*2.50, self.sprite.IMG_DIMS[1]*2.50)
        self.pos = pos
        self.radius = max(80, 4)
        self.speed = 50
        self.jumpheight = 20
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 20
        self.on_ground = True
        self.left_right = 'left'
           
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
        self.velocity = -aimAt*20
        
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
            self.ground_level = 380
            self.left = 5
            self.right = 340
            self.normal = Vector(1,0)
        elif colour=="green":
            self.sprite = green_rooftopSprite
            self.pos = Vector(550,305)
            self.ground_level = 300
            self.left = 400
            self.right = 627
        else:
            self.sprite = red_rooftopSprite
            self.pos = Vector(790,320)
            self.ground_level = 345
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
        self.r = False

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
        if key == simplegui.KEY_MAP['r']:
            player.reload()
            
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
        self.pl = 0
        #self.entities = [Zombie(Vector(800, 347))]
        self.entities = stages[0]
        self.bullets = []
        
        self.mouse = mouseObject
        
        #this variable keeps track of which platform the player is moving  
        #it gets initialised with 0 , cause the player starts from the first rooftop
        self.drawIsTrue = False
        self.pl = 0
        self.stage = -2
        self.background_x = 854/2
        self.time_left = 120
        
        self.shoot_timer = 0
        
    def draw(self, canvas):
        if self.stage == -2:
            canvas.draw_image(STARTMENU_SPRITE,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)
        if self.stage == -1:
            canvas.draw_image(STORY5_SPRITE,
                              (2800/2,1577/2),
                              (2800,1577),
                              (854/2,480/2),
                              (854,480),
                              0)            
            
              
        if self.stage >= 0:    
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
        
        if self.drawIsTrue:
            time_left = str(self.time_left)
            ammo = str(self.player.ammo)
            ammo_capacity = str(self.player.ammo_capacity)
            lives = str(self.player.lifes)
            canvas.draw_text('Time left: '+ time_left, (20, 40), 40, 'Red')
            canvas.draw_text('Ammo:'+ammo+'/'+ammo_capacity, (20, 60), 20, 'Red')
            canvas.draw_text('Lives: ' + lives, (20,100), 40,'Red')
            
            if clock.transition(100):
                self.time_left -= 1
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


    def player_fell(self):
        self.player.lifes -= 1
        self.player.pos = Vector(115, 380)
        self.pl = "Gray"
        if self.player.lifes == 0:
            self.player.game_over = True
    

    def update(self):
        if self.player.game_over:
            self.drawIsTrue = False
            self.stage = -1
            self.player.game_over = False
            self.player.lifes = 3
            
            
        mouseReturn = self.mouse.clickPos()     
        if self.stage < 0:
            menu_music.play()
            if mouseReturn != None:
                self.stage += 1
                if (self.stage) == 0:
                    menu_music.rewind()
                    self.drawIsTrue = True

        else:
            if self.stage == 0:
                if self.player.pos.x <= 0:
                    self.player.pos.x = 0
            if self.stage != 0:
                if self.player.pos.x <= 0:
                    self.stage -= 1
                    self.player.pos.x = 854
            if self.player.pos.x > 854:
                #Uses stage number to load from array of preset stages
                print(self.stage)
                self.stage += 1
                if (self.stage > len(stages)):
                    self.stage = len(stages)
                self.entities = stages[self.stage]
                self.player.pos.x = 0
                self.player.ammo = 7
                self.player.ammo_capacity = 21


            if self.keyboard.left:
                if self.stage == 0 and self.player.pos.x <= 0:
                    self.background_x += 0
                else:
                    self.background_x += 0.05
                    self.player.run_left()
         
            if self.keyboard.right:
                self.background_x -= 0.05
                self.player.run_right()
                
            if self.keyboard.r:
                self.player.reload()
                
                
            if self.player.pos.x > gray_rooftop.right and self.player.pos.x < green_rooftop.left:
                self.player.on_ground = False
            if self.keyboard.space and self.player.on_ground:
                if self.keyboard.last_direction == 'a':
                    self.player.sprite.IMG_CENTRE = ((610/12)*5,(329/6))
                if self.keyboard.last_direction == 'd':
                    self.player.sprite.IMG_CENTRE = ((610/12)*7,(329/6))
                self.player.on_ground = False
                self.player.velocity.add(Vector(0, -20))
            if self.keyboard.any_input == False and self.keyboard.last_direction == 'd':
                self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6))
            if self.keyboard.any_input == False and self.keyboard.last_direction == 'a':
                self.player.sprite.IMG_CENTRE = ((610/12),(329/6))
            if self.player.on_ground == False:
                self.player.velocity.add(Vector(0, 0.75))
                
            if self.player.pos.x >= gray_rooftop.left and self.player.pos.x <= gray_rooftop.right:
                self.pl = "Gray"    
            if self.player.pos.x >= green_rooftop.left and self.player.pos.x <= green_rooftop.right:
                self.pl = "Green"
            if self.player.pos.x >= red_rooftop.left and self.player.pos.x <= red_rooftop.right:
                self.pl = "Red"    
            if self.player.pos.y >= gray_rooftop.ground_level and self.player.pos.x >= gray_rooftop.left and self.player.pos.x <= gray_rooftop.right and self.pl == "Gray":
                self.player.pos.y = gray_rooftop.ground_level
                self.player.on_ground = True
            if self.player.pos.y >= green_rooftop.ground_level and self.player.pos.x >= green_rooftop.left and self.player.pos.x <= green_rooftop.right and self.pl == "Green":
                self.player.pos.y = green_rooftop.ground_level
                self.player.on_ground = True
            if self.player.pos.y >= red_rooftop.ground_level and self.player.pos.x >= red_rooftop.left and self.player.pos.x <= red_rooftop.right and self.pl == "Red":
                self.player.pos.y = red_rooftop.ground_level
                self.player.on_ground = True        
          
                 
                    
            
            #Below code checks if player is on floor, should change for platform

            if self.player.pos.y >= 480:
                self.player_fell() 

            if self.player.pos.x > green_rooftop.right and self.player.pos.x < red_rooftop.left:
                self.player.on_ground = False
            player.update()
            
            if mouseReturn != None:
                if self.shoot_timer <= 0:
                    player.shoot(mouseReturn)
                    self.shoot_timer = 25
            if self.shoot_timer > 0:
                self.shoot_timer -= 1

            for i in self.bullets:
                i.update()

            for x in self.entities:
                x.update()
                player.hitByEnemy(x)
                if x.is_dead == True:
                    self.entities.remove(x)
                if (isinstance(x, Enemy)):
                    for b in self.bullets:
                        x.hitByBullet(b)

        
#Defining sprites
bulletSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/bullet_sprite.png"), (12.5, 12.5), (25, 25))
playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheetV2.png"), ((610/12)*3, 329/6), (610/6, 329/3))

##USE FOR REFERENCE WHEN PROGRAMMING ONLY
#zombieSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))

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

player = Player(playerSprite, Vector(115, 380), 25, 10, 20, 5, 3)


ExampleStageOne = [Zombie(Vector(800, 347)), Zombie(Vector(600, 300)),Zombie(Vector(320, 380))]
ExampleStageTwo = [BossZombie(Vector(800, 347))]

stages = [ExampleStageOne, ExampleStageTwo]

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