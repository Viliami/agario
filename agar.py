import pygame,random,math

# Color Definitions
PLAYER_COLORS = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255)]

VIRUS_COLORS = [(66,254,71)]

# Dimension Definitions
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (2000,2000)

# Other Definitions
CELLS = list()

# Pygame initialization
pygame.init()
pygame.display.set_caption("Agar.io")
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
SCOREBOARD_SURFACE = pygame.Surface((95,25),pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155,278),pygame.SRCALPHA) 
SCOREBOARD_SURFACE.fill((50,50,50,80))
LEADERBOARD_SURFACE.fill((50,50,50,80))

# Auxiliary Functions
def drawText(message,pos,color=(255,255,255)):
    """Blits text to main (global) screen.
    """
    MAIN_SURFACE.blit(font.render(message,1,color),pos)

def getDistance(pos1,pos2):
    """Calculates Euclidean distance between given points.
    """
    px,py = pos1
    p2x,p2y = pos2
    diffX = math.fabs(px-p2x)
    diffY = math.fabs(py-p2y)
    return ((diffX**2)+(diffY**2))**(0.5)


class Camera:
    """Used to represent the concept of POV.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    
    def centre(self,blobOrPos):
        """Makes sure that the given object will be at the center of player's view. 
        Zooms is taken into account as well.
        """
        if(isinstance(blobOrPos,Player)):
            p = blobOrPos
            self.x = (p.startX-(p.x*self.zoom))-p.startX+((SCREEN_WIDTH/2))
            self.y = (p.startY-(p.y*self.zoom))-p.startY+((SCREEN_HEIGHT/2))
        elif(type(blobOrPos) == tuple):
            self.x,self.y = blobOrPos

class Player:
    """Used to represent the concept of a player.
    """
    
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
        piece = Piece(surface,(self.x,self.y),self.color,self.mass,self.name) #not used or needed

    def update(self):
        """Updates players position and detects cells that can be eaten.
        Cells than can be  eaten are appropriately removed.
        """
        self.move()
        self.collisionDetection()

    def collisionDetection(self):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        for cell in CELLS:
            if(getDistance((cell.x,cell.y),(self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                CELLS.remove(cell)


    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """
        
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
        """Unsupported feature.
        """
        pass

    def split(self):
        """Unsupported feature.
        """
        pass

    def draw(self,cam):
        """Draws a player as an outlined circle.
        """
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

class Piece:
    """Unsupported feature.
    """
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


class Cell: # Semantically, this is a parent class of player
    """Used to represent the fundamental entity of game.
    A cell can be considered as a quantom of mass.
    It can be eaten by other entities.
    """
    def __init__(self,surface):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.surface = surface
        self.color = CELL_COLORS[random.randint(0,len(CELL_COLORS)-1)]

    def draw(self,cam):
        """Draws a cell as a simple circle.
        """
        pygame.draw.circle(self.surface,self.color,(int((self.x*cam.zoom+cam.x)),int(self.y*cam.zoom+cam.y)),int(self.mass*cam.zoom))

def spawn_cells(numOfCells):
    """Populates the global cell-list with randomly placed cells.
    """
    for i in range(numOfCells):
        cell = Cell(MAIN_SURFACE)
        CELLS.append(cell)


def draw_grid():
    """Draws the background grid on main surface.
    """

    # A grid is a set of horizontal and prependicular lines
    for i in range(0,2001,25):
        pygame.draw.line(MAIN_SURFACE,(230,240,240),(0+camera.x,i*camera.zoom+camera.y),(2001*camera.zoom+camera.x,i*camera.zoom+camera.y),3)
        pygame.draw.line(MAIN_SURFACE,(230,240,240),(i*camera.zoom+camera.x,0+camera.y),(i*camera.zoom+camera.x,2001*camera.zoom+camera.y),3)


# Initialize essential entities
camera = Camera()
blob = Player(MAIN_SURFACE,"Viliami")
spawn_cells(2000)


def draw_HUD():
    """Draws the Heads-Up Display the main surface.
    """
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

# Game main loop
while(True):
    
    clock.tick(70)
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if(e.key == pygame.K_SPACE):
                blob.split()
            if(e.key == pygame.K_w):
                blob.feed()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()


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
