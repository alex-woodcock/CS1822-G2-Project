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
STORY1_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story1.png') 
STORY2_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story2.png') 
STORY3_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story3.png') 
STORY4_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story4.png') 
STORY5_SPRITE = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/story5.png')
GAME_OVER = simplegui.load_image('http://personal.rhul.ac.uk/zhac/315/game_over.png') 
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
locked_door = simplegui.load_sound('http://personal.rhul.ac.uk/zjac/379/locked_door.mp3')
locked_door.set_volume(0.5)
door_opening = simplegui.load_sound('http://personal.rhul.ac.uk/zjac/379/door_opening.mp3')
door_opening.set_volume(0.5)


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
        self.speed = 100
        self.jumpheight = 20
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 5
        self.rotate = True
        self.left_right = 'left'
        self.current_platform = ''
        
    def update(self):

        if self.health > 0:
            if self.rotate == False:
                if self.left_right == 'left':
                    self.left_right = 'right'
                else:
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
                    
class FlyingZombie(Zombie):
    def __init__(self, pos):
        self.sprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/flying_zombie.png"), (51, 55*3), (100, 100))
        self.sprite.img_dest_dim = (self.sprite.IMG_DIMS[0]*0.6, self.sprite.IMG_DIMS[1]*0.6)
        self.pos = pos
        self.radius = max(25, 4)
        self.speed = 10
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 5
        self.left_right = 'left'
        self.current_platform = ''
        
        
    def update(self):
        #add zombie shooting here
        if self.health > 0:
            if clock.transition(self.frame_duration*15):  
                if self.left_right == 'left':
                    self.left_right = 'right'
                else:
                    self.left_right = 'left'
            if self.left_right == 'left':
                self.pos.add(Vector(-0.5* self.speed/10,0) )
                if clock.transition(self.frame_duration):
                    img_centre_x = self.sprite.IMG_CENTRE[0]
                    if (img_centre_x + 100) > 250:
                        img_centre_x = 50            
                    self.sprite.IMG_CENTRE = (img_centre_x+100,50)               
                
            if self.left_right == 'right':
                self.pos.add(Vector(0.5* self.speed/10,0))
                if clock.transition(self.frame_duration):
                    img_centre_x = 450
                    if (img_centre_x + 100) > 650:
                        img_centre_x = 450            
                    self.sprite.IMG_CENTRE = (img_centre_x+100,150)                        
        if self.health <= 0:
            zombie_death.play()
            self.pos.add(Vector(0,5))
            if clock.transition(self.frame_duration):
                img_centre_x = self.sprite.IMG_CENTRE[0]
                if not img_centre_x+100 > 600:
                    self.sprite.IMG_CENTRE = (img_centre_x+100,50)
                else:
                    self.is_dead = True
                    

                    

        
        
        
        
        
