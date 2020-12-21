import pygame,random,math

# General Settings
PLAYER_COLORS = [(37,7,255),(35,183,253),(48,254,241),(19,79,251),(255,7,230),(255,7,23),(6,254,13)]
CELL_COLORS = [(80,252,54),(36,244,255),(243,31,46),(4,39,243),(254,6,178),(255,211,7),(216,6,254),(145,255,7),(7,255,182),(255,6,86),(147,7,255)]
VIRUS_COLORS = [(66,254,71)]
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (2000,2000)
CELLS = list()

# Initializing pygame modules
pygame.init()
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
 # Transparent rect for score
SCOREBOARD_SURFACE = pygame.Surface((95,25),pygame.SRCALPHA)
# Transparent rect for leaderboard
LEADERBOARD_SURFACE = pygame.Surface((155,278),pygame.SRCALPHA) 
SCOREBOARD_SURFACE.fill((50,50,50,80))
LEADERBOARD_SURFACE.fill((50,50,50,80))
pygame.display.set_caption("Agar.io")
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

# Blits text to central (global) screen
def drawText(message,pos,color=(255,255,255)):
        MAIN_SURFACE.blit(font.render(message,1,color),pos)

# Calculates Euclidean distance
def getDistance(pos1,pos2):
    px,py = pos1
    p2x,p2y = pos2
    diffX = math.fabs(px-p2x)
    diffY = math.fabs(py-p2y)
    return ((diffX**2)+(diffY**2))**(0.5)


