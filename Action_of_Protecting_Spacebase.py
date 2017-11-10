# Game Programming
# Course ID #: 543
# Username: bluecarneal
# User ID #: 38516
# Challenge Set #: 4

#NOTE: Each individual file must be within the same folder.

#All images, sounds, and code created by bluecarneal, unless othewise noted.

#NOTE: mars.ogg is from 'The Planets', Holst's symphony.  This performance was not copyrighted.

#NOTE:  This game starts out reaaaaaallly easy.  Beat it a few times, and it will get harder.

#Falling aliens (the green ones) are supposed to die on impact.  This is intentional.

#imports
import pygame
from pygame.locals import *
from sys import exit
from random import *
from math import *

#game variables
def level():
    LEVEL = 3 #default
    file = open('history.txt','r')
    history = ''
    for line in file: #There should only be one line
        history = line
    wins = 0
    losses = 0
    winStreak = 0
    lossStreak = 0
    for game in history: #count wins and losses
        if game == '1':
            wins+=1
        if game == '0':
            losses +=1
    index = (len(history)-1)
    if history[index] == '1': 
        winStreak +=1
        if history[index-1] == '1':
            winStreak += 1
            if history[index-2] == '1':
                winStreak += 1
                if history[index-3] == '1':
                    winStreak += 1
                    if history[index-4] == '1':
                        winStreak += 1
    if history[index] == '0':
        lossStreak +=1
        if history[index-1] == '0':
            lossStreak += 1
            if history[index-2] == '0':
                lossStreak += 1
                if history[index-3] == '0':
                    lossStreak += 1
                    if history[index-4] == '0':
                        lossStreak += 1
    if winStreak == 5:  #Hopefully this balances the game a bit, although this is probably unbalanced itself.
        LEVEL = 5
    if winStreak == 4:
        LEVEL = 4
    if winStreak == 3:
        LEVEL = 4
    if winStreak == 2 and wins == 2: #only lost once past 5
        LEVEL = 4
    if winStreak == 2 and randint(0,1) == 1:
        LEVEL = 4
    if lossStreak == 5:
        LEVEL = 1
    if lossStreak == 3:
        LEVEL = 2
    if lossStreak == 2 and wins<=2:  #Lost two in a row and lost at least 3 out of last 5
        LEVEL = 2
    if losses == 4:
        LEVEL = 2
    return LEVEL
        
LEVEL = level()
AMMO1 = 150//LEVEL
AMMO2 = 150//LEVEL
PEOPLE = 250 + (LEVEL*50)
turret_delay_factor = LEVEL+1
robot1_delay_factor = LEVEL+1
robot2_delay_factor = LEVEL+1
    
SCORE1 = 0
SCORE2 = 0
CAPACITY = 50
MISSES = 0
HITS = 0

#from here starts a long list of classes.  Many of them are
#similar to things we've worked with before, so I won't go into to much
#detail.
class Button(pygame.sprite.Sprite):   #Credit to kprater3-14 for creating (part of) this class.
    def __init__(self, frames, x, y):
        """Creates a button that you can click and highlight"""
        pygame.sprite.Sprite.__init__(self)
        self.frameNames = frames
        self.frames=[]
        for image in self.frameNames:
            picture = pygame.image.load(image)
            picture = picture.convert()
            self.frames.append(picture)
        self.image = self.frames[0]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen, x, y):
        """Draws the button"""
        self.highlight(x, y)
        screen.blit(self.image,self.rect)
        
    def clicked(self,x,y):
        """Determines if the button was clicked"""
        return self.rect.collidepoint(x,y)

    def highlight(self, x, y):
        """Determines if the button should be highlighted"""
        if self.rect.collidepoint(x,y):
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]
    
class Scoreboard(pygame.Surface):
    def __init__(self, score, energy, turret, people, player):
        """Creates a scoreboard given certain values"""
        pygame.Surface.__init__(self, (256,115))
        self.font = pygame.font.Font(None, 15)
        self.score = score
        self.energy = energy
        self.turret = turret
        self.people = people
        self.player = player
        self.draw()
    def draw(self):
        """Draws the scoreboard"""
        self.fill(pygame.Color('black'))
        text1 = font.render('Player '+str(self.player), True, (255,255,255))
        text2 = font.render('Score: '+str(self.score), True, (255,255,255))
        text3 = font.render('Energy: '+str(self.energy)[0:5]+'%', True, (255,255,255))
        text4 = font.render('Ammo: '+str(self.turret), True, (255,255,255))
        text5 = font.render('Scientists: '+str(self.people), True, (255,255,255))
        self.blit(text1, (10,10))
        self.blit(text2, (10,30))
        self.blit(text3, (10, 50))
        self.blit(text4, (10,70))
        self.blit(text5, (10,90))
        
