import pygame,random,math

pygame.init()
colors_players = [(37,7,255),(35,183,253),(48,254,241),(19,79,251),(255,7,230),(255,7,23),(6,254,13)]
colors_cells = [(80,252,54),(36,244,255),(243,31,46),(4,39,243),(254,6,178),(255,211,7),(216,6,254),(145,255,7),(7,255,182),(255,6,86),(147,7,255)]
colors_viruses = [(66,254,71)]

class Player:
    def __init__(self,surface):
        self.x = random.randint(100,400)
        self.y = random.randint(100,400)
        self.mass = 20
        self.surface = surface
        self.color = colors_players[random.randint(0,len(colors_players)-1)]
    
    def update(self):
        self.move()

    def move(self):
        dX,dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY-self.y,dX-self.x)*180/math.pi
        speed = 2
        vx = speed * (90-math.fabs(rotation))/90
        vy = 0
        if(rotation < 0):
            vy = -speed + math.fabs(vx)
        else:
            vy = speed - math.fabs(vx)
        self.x += vx
        self.y += vy
        
    def draw(self):
        pygame.draw.circle(self.surface,self.color,(int(self.x),int(self.y)),self.mass)
        pygame.draw.circle(self.surface,(self.color[0]-int(self.color[0]/3),int(self.color[1]-self.color[1]/3),int(self.color[2]-self.color[2]/3)),(int(self.x),int(self.y)),self.mass,int(80/self.mass))

screen_width, screen_height = (500,500)
surface = pygame.display.set_mode((screen_width,screen_height))
t_surface = pygame.Surface((95,25),pygame.SRCALPHA) #transparent rect for score
t_lb_surface = pygame.Surface((155,278),pygame.SRCALPHA) #transparent rect for leaderboard
t_surface.fill((50,50,50,80))
t_lb_surface.fill((50,50,50,80))
blob = Player(surface)
pygame.display.set_caption("Agar.io")
cell_list = list()
font = pygame.font.Font("Ubuntu-B.ttf",20)
big_font = pygame.font.Font("Ubuntu-B.ttf",24)

class Cell:
    def __init__(self,surface):
        self.x = random.randint(20,480)
        self.y = random.randint(20,480)
        self.mass = 5-1
        self.surface = surface
        self.color = colors_cells[random.randint(0,len(colors_cells)-1)]
        
    def draw(self):
        pygame.draw.circle(self.surface,self.color,(self.x,self.y),self.mass)

def spawn_cells():
    for i in range(0,120):
        cell = Cell(surface)
        cell_list.append(cell)
        
def draw_grid():
    for i in range(0,screen_width,20):
        pygame.draw.line(surface,(234,242,246),(0,i),(screen_width,i))
        pygame.draw.line(surface,(234,242,246),(i,0),(i,screen_height))

def drawText(string,pos,color=(255,255,255)):
    surface.blit(font.render(string,0,color),pos)

def draw_HUD():
    surface.blit(t_surface,(8,screen_height-30))
    surface.blit(t_lb_surface,(screen_width-160,15))
    drawText("Score: 10",(10,screen_height-30))
    surface.blit(big_font.render("Leaderboard",0,(255,255,255)),(screen_width-157,20))
    drawText("1. G #1",(screen_width-157,20+25))
    drawText("2. G #2",(screen_width-157,20+25*2))
    drawText("3. ISIS",(screen_width-157,20+25*3))
    drawText("4. ur mom",(screen_width-157,20+25*4))
    drawText("5. w = pro team",(screen_width-157,20+25*5))
    drawText("6. jumbo",(screen_width-157,20+25*6))
    drawText("7. [voz]plz team",(screen_width-157,20+25*7))
    drawText("8. G #3",(screen_width-157,20+25*8))
    drawText("9. doge",(screen_width-157,20+25*9))
    drawText("10. G #4",(screen_width-157,20+25*10))

spawn_cells()
clock = pygame.time.Clock()
while(True):
    clock.tick(60)
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
        if(e.type == pygame.QUIT):
            pygame.quit()
    blob.update()
    surface.fill((242,251,255))
    draw_grid()
    for c in cell_list:
        c.draw()
    blob.draw()
    draw_HUD()
    pygame.display.flip()