class Camera:
    """Camera is used to represent the concept of POV."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    # Makes sure that the given object will be at the center of player's view. Zooms out/ in as well
    def centre(self,blobOrPos):
        if(isinstance(blobOrPos,Player)):
            p = blobOrPos
            self.x = (p.startX-(p.x*self.zoom))-p.startX+((SCREEN_WIDTH/2))
            self.y = (p.startY-(p.y*self.zoom))-p.startY+((SCREEN_HEIGHT/2))
        elif(type(blobOrPos) == tuple):
            self.x,self.y = blobOrPos


class Player:
    """Player is used to represent the concept of the player."""
    def __init__(self,surface,name = ""):
        self.startX = self.x = random.randint(100,400)
        self.startY = self.y = random.randint(100,400)
        self.mass = 20
        self.speed = 4
        self.surface = surface

        # Initialize player with a random color
        self.color = PLAYER_COLORS[random.randint(0,len(PLAYER_COLORS)-1)]
        self.name = name
        self.pieces = list()
        piece = Piece(surface,(self.x,self.y),self.color,self.mass,self.name)

    # Should be called before each new blit
    def update(self):
        self.move()
        self.collisionDetection()

    # Any cell closer than the radius of player will be eaten
    def collisionDetection(self):
        for cell in CELLS:
            if(getDistance((cell.x,cell.y),(self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                CELLS.remove(cell)


    def move(self):
        dX,dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY-(float(SCREEN_HEIGHT)/2),dX-(float(SCREEN_WIDTH)/2))
        # Convert radians to degrees [-180, 180]
        rotation *= 180/math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90-math.fabs(rotation))/90
        vx = self.speed * normalized
        vy = 0
        if(rotation < 0):
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def feed(self):
        pass

    def split(self):
        pass

    # Draw the player
    def draw(self,cam):
        col = self.color
        zoom = cam.zoom
        x = cam.x
        y = cam.y
        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface,(col[0]-int(col[0]/3),int(col[1]-col[1]/3),int(col[2]-col[2]/3)),(int(self.x*zoom+x),int(self.y*zoom+y)),int((self.mass/2+3)*zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface,col,(int(self.x*cam.zoom+cam.x),int(self.y*cam.zoom+cam.y)),int(self.mass/2*zoom))
        if(len(self.name) > 0):
            fw, fh = font.size(self.name)
            # Draw player's name
            drawText(self.name, (self.x*cam.zoom+cam.x-int(fw/2),self.y*cam.zoom+cam.y-int(fh/2)),(50,50,50))

# Totally unused class
class Piece:
    def __init__(self,surface,pos,color,mass,name,transition=False):
        self.x,self.y = pos
        self.mass = mass
        self.splitting = transition
        self.surface = surface
        self.name = name

    def draw(self):
        pass

    def update(self):
        if(self.splitting):
            pass

# Semantically, this is a parent class of player
# Represents the smallest quantities of mass the player eats
class Cell:
    def __init__(self,surface):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.surface = surface
        self.color = CELL_COLORS[random.randint(0,len(CELL_COLORS)-1)]

    def draw(self,cam):
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*cam.zoom))

# Populates the global cell-list with randomly placed cells
def spawn_cells(numOfCells):
    for i in range(numOfCells):
        cell = Cell(MAIN_SURFACE)
        CELLS.append(cell)

# Draws the background grid on every call
def draw_grid():
    for i in range(0,2001,25):
        pygame.draw.line(MAIN_SURFACE,(230,240,240),(0+camera.x,i*camera.zoom+camera.y),(2001*camera.zoom+camera.x,i*camera.zoom+camera.y),3)
        pygame.draw.line(MAIN_SURFACE,(230,240,240),(i*camera.zoom+camera.x,0+camera.y),(i*camera.zoom+camera.x,2001*camera.zoom+camera.y),3)

camera = Camera()
# Main player
blob = Player(MAIN_SURFACE,"Viliami")
spawn_cells(2000)

# Draws the Heads-Up Display on screen.
def draw_HUD():
    w,h = font.size("Score: "+str(int(blob.mass*2))+" ")
    MAIN_SURFACE.blit(pygame.transform.scale(SCOREBOARD_SURFACE,(w,h)),(8,SCREEN_HEIGHT-30))
    MAIN_SURFACE.blit(LEADERBOARD_SURFACE,(SCREEN_WIDTH-160,15))
    drawText("Score: " + str(int(blob.mass*2)),(10,SCREEN_HEIGHT-30))
    MAIN_SURFACE.blit(big_font.render("Leaderboard",0,(255,255,255)),(SCREEN_WIDTH-157,20))
    drawText("1. G #1",(SCREEN_WIDTH-157,20+25))
    drawText("2. G #2",(SCREEN_WIDTH-157,20+25*2))
    drawText("3. ISIS",(SCREEN_WIDTH-157,20+25*3))
    drawText("4. ur mom",(SCREEN_WIDTH-157,20+25*4))
    drawText("5. w = pro team",(SCREEN_WIDTH-157,20+25*5))
    drawText("6. jumbo",(SCREEN_WIDTH-157,20+25*6))
    drawText("7. [voz]plz team",(SCREEN_WIDTH-157,20+25*7))
    drawText("8. G #3",(SCREEN_WIDTH-157,20+25*8))
    drawText("9. doge",(SCREEN_WIDTH-157,20+25*9))
    if(blob.mass <= 500):
        drawText("10. G #4",(SCREEN_WIDTH-157,20+25*10))
    else:
        drawText("10. Viliami",(SCREEN_WIDTH-157,20+25*10),(210,0,0))

# Main loop
while(True):
    # Set FPS
    clock.tick(70)

    # Check for events
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            # The player pressed 'esc'
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            # The player pressed 'space'
            if(e.key == pygame.K_SPACE):
                blob.split()
            # The player pressed 'W'
            if(e.key == pygame.K_w):
                blob.feed()
        # The player clicked the 'X' button
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()

    # Check what player eats and set his/her new position
    blob.update()
    # Update camera zoom. Is this supposed to be here?
    camera.zoom = 100/(blob.mass)+0.3
    camera.centre(blob)
    MAIN_SURFACE.fill((242,251,255))
    # Uncomment next line to get dark-theme
    #surface.fill((0,0,0))

    # Extremely painful procedure (re-painting the huge grid):
    draw_grid()
    for c in CELLS:
        c.draw(camera)

    # Update player's position on screen
    blob.draw(camera)
    draw_HUD()
    # Start calculating next frame
    pygame.display.flip()