class Robot(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, dx, dy):
        """Creates a robot given frames and other values"""
        pygame.sprite.Sprite.__init__(self)
        self.dx = dx
        self.dy = dy
        self.starts = frames[0:2] #Divides the frames into the different types.
        self.walks = frames[2:5]
        self.jumps = frames[5]
        self.image = self.starts[0]
        left = x - self.image.get_width()/2
        top = y - self.image.get_height()/2
        self.rect = pygame.Rect(left, top,
                                self.image.get_width(),
                                self.image.get_height())
        self.animation = 0 #animation counter
        self.jump = False #are we jumping?
        self.switch = 1 #on/off switch for slowing the animation
        self.lastmove = 0 #right = 0, left is 1
        self.dy = -40 
        self.stills = 0 #animation counter for when still
        self.energy = 100

    def draw(self,screen):
        """Draws the robot"""
        screen.blit(self.image, self.rect)

    def update(self,key,screen):
        """Updates the robot"""
        if self.energy>0: #if we are still alive
            self.switch = self.switch * -1 #flip the switch (so the robot is animated at 15 fps)
            if key == K_UP: #Did we jump?
                self.jump = True
                self.energy -= 0.05
            if self.jump == False: #If we didn't jump
                if key == K_LEFT and self.rect.left - self.dx > 0: #Did we move left?
                    self.energy -= 0.075
                    self.lastmove = 1
                    self.rect = self.rect.move(self.dx*-1,0)
                    if self.switch == 1: #move the animation counter
                        self.animation = (self.animation+1)%3
                        self.image = pygame.transform.flip(self.walks[self.animation], 1, 0) #flip the image, if necessary.  This halves the number of image files necessary.
                if key == K_RIGHT and self.dx+self.rect.right < screen.get_width():
                    self.energy -= 0.075
                    self.lastmove = 0
                    self.rect = self.rect.move(self.dx*1,0)
                    if self.switch == 1:
                        self.animation = (self.animation+1)%3
                        self.image = self.walks[self.animation]
                if key == None:
                    self.stills = (self.stills+randint(0,1))%2
                    self.image = self.starts[self.stills]
            else: #We're jumping
                if self.dy > 0 and self.rect.bottom + self.dy>500: 
                    self.rect = self.rect.move(0,500-self.rect.bottom)
                    self.jump = False
                    self.dy = -40
                else:
                    if self.lastmove == 0:
                        if self.rect.right+self.dx//3<screen.get_width(): #don't go off screen
                            self.rect = self.rect.move(self.dx//3,self.dy)
                        else:
                            self.rect = self.rect.move(0,500-self.rect.bottom)
                            self.jump = False
                            self.dy = -40
                    else:
                        if self.rect.left+self.dx//3>0:
                            self.rect = self.rect.move(-self.dx//3,self.dy)
                        else:
                            self.rect = self.rect.move(0,500-self.rect.bottom)
                            self.jump = False
                            self.dy = -40
                    self.dy += 8
                    self.image = pygame.transform.flip(self.jumps, self.lastmove, 0)
            self.draw(screen)

    def getEnergy(self):
        """Returns energy"""
        return self.energy

    def energize(self):
        """Method for handling a energy power up"""
        self.energy  = (self.energy+20)
        if self.energy>100:
            self.energy=100
    def lastMove(self):
        """Return last direction moved"""
        if self.lastmove == 0:
            return 1
        else:
            return -1
        
    def laserShot(self):
        """Subtract energy for a laser shot"""
        self.energy -= 0.3

    def loseEnergy(self, amount):
        """Method to subtract a give amount of energy"""
        self.energy -= amount

    def restart(self):
        self.energy = 100
        
class Robot2(Robot): #Same as Robot, but the controls are different.
    def __init__(self, frames, x, y, dx, dy):
        Robot.__init__(self, frames, x, y, dx, dy)

    def update(self, key, screen):
        if self.energy>0:
            self.switch = self.switch * -1
            if key == K_w:
                self.jump = True
                self.energy -= 0.1
            if self.jump == False:
                if key == K_a and self.rect.left - self.dx > 0:
                    self.energy -= 0.075
                    self.lastmove = 1
                    self.rect = self.rect.move(self.dx*-1,0)
                    if self.switch == 1:
                        self.animation = (self.animation+1)%3
                        self.image = pygame.transform.flip(self.walks[self.animation], 1, 0)
                if key == K_d and self.dx+self.rect.right < screen.get_width():
                    self.energy -= 0.075
                    self.lastmove = 0
                    self.rect = self.rect.move(self.dx*1,0)
                    if self.switch == 1:
                        self.animation = (self.animation+1)%3
                        self.image = self.walks[self.animation]
                if key == None:
                    self.stills = (self.stills+randint(0,1))%2
                    self.image = self.starts[self.stills]
            else:
                if self.dy > 0 and self.rect.bottom + self.dy>500:
                    self.rect = self.rect.move(0,500-self.rect.bottom)
                    self.jump = False
                    self.dy = -40
                else:
                    if self.lastmove == 0:
                        if self.rect.right+self.dx//3<screen.get_width(): #don't go off screen
                            self.rect = self.rect.move(self.dx//3,self.dy)
                        else:
                            self.rect = self.rect.move(0,500-self.rect.bottom)
                            self.jump = False
                            self.dy = -40
                    else:
                        if self.rect.left+self.dx//3>0:
                            self.rect = self.rect.move(-self.dx//3,self.dy)
                        else:
                            self.rect = self.rect.move(0,500-self.rect.bottom)
                            self.jump = False
                            self.dy = -40
                    self.dy += 8
                    self.image = pygame.transform.flip(self.jumps, self.lastmove, 0)
            self.draw(screen)


#The rest of the classes are lasers, powerups, and enemies.  These are moving sprites with some animation.        
class Laser(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.image = self.frames[0]
        self.dx = dx
        self.dy = dy
        left = x - self.image.get_width()/2
        top = y - self.image.get_height()/2
        self.rect = pygame.Rect(left, top,
                                self.image.get_width(),
                                self.image.get_height())
        self.animation = 0
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def update(self, timePassed, screen):
        self.animation = (self.animation+1)%(len(self.frames))
        self.image = self.frames[self.animation]
        self.rect = self.rect.move(self.dx*timePassed, self.dy*timePassed)
        self.draw(screen)
        
class Alien1(Laser):
    def __init__(self, frames, x, y, dx, dy):
        Laser.__init__(self, frames, x, y, dx, dy)
        self.switch = 0
        self.type = 1
        self.life = randint(1,2)
    def update(self, timePassed, screen):
        self.switch += 1
        if self.switch%15 == 0:
            self.switch = 0
            self.animation = (self.animation+1)%(len(self.frames))
        if self.rect.left-10<0 or self.rect.right+10> screen.get_width():
            self.dx = self.dx * -1
        self.image = self.frames[self.animation]
        self.rect = self.rect.move(self.dx*timePassed, self.dy*timePassed)
        self.draw(screen)

class Alien2(Alien1):
    def __init__(self, frames, x, y, dx, dy):
        Alien1.__init__(self, frames, x, y, dx, dy)
        self.type = 2
        self.life = 2
class Alien3(Alien1):
     def __init__(self, frames, x, y, dx, dy):
        Alien1.__init__(self, frames, x, y, dx, dy)
        self.type = 3
        self.life = 4
class AmmoUp(pygame.sprite.Sprite):
    def __init__(self, x, y, dy, amount):
        pygame.sprite.Sprite.__init__(self)
        self.dy = dy
        self.amount = amount
        self.animation = 0
        self.font = pygame.font.Font(None, 30)
        self.image = self.makeImage()
        left = x - self.image.get_width()/2
        top = y - self.image.get_height()/2
        self.rect = pygame.Rect(left, top,
                                self.image.get_width(),
                                self.image.get_height())
        if randint(0,5)==0:
            self.amount = 'UP'
            
    def makeImage(self):
        self.animation = (self.animation+1)%3
        image = pygame.Surface((32,32))
        image.fill(pygame.Color('white')) 
        image.set_colorkey(pygame.Color('white'))
        if self.animation == 0:
            text = font.render(str(self.amount), True, pygame.Color('red'))
        elif self.animation == 1:
            text = font.render(str(self.amount), True, pygame.Color('orange'))
        elif self.animation == 2:
            text = font.render(str(self.amount), True, pygame.Color('yellow'))
        image.blit(text, (1,1))
        return image
        
    def draw(self, screen):
        self.image = self.makeImage()
        screen.blit(self.image, self.rect)
                    
    def update(self, timePassed, screen):
        self.rect = self.rect.move(0, timePassed*self.dy)
        self.draw(screen)

    def getType(self):
        if self.amount == 'UP':
            return 'speed'
        else:
            return 'ammo'
    
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.dx = dx
        self.dy = dy
        self.image = pygame.image.load('rocket.png')
        self.image = self.image.convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        left = x - self.image.get_width()/2
        top = y - self.image.get_height()/2
        self.rect = pygame.Rect(left, top,
                                self.image.get_width(),
                                self.image.get_height())
        self.counter = 0
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self, timePassed, screen):
        self.counter += 1
        if self.counter>300:
            self.dy-=10
            self.rect = self.rect.move(self.dx*timePassed, self.dy*timePassed)
        self.draw(screen)
        
class EnergyUp(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.dx = dx
        self.dy = dy
        self.frameNames = ['logo.png','logo2.png']
        self.frames = []
        for frame in self.frameNames:
            image = pygame.image.load(frame)
            image = image.convert()
            image.set_colorkey(image.get_at((0,0)))
            self.frames.append(image)
        self.image = self.frames[0]
        left = x - self.image.get_width()/2
        top = y - self.image.get_height()/2
        self.rect = pygame.Rect(left, top,
                                self.image.get_width(),
                                self.image.get_height())
        self.animation = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, timePassed, screen):
        if randint(0,1)==0:
            self.animation = (self.animation+1)%2
        self.image = self.frames[self.animation]
        self.rect = self.rect.move(self.dx*timePassed, self.dy*timePassed)
        self.draw(screen)

    def getType(self):
        return 'energy'


#Sets up the pygame window with title, logo, cursor.        
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
logo = pygame.image.load('logo.png') 
logo.set_colorkey(logo.get_at((0,0)))
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((952, 631)) 
pygame.display.set_caption('Action of Protecting Spacebase') # title of window
cursor_strings = ( #I designed it on a piece of graph paper.  Pixelating a circle is tricky.  
                  "           X            ",
                  "           X            ",
                  "          XXX           ",
                  "       XXX X XXX        ",
                  "      X    X    X       ",
                  "     X     X     X      ",
                  "    X      X      X     ",
                  "   X       X       X    ",
                  "   X       X       X    ",
                  "   X       X       X    ",
                  "  X        X        X   ",
                  "XXXXXXXXXXXXXXXXXXXXXXX ",
                  "  X        X        X   ",
                  "   X       X       X    ",
                  "   X       X       X    ",
                  "   X       X       X    ",
                  "    X      X      X     ",
                  "     X     X     X      ",
                  "      X    X    X       ",
                  "       XXX X XXX        ",
                  "          XXX           ",
                  "           X            ",
                  "           X            ",
                  "                        ")
cursor_data, cursor_mask = pygame.cursors.compile(cursor_strings, black='X', white='.', xor='o')
pygame.mouse.set_cursor((24,24), (11,11), cursor_data, cursor_mask)


#There's a bunch of image preparation going on for the next 50 lines.
backgroundNames = ['menubackground1.png','menubackground2.png','instructionsbackground.png','background.png']
backgroundFrames = []
for frame in backgroundNames:
    picture = pygame.image.load(frame)
    picture = picture.convert()
    picture.set_colorkey(picture.get_at((0,0)))
    backgroundFrames.append(picture)


robotFrameNames = ['bot1-S1.png', 'bot1-S2.png', 'bot1-1.png', 'bot1-2.png', 'bot1-3.png', 'bot1-J.png','bot2-S1.png', 'bot2-S2.png', 'bot2-1.png', 'bot2-2.png', 'bot2-3.png', 'bot2-J.png']
robot1Frames = []
robot2Frames = []
for frame in robotFrameNames:
    picture = pygame.image.load(frame)
    picture = picture.convert()
    picture.set_colorkey(picture.get_at((0,0)))
    if frame[3]=='1':
        robot1Frames.append(picture)
    else:
        robot2Frames.append(picture)


laserFrames = []
laserFrameNames = ['laser1.png', 'laser2.png', 'laser3.png']
for frame in laserFrameNames:
    picture = pygame.image.load(frame)
    picture = picture.convert()
    laserFrames.append(picture)


alien1Frames = []
alien2Frames = []
alien3Frames = []
alienFrameNames = ['alien1-1.png', 'alien1-2.png', 'alien2-1.png', 'alien2-2.png', 'alien3-1.png', 'alien3-2.png']
for frame in alienFrameNames:
    picture = pygame.image.load(frame)
    picture = picture.convert()
    picture.set_colorkey(picture.get_at((picture.get_width()-1, picture.get_height()-1)))
    if frame[5] == '1':
        alien1Frames.append(picture)
    elif frame[5] == '2':
        alien2Frames.append(picture)
    elif frame[5] == '3':
        alien3Frames.append(picture)

print("Loading...") #tells the user that the game is loading, because it takes about 10 seconds (mainly because mars.ogg is large)

#load the two sounds
mars = pygame.mixer.Sound('mars.ogg')
laser_sound = pygame.mixer.Sound('laser.ogg')

#start the clock
clock = pygame.time.Clock()

#create the keys
key = None
key1 = None
key2 = None
key3 = None

#create sprite groups for ease of updating
lasers = pygame.sprite.Group()
aliens = pygame.sprite.Group()
powerUps = pygame.sprite.Group()
rockets = pygame.sprite.Group()
turretlasers = pygame.sprite.Group()
robot1lasers = pygame.sprite.Group()
robot2lasers = pygame.sprite.Group()
allLasers = pygame.sprite.Group()


stage = 'mainmenu' #initial stage
menuanimation = 0
background = backgroundFrames[menuanimation] #main background is animated
cx, cy = 0, 0 #clicked coordinates
testbot1 = False #have we already initialized the robots?
testbot2 = False
font = pygame.font.Font(None, 25) #the font
counter = 0 #keeps track of where we are in the game.  I use it to time enemy waves and such.

turret_delay = 0 #delay counters
robot1_delay = 0
robot2_delay = 0

marsOn = False #background music on?
gameStarted = False #gamestarted?
processed = False #did we process the results?
turret1 = True #for two players, does Player 1 control turret?


def genForm(kind): #This creates waves of aliens.  Very easy to create new waves.
    if kind == 'diamond':
        coordinateList = [(300,0), (500,0), (700,0), (500,100), (500,-100)]
        speedList = [(0, 125), (0, 125), (0, 125), (0,125), (0,125)]
        typeList = [2,3,2,2,2]
    if kind == 'wall':
        coordinateList = [(25, 0), (150, 0), (275, 0), (400, 0), (525, 0), (650, 0), (775, 0), (900, 0)]
        speedList = [(0,125),(0,150),(0,125),(0,150),(0,125),(0,150),(0,125),(0,150)]
        typeList = [2,3,2,3,2,3,2,3]
    if kind == 'random':
        coordinateList=[]
        speedList=[]
        typeList=[]
        for i in range(0,randint(2,5)):
            coordinateList.append((randint(60,screen.get_width()-60),0)) #yes, it gives a safe spot, but it eliminates errors if an enemy was half off half on screen.
            speedList.append((0, randint(100,175)))
            typeList.append((randint(1,3)))
    if kind == 'speed':
        coordinateList = [(500,0), (600,-25), (400,-25), (700, -50), (300, -50), (500, -50)]
        speedList = [(0,200),(0,200),(0,200),(0,200),(0,200),(0,200)]
        typeList = [3,2,2,2,2,3]
            
    for i in range(len(typeList)):
        if typeList[i]==1:
            alien = Alien1(alien1Frames,
                           x = coordinateList[i][0],
                           y = coordinateList[i][1],
                           dx = speedList[i][0],
                           dy = speedList[i][1])
        elif typeList[i]==2:
            alien = Alien2(alien2Frames,
                           x = coordinateList[i][0],
                           y = coordinateList[i][1],
                           dx = speedList[i][0],
                           dy = speedList[i][1])
        elif typeList[i]==3:
            alien = Alien3(alien3Frames,
                           x = coordinateList[i][0],
                           y = coordinateList[i][1],
                           dx = speedList[i][0],
                           dy = speedList[i][1])
        aliens.add(alien)

def processData(win,loss,point,hit,miss): #This processes the data at the end of a 1 player game using two text files.
    file = open('data.txt','r')
    for line in file:
        line.strip()
        line = line.split(',')
        wins = int(line[0])+win
        losses = int(line[1])+loss
        points = int(line[2])+point
        hits = int(line[3])+hit
        misses = int(line[4])+miss
    file.close()
    file = open('data.txt', 'w')
    file.write(str(wins)+','+str(losses)+','+str(points)+','+str(hits)+','+str(misses))
    file.close()
    file = open('scores.txt','a')
    file.write(str(point)+'\n')
    file.close()
    file = open('scores.txt','r')
    scores = []
    for line in file:
        line = line.strip()
        scores.append(int(line))
    scores.sort()
    scores = scores[::-1]
    place = scores.index(int(point))+1
    file.close()
    file = open('history.txt','r')
    history = ''
    for line in file: #there should only be one line
        line.strip()
        history = line
    file.close()
    if win == 1:
        history +='1'
    elif loss == 1:
        history+='0'
    history = history[1:6] #remove the first record (we only want 5 at a time)
    file = open('history.txt', 'w')
    file.write(history)
    file.close()
    report = wins, losses, points, hits, misses, place, scores 
    return report

while True: #time to start the main loop!
    
    timePassed = clock.tick(30) #advance the clock
    timePassed = timePassed / 1000.0
    screen.fill(pygame.Color('black')) #fill the background
    counter +=1 #advance the counter
    
    for event in pygame.event.get(): #gather the necessary events
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN: # remember pressed key
            if event.key == K_UP or event.key == K_RIGHT or event.key == K_LEFT:
                key1 = event.key
            if event.key == K_w or event.key == K_a or event.key == K_d:
                key2 = event.key
            if event.key == K_r:
                key3 = event.key
            key = event.key
        elif event.type == KEYUP: # clear pressed key
            if event.key == K_UP or event.key == K_RIGHT or event.key == K_LEFT:
                key1 = None
            if event.key == K_w or event.key == K_a or event.key == K_d:
                 key2 = None
            if event.key == K_r:
                key3 = None
            key = None
        elif event.type == MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos() #clicked coordinates
        elif event.type == MOUSEBUTTONUP:
            cx, cy = 0, 0
            
    hx, hy = pygame.mouse.get_pos() #mouse hovering coordinates
    if not marsOn: #start up the background music
        mars.play(fade_ms=1000)
        mars.play(-1)
        marsOn = True
        
    if stage == 'mainmenu': #We start at the main menu
        if randint(0,1)==0: #animate
            menuanimation = (menuanimation+1)%2
            background = backgroundFrames[menuanimation]
        screen.blit(background, (0,0))
        #Adding buttons...
        button1 = Button(['onePlayerButton1.png','onePlayerButton2.png'],
                         x = 412,
                         y = 250)
        button2 = Button(['twoPlayerButton1.png', 'twoPlayerButton2.png'],
                         x = 412,
                         y = 324)
        button3 = Button(['instructionsButton1.png','instructionsButton2.png'],
                         x = 809,
                         y = 553)
        button1.draw(screen, hx, hy)
        button2.draw(screen, hx, hy)
        button3.draw(screen, hx, hy)
        if testbot1 == False: #If we haven't started a robot, make one.
            robot1 = Robot(robot1Frames,
                  x = screen.get_width()//2,
                  y = 500-(robot2Frames[0].get_height()//2),
                  dx = 10,
                  dy = 0)
            testbot1 = True
        robot1.update(key1,screen) #update the robot.
        if button1.clicked(cx, cy): #Things that happen when we click buttons.
            stage = 'oneplayerstart'
        if button2.clicked(cx, cy):
            stage = 'twoplayerstart'
        if button3.clicked(cx, cy):
            stage = 'maininstructions'
            
    if stage == 'maininstructions': #Display the instructions page
        background = backgroundFrames[2]
        screen.blit(background,(0,0))
        button1 = Button(['backButton1.png','backbutton2.png'],
                         x = 15,
                         y = 553)
        button1.draw(screen, hx, hy)
        if button1.clicked(cx, cy):
            stage = 'mainmenu'
        #robot1.update(key1, screen)  #Removes the issue of robot blocking the text.
        
    if stage == 'twoplayerstart': #Display start button for two player game
        robot1.update(key1, screen)
        if testbot2 == False: #adds the second robot
            robot2 = Robot2(robot2Frames,
                  x = screen.get_width()//2+32,
                  y = 500-(robot1Frames[0].get_height()//2),
                  dx = 10,
                  dy = 0)
            testbot2 = True
        robot2.update(key2, screen)
        button1 = Button(['backButton1.png','backbutton2.png'],
                         x = 15,
                         y = 553)
        button1.draw(screen, hx, hy)
        button2 = Button(['startButton1.png','startButton2.png'],
                         x = 412,
                         y = 250)
        button2.draw(screen, hx, hy)
        if button2.clicked(cx, cy):
              stage = 'twoplayergame'
        if button1.clicked(cx, cy):
            stage = 'mainmenu'
            
    if stage == 'oneplayerstart': #start page for one player game
          levelData = font.render("Based on recent play history, the difficulty has been set to level "+str(LEVEL), True, (255,255,255))
          button1 = Button(['startButton1.png','startButton2.png'],
                         x = 412,
                         y = 324)
          button1.draw(screen, hx, hy)
          button2 = Button(['backButton1.png','backbutton2.png'],
                         x = 15,
                         y = 553)
          button2.draw(screen, hx, hy)
          if button1.clicked(cx, cy):
              stage = 'oneplayergame'
          if button2.clicked(cx, cy):
              stage = 'mainmenu'
          robot1.update(key1, screen)
          screen.blit(levelData, (250,250))
    if stage == 'oneplayergame' or stage == 'twoplayergame': #initially, this code was for a one player game, but
        #the two player code sort of rides piggy back on the one player code.
        if not gameStarted:
            robot1.restart() #replace the energy used on the menus.
            if stage == 'twoplayergame':
                robot2.restart()
        if stage == 'twoplayergame':
            LEVEL = 3 #default part of the level so there's no unfair advantage.  
        gameStarted = True #The game started
        background = backgroundFrames[3] #use the game background
        screen.blit(background, (0,0))
        
        if stage == 'twoplayergame': #Displays and changes who controls the turret for a 2 player game
            if turret1: 
                text = font.render('Player 1 controls turret', True, (255,255,255))
                screen.blit(text, (250,250))
            else:
                text = font.render('Player 2 controls turret', True, (255,255,255))
                screen.blit(text, (250,250))
                
        if counter%900==0 and stage == 'twoplayergame' and turret1:
            text = font.render('Player 2 controls turret', True, (255,255,255))
            screen.blit(text, (250,250))
            turret1 = False
            
        if counter%1801==0 and stage == 'twoplayergame' and not turret1:
            text = font.render('Player 1 controls turret', True, (255,255,255))
            screen.blit(text, (250,250))
            turret1 = True
            
        if counter%(500-(LEVEL*50))==0 or counter == 120: #don't keep the player waiting too long
            waveType = randint(1,8)
            if waveType == 1 or waveType == 2 or waveType == 3:
                genForm('random')
            if waveType == 4 or waveType == 5:
                genForm('diamond')
            if waveType == 6:
                genForm('wall')
            if waveType == 7 or waveType == 8:
                genForm('speed')
                
        if counter%(LEVEL*50+100) == 0: 
            upType = randint(0,5)
            if upType == 0 or upType == 1 or upType == 2 or upType == 3 or upType == 4:
                powerUp = AmmoUp(x = randint(10,screen.get_width()-10),
                                 y = 0,
                                 dy = 100,
                                 amount = randint(5,15))
            else:
                powerUp = EnergyUp(x = randint(10,screen.get_width()-10),
                                 y = 0,
                                 dx = 0,
                                 dy = 100)
            powerUps.add(powerUp)
            
        if counter%(3*LEVEL*75) == 0: #a mere minute or so on LEVEL 1 (should be really easy to win), compared to over 6 minutes on level 5.  
            rocket = Rocket(x = 541,
                            y = 472,
                            dx = 0,
                            dy = 75)
            rockets.add(rocket)
            
##########################################################################
        #all this stuff deals with firing lasers.  There's a bit of trig, and two player options make it a bit messy.  It works.

            
        if (cx, cy) != (0, 0): #551, 457
            speed = 500 #pixels/frame
            xdist = cx - 551  #positive to left
            ydist = cy - 457 #positive to below
            turret_delay = (turret_delay+1)%turret_delay_factor #advance delay counter
            shoot = False
            if ydist < 0 and turret_delay%turret_delay_factor == 0: #if we can shoot
                if stage == 'twoplayergame':
                    if turret1:
                        if AMMO1 > 0:
                            laser_sound.play()
                            AMMO1 -= 1
                            shoot = True
                    else:
                        if AMMO2>0:
                            laser_sound.play()
                            AMMO2-=1
                            shoot = True
                else:
                    if AMMO1>0:
                        laser_sound.play()
                        AMMO1-=1
                        shoot = True
                if shoot: #doing the math do get the right vectors
                    hyp = sqrt(xdist**2+ydist**2)
                    angle = atan2(ydist,xdist)
                    xspeed = speed*cos(angle)
                    yspeed = speed*sin(angle)
                    laser = Laser(laserFrames,
                                  x = 551,
                                  y = 457,
                                  dx = xspeed,
                                  dy = yspeed)
                    turretlasers.add(laser)
                    allLasers.add(laser) #add to the laser groups
        if key == K_SPACE and robot1.getEnergy()>0: #did the robot shoot?
            robot1_delay = (robot1_delay+1)%robot1_delay_factor #can he shoot?
            if robot1_delay%robot1_delay_factor == 0: 
                laser = Laser(laserFrames,
                                  x = robot1.rect.left+16,
                                  y = robot1.rect.top+32,
                                  dx = 375*robot1.lastMove(),
                                  dy = 0)
                robot1.laserShot()
                robot1lasers.add(laser)
                allLasers.add(laser)
        if stage == 'twoplayergame':
            if key3 == K_r and robot2.getEnergy()>0:
                robot2_delay = (robot2_delay+1)%robot2_delay_factor
                if robot2_delay%robot2_delay_factor == 0:
                    laser = Laser(laserFrames,
                                  x = robot2.rect.left+16,
                                  y = robot2.rect.top+32,
                                  dx = 375*robot2.lastMove(),
                                  dy = 0)
                    robot2.laserShot()
                    robot2lasers.add(laser)
                    allLasers.add(laser)
###########################################################################            
        for laser in allLasers: #if a laser is offscreen, get rid of it.  
            laser.update(timePassed,screen) #update all of them.
            if laser.rect.top<0 or laser.rect.left<0 or laser.rect.right>screen.get_width():
                laser.kill()
                MISSES+=1 #you missed!
        
        for rocket in rockets: #updating rockets.
            rocket.update(timePassed,screen)
            if rocket.rect.top<0: #If a rocket departs
                rocket.kill()
                SCORE1+=1500
                if stage == 'twoplayergame':
                    SCORE2+=1500
                PEOPLE -= CAPACITY
                
        for powerUp in powerUps: #this loop goes through the powerups, kills them if necessary, and handles the effects.
            powerUp.update(timePassed,screen)
            if powerUp.rect.bottom > 500:
                powerUp.kill()
            if pygame.sprite.collide_rect(powerUp, robot1):
                if powerUp.getType() == 'energy':
                    robot1.energize() #replenish energy
                    SCORE1+=200
                elif powerUp.getType() == 'ammo':
                    AMMO1+=powerUp.amount #add to ammo
                    SCORE1+=powerUp.amount*10
                elif powerUp.getType() == 'speed' and turret_delay_factor>0:
                    turret_delay_factor -=1 #make the guns shoot faster
                    SCORE1+=150
                powerUp.kill()
            if stage == 'twoplayergame':
                if pygame.sprite.collide_rect(powerUp, robot2):
                    if powerUp.getType() == 'energy':
                        robot2.energize()
                        SCORE2+=200
                    elif powerUp.getType() == 'ammo':
                        AMMO2+=powerUp.amount
                        SCORE2+=powerUp.amount*10
                    elif powerUp.getType() == 'speed' and turret_delay_factor>0:
                        turret_delay_factor -=1
                        SCORE2+=150
                    powerUp.kill()

                    
        for alien in aliens: #updates the aliens
            alien.update(timePassed, screen)
            if alien.rect.bottom>500 or alien.rect.left<0 or alien.rect.right>screen.get_width():
                if alien.type != 1: #if an alien craft lands, create an alien
                    newAlien = Alien1(alien1Frames,
                                      x = alien.rect.left,
                                      y = alien.rect.top,
                                      dx = choice([randint(-150,-75),randint(75,150)]),
                                      dy = 0)
                    aliens.add(newAlien)
                                      
                alien.kill()
                    
            if pygame.sprite.collide_rect(alien, robot1): #handle collision
                robot1.loseEnergy(15)
                alien.kill()
            if stage == 'twoplayergame':
                if pygame.sprite.collide_rect(alien, robot2):
                    robot2.loseEnergy(15)
                    alien.kill()
                    
            for laser in robot1lasers: 
                for alien in aliens:
                    if pygame.sprite.collide_rect(alien, laser): #did we shoot the alien with the robot?
                        laser.kill()
                        HITS+=1 
                        alien.life -= 1
                        if alien.life == 0:
                            alien.kill()
                            if alien.type == 1:
                                SCORE1+=125
                            if alien.type == 2:
                                SCORE1+=250
                            if alien.type == 3:
                                SCORE1+=400
                                
            if stage == 'twoplayergame':
                for laser in robot2lasers:
                    for alien in aliens:
                        if pygame.sprite.collide_rect(alien, laser):
                            laser.kill()
                            HITS+=1
                            alien.life -= 1
                            if alien.life == 0:
                                alien.kill()
                                if alien.type == 1:
                                    SCORE2+=125
                                if alien.type == 2:
                                    SCORE2+=250
                                if alien.type == 3:
                                    SCORE2+=400
            for alien in aliens:
                if stage == 'twoplayergame':
                    for laser in turretlasers:
                        if pygame.sprite.collide_rect(alien, laser): #did we shoot the alien with the turret?
                            laser.kill()
                            alien.life -= 1
                            if alien.life == 0 and turret1:
                                alien.kill()
                                if alien.type == 1:
                                    SCORE1+=125
                                if alien.type == 2:
                                    SCORE1+=250
                                if alien.type == 3:
                                    SCORE1+=400
                            if alien.life == 0 and not turret1:
                                alien.kill()
                                if alien.type == 1:
                                    SCORE2+=125
                                if alien.type == 2:
                                    SCORE2+=250
                                if alien.type == 3:
                                    SCORE2+=400
                else:
                    for laser in turretlasers:
                        if pygame.sprite.collide_rect(alien, laser):
                            laser.kill()
                            alien.life -= 1
                            if alien.life == 0:
                                alien.kill()
                                if alien.type == 1:
                                    SCORE1+=125
                                if alien.type == 2:
                                    SCORE1+=250
                                if alien.type == 3:
                                    SCORE1+=400

        scoreboard = Scoreboard(SCORE1, robot1.getEnergy(), AMMO1, PEOPLE, 1) #creates the scoreboard
         
        robot1.update(key1,screen) #updates the robot
        if stage == 'twoplayergame': #does the same for if there's a two player game
            robot2.update(key2,screen)
            scoreboard2 = Scoreboard(SCORE2, robot2.getEnergy(), AMMO2, PEOPLE, 2)
            screen.blit(scoreboard2, ((screen.get_width()//2-256), 510))
            
        screen.blit(scoreboard, ((screen.get_width()//2-64), 510)) #blit the scoreboard
        
        if PEOPLE<=0 or robot1.getEnergy()<=0: #gameover?
            if stage == 'oneplayergame':
                stage = 'oneplayerend'
                mars.stop()
        if stage == 'twoplayergame':
            if robot1.getEnergy() <= 0 or robot2.getEnergy()<=0 or PEOPLE<=0: #gameover?
                stage = 'twoplayerend'
                mars.stop()
                
    if stage == 'oneplayerend':
        if not processed: #process the results using the text files.
            if PEOPLE<=0: #we won!
                info = processData(1,0,SCORE1,HITS,MISSES)
            else: #we lost.
               info = processData(0,1,SCORE1,HITS,MISSES)
            processed = True
        if PEOPLE <=0: #display results and high scores.
            length = min(10,len(info[6]))
            text = font.render("Congratulations, you won!  You are # "+str(info[5])+" on the leaderboard.  Here's the top "+str(length)+":", True, (255,255,255))
            hlighted = False
            for i in range(0, length):
                if int(info[6][i]) == SCORE1 and not hlighted:
                    hlighted = True
                    text2 = font.render(str(info[6][i]), True, (0,255,0))
                else:
                    text2 = font.render(str(info[6][i]), True, (255,255,255))
                screen.blit(text2, (300,(275+i*30)))
        if PEOPLE>0: #display loss message.
            text = font.render("Too bad, you lost.  Try again!", True, (255,255,255))
        screen.blit(text, (250,250))
        button1 = Button(['statsButton1.png', 'statsButton2.png'], #stats button
                          x = 809,
                          y = 553)
        button1.draw(screen, hx, hy)
        button2 =  Button(['replayButton1.png','replayButton2.png'],
                          x = 809,
                          y = 479)
        button2.draw(screen, hx, hy)
        if button1.clicked(cx, cy):
            stage = 'oneplayerstats'
        if button2.clicked(cx, cy):
            LEVEL = level()
            AMMO1 = 150//LEVEL
            AMMO2 = 150//LEVEL
            PEOPLE = 250 + (LEVEL*50)
            turret_delay_factor = LEVEL+1
            robot1_delay_factor = LEVEL+1
            robot2_delay_factor = LEVEL+1
            SCORE1 = 0
            SCORE2 = 0
            CAPACITY = 50
            MISSES = 0
            HITS = 0
            mars.play(-1)
            marsOn = True
            robot1.restart()
            gameStarted = False #gamestarted?
            processed = False #did we process the results?
            turret1 = True #for two players, does Player 1 control turret?
            stage = 'oneplayerstart'
            for alien in aliens:
                alien.kill()
            for laser in allLasers:
                laser.kill()
            for powerUp in powerUps:
                powerUp.kill()
            counter = 0
    if stage == 'oneplayerstats': #page for all time statistics.
        wins = info[0]
        losses = info[1]
        points = info[2]
        hits = info[3]
        misses = info[4]
        text1 = font.render("You've won "+str(wins)+" games out of "+str(wins+losses)+".", True, (255,255,255))
        text2 = font.render("You've fired "+str(hits+misses)+" shots, and you've made "+str((hits/(misses+hits))*100)[0:4]+"% of them.", True, (255,255,255))
        text3 = font.render("You've earned "+str(points)+" total points.", True, (255,255,255))
        screen.blit(text1, (250,250))
        screen.blit(text2, (300,300))
        screen.blit(text3, (350, 350))
        button1 = Button(['backButton1.png', 'backButton2.png'],
                          x = 15,
                          y = 553)
        button1.draw(screen, hx, hy)
        if button1.clicked(cx, cy):
            stage = 'oneplayerend'
            
    if stage == 'twoplayerend': #displays results for a two player game
        if robot2.getEnergy()>robot1.getEnergy() and PEOPLE>0:
            text = font.render('Player 2 survived longer and won!', True, (255,255,255))
        elif robot1.getEnergy()>robot2.getEnergy() and PEOPLE>0:
            text = font.render('Player 1 survived longer and won!', True, (255,255,255))
        elif PEOPLE<=0:
            if SCORE1>SCORE2:
                text = font.render('You both finished, but Player 1 had more points and won!', True, (255,255,255))
            if SCORE1 == SCORE2:
                text = font.render('You both finished, and it was a tie!', True, (255,255,255))
            else:
                text = font.render('You both finished, but Player 2 had more points and won!', True, (255,255,255))
        button2 =  Button(['replayButton1.png','replayButton2.png'],
                          x = 809,
                          y = 553)
        button2.draw(screen, hx, hy)
        if button2.clicked(cx, cy):
            LEVEL = level()
            AMMO1 = 150//LEVEL
            AMMO2 = 150//LEVEL
            PEOPLE = 250 + (LEVEL*50)
            turret_delay_factor = LEVEL+1
            robot1_delay_factor = LEVEL+1
            robot2_delay_factor = LEVEL+1
            SCORE1 = 0
            SCORE2 = 0
            CAPACITY = 50
            MISSES = 0
            HITS = 0
            mars.play(-1)
            marsOn = True
            robot1.restart()
            robot2.restart()
            gameStarted = False #gamestarted?
            processed = False #did we process the results?
            turret1 = True #for two players, does Player 1 control turret?
            stage = 'twoplayerstart'
            for alien in aliens:
                alien.kill()
            for laser in allLasers:
                laser.kill()
            for powerUp in powerUps:
                powerUp.kill()
            counter = 0        
        scoretext = font.render('Player 1: '+str(SCORE1)+'      Player 2: '+str(SCORE2), True, (255,255,255))
        screen.blit(text, (250,250))
        screen.blit(scoretext, (300,300))
        
    pygame.display.update() #updates display.