class BossZombie(Zombie):
    def __init__(self, pos):
        self.sprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))  
        self.sprite.img_dest_dim = (self.sprite.IMG_DIMS[0]*5, self.sprite.IMG_DIMS[1]*5)
        self.pos = pos
        self.radius = max(200, 4)
        self.speed = 50
        self.jumpheight = 20
        self.velocity = Vector(0,0)
        self.frame_duration = 20
        self.is_dead = False
        self.health = 20
        self.on_ground = True
        self.left_right = 'left'
        
    def update(self):
        if self.health > 0:                      
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
    def __init__(self,colour,pos):
        if colour=="gray":
            self.sprite = gray_rooftopSprite
            self.pos = pos 
            self.ground_level = 380
            self.left = 0
            self.right = 340
            self.normal = Vector(1,0)
            
        elif colour=="green":
            self.sprite = green_rooftopSprite
            self.pos = pos 
            self.ground_level = 300
            self.left = 400
            self.right = 627
            
        elif colour =="red":
            self.sprite = red_rooftopSprite
            self.pos = pos 
            self.ground_level = 345
            self.left = 720
            self.right = 810
            
    def draw(self,canvas):
        self.sprite.draw(canvas,self.pos)
    
    def __repr__(self):
            return str("This is platform" + str(self.ground_level))        
        
        
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
        self.o = False
        self.flag = False #controls the sound of the fisrt door
        self.flag2=False #controls the sound of the second door
        self.flag3 = False	#controls message for the first door
        self.flag4 = False #controls message for the second door
        self.flag5 = False #makes sure flag4 can only be true if player stands in front of the second door

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
        if key == simplegui.KEY_MAP['o']:
            self.o= True
            if self.flag == True: 
                locked_door.play()
                self.flag= False 
            if self.flag2==True :
                door_opening.play()
                self.flag2==False
              
            
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['a']:     
            self.left = False
        if key == simplegui.KEY_MAP['d']:         
            self.right = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False
        else:
            self.any_input = False
            
        if key == simplegui.KEY_MAP['o']:
            self.flag3 = True
            if self.flag5==True:
                self.flag4 = True
            self.o= False

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
        self.current_platform = ''
        #self.entities = [Zombie(Vector(800, 347))]
        self.entities = stages[0]
        self.bullets = []
        
        self.mouse = mouseObject
        
        #this variable keeps track of which platform the player is moving  
        #it gets initialised with 0 , cause the player starts from the first rooftop
        self.drawIsTrue = False
        self.pl = 0
        self.stage = -6
        self.background_x = 854/2
        self.time_left = 120
        
        self.open = False #checks if door is open
        
        self.shoot_timer = 0
        
    def draw(self, canvas):
        if self.stage == -7:
            canvas.draw_image(GAME_OVER,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)             
            
        if self.stage == -6:
            canvas.draw_image(STARTMENU_SPRITE,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)            
               
        if self.stage == -5:
            canvas.draw_image(STORY1_SPRITE,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)
            
        if self.stage == -4:
            canvas.draw_image(STORY2_SPRITE,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)
            
        if self.stage == -3:
            canvas.draw_image(STORY3_SPRITE,
                              (2556/2,1440/2),
                              (2556,1440),
                              (854/2,480/2),
                              (854,480),
                              0)
            
        if self.stage == -2:
            canvas.draw_image(STORY4_SPRITE,
                              (2130/2,1200/2),
                              (2130,1200),
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
            
        #if self.stage == 1:
            #new_platform_list = []
            #new_platform_list.append(Platform("red",Vector(155,320)))
            #self.platform_list = new_platform_list
            
            
        inter.update()
        clock.tick()
        
        
        if (self.player.pos.x>805) and (self.open==False):
            self.player.pos.x = 805
            
       
        
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
          
            for platform in self.platform_list:
                platform.draw(canvas)
               

            #this lne is just for measuring it will be deleted later 
            canvas.draw_line((805, 270), (820, 270), 1, 'Red')

            player.draw(canvas)
            
            
        #code for the doors
            if self.player.pos.x >=190 and self.player.pos.x<=230: 
                self.keyboard.flag=True
                #third argument decides which door it is
                self.give_info(canvas,"Press 'O' to open the door",1)
                if self.keyboard.flag3 == True:
                    self.give_info(canvas,"    This door is locked!",1)
                    self.keyboard.flag3==False
                    
                
            if self.player.pos.x>=740:
                self.keyboard.flag5 = True
                self.keyboard.flag2=True
                self.give_info(canvas,"Press 'O' to open the door",2)
                if self.keyboard.flag4==True:
                    self.open  = True
                    self.give_info(canvas,"  The door is now open!",2)
                    self.keyboard.flag4==False
            
                    
                    
            for x in self.entities:
                x.draw(canvas)
            for i in self.bullets:
                i.draw(canvas)
    
    #code for displaying info boxes
    def give_info(self,canvas,info,door):
        
        if door==1:
            canvas.draw_line((235, 322),  (340, 322), 15, 'white')

            canvas.draw_line((235, 315), (340, 315), 1, 'black')
            canvas.draw_line((235, 330), (340, 330), 1, 'black')
            canvas.draw_line((235, 315), (235, 330), 1, 'black')
            canvas.draw_line((340, 315), (340, 330), 1, 'black')

            canvas.draw_text(info, (240, 325), 9, 'black')
        else:
            canvas.draw_line((700, 263),  (805, 263), 15, 'white')

            canvas.draw_line((700, 270), (805, 270), 1, 'black')
            canvas.draw_line((700, 255), (805, 255), 1, 'black')
            canvas.draw_line((700, 255), (700, 270), 1, 'black')
            canvas.draw_line((805, 255), (805, 270), 1, 'black')
            
            canvas.draw_text(info, (705, 265), 9, 'black')
            

    def player_fell(self):
        self.player.lifes -= 1
        self.player.pos = Vector(115, 380)
        self.pl = "Gray"
        if self.player.lifes == 0:
            self.player.game_over = True
    

    def update(self):
        if self.player.game_over:
            self.drawIsTrue = False
            self.stage = -7
            self.player.game_over = False
            self.player.lifes = 3
            
            
        mouseReturn = self.mouse.clickPos()     
        if self.stage < 0:
            menu_music.play()
            if mouseReturn != None:
                if self.stage == -7:
                    self.stage = -1
                else:    
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
                
                self.stage += 1
                if (self.stage >= len(stages)):
                    self.stage = len(stages)
                print(self.stage)
                self.entities = stages[self.stage]
                self.player.pos.x = 0
                self.player.pos.y = 380
                self.player.ammo = 7
                self.player.ammo_capacity = 21


            if self.keyboard.left:
                if self.stage == 0 and self.player.pos.x <= 0:
                    self.background_x += 0
                else:
                    self.background_x += 0.02
                    self.player.run_left()
         
            if self.keyboard.right:
                self.background_x -= 0.02
                self.player.run_right()
                
            if self.keyboard.r:
                self.player.reload()
                
                
           
            
            if self.keyboard.space and self.player.on_ground:
                if self.keyboard.last_direction == 'a':
                    self.player.sprite.IMG_CENTRE = ((610/12)*5,(329/6))
                    self.player.velocity.add(Vector(-3, -15))
                if self.keyboard.last_direction == 'd':
                    self.player.sprite.IMG_CENTRE = ((610/12)*7,(329/6))
                    self.player.velocity.add(Vector(3, -15))
                self.player.on_ground = False
            if self.keyboard.any_input == False and self.keyboard.last_direction == 'd':
                self.player.sprite.IMG_CENTRE = ((610/12)*3,(329/6))
            if self.keyboard.any_input == False and self.keyboard.last_direction == 'a':
                self.player.sprite.IMG_CENTRE = ((610/12),(329/6))
            if self.player.on_ground == False:
                self.player.velocity.add(Vector(0, 0.75))
            
            
            for platform in self.platform_list:
                if self.player.pos.y >= platform.ground_level and self.player.pos.x >= platform.left and self.player.pos.x <= platform.right:
                    self.player.pos.y = platform.ground_level
                    self.player.on_ground = True
                    self.current_platform = platform
                   
            if self.player.pos.x > self.current_platform.right or self.player.pos.x < self.current_platform.left:
                self.player.on_ground = False
                 
          
                 
            
            
            #Below code checks if player is on floor, should change for platform

            if self.player.pos.y >= 480:
                player_hit.play()
                player_hit.rewind()
                player_hit.play()
                self.player_fell() 

            
            player.update()
            
            if mouseReturn != None:
                if self.shoot_timer <= 0:
                    player.shoot(mouseReturn)
                    self.shoot_timer = 25
            if self.shoot_timer > 0:
                self.shoot_timer -= 1

            for i in self.bullets:
                i.update()
                
            #enemies
            for x in self.entities:
                x.update()
                if(x.health>0):
                        player.hitByEnemy(x)
                if x.is_dead == True:
                    self.entities.remove(x)
                if (isinstance(x, Enemy)):
                    for b in self.bullets:
                        x.hitByBullet(b)
                if isinstance(x,BossZombie) == False:       
                    for platform in self.platform_list:
                        if x.pos.y >= platform.ground_level and x.pos.x >= platform.left and x.pos.x <= platform.right:
                            x.pos.y = platform.ground_level
                            x.rotate = True
                            x.current_platform = platform
                        if x.current_platform != '':
                            if x.pos.x > x.current_platform.right or x.pos.x < x.current_platform.left:
                                x.rotate = False


        
#Defining sprites
bulletSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/bullet_sprite.png"), (12.5, 12.5), (25, 25))
playerSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/mc_spritesheetV2.png"), ((610/12)*3, 329/6), (610/6, 329/3))

##USE FOR REFERENCE WHEN PROGRAMMING ONLY
#zombieSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zhac/315/zombie_sheet.png"), (51, 55*3), (100, 100))

gray_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/new_gray_rooftop.png"),(697 / 2, 697 / 2) ,(697, 697))
green_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/new_green_rooftop.png"),(754/2,754/2),(754,754))
red_rooftopSprite = Sprite(simplegui.load_image("http://personal.rhul.ac.uk/zjac/379/red_rooftop.png"),(800/2,800/2),(800,800))
 

#creating a list to store the platforms
platform_list = []
platform_list.append(Platform("gray",Vector(155,305)))
platform_list.append(Platform("green",Vector(550,305)))
platform_list.append(Platform("red",Vector(790,320)))



kbd = Keyboard()
clock = Clock()

player = Player(playerSprite, Vector(115, 380), 25, 10, 20, 5, 3)


EnemiesStageOne = [Zombie(Vector(800, 347)), Zombie(Vector(600, 300)),Zombie(Vector(320, 380)),  FlyingZombie(Vector(600,100))]
EnemiesStageTwo = [BossZombie(Vector(810, 400))]
VictoryScreen = []

stages = [EnemiesStageOne, EnemiesStageTwo, VictoryScreen]

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