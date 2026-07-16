import pygame ,sys , random

pygame.init() #main
screen = pygame.display.set_mode((800,600)) #設定視窗大小(寬,高)
pygame.display.set_caption("敲磚塊遊戲") #設定標題
clock = pygame.time.Clock() #控制fps
#初始設定
def mainset():
    global ballx,bally,boardx,start,end,ballbound,point,live,brickl
    ballx,bally = 400,530
    boardx = 340
    start = False
    end = False
    ballbound = 0 
    point = 0 
    live = 3
    brickl = []
    for i in range(2,802,100): #8 寬
        for j in range(2,272,30): #9 高
            brickl.append([i,j,"t"])

mainset()

#顏色(R,G,B)
lightblue = (0,200,255)
darkblue = (0,0,139)
black = (0,0,0)
white = (255,255,255)
orange = (255,100,0)
green = (0,128,0)
yellow = (255,255,0)

#畫圖(磚塊、板子、球)
def draw(boardx,ballx,bally): #x從左到右 y從上到下
    pygame.draw.rect(screen,green,(boardx,550,120,10)) #rect(畫面,顏色,(x,y,寬,高) #中心:x=300
    pygame.draw.circle(screen,yellow,(ballx,bally),20) #circle(畫面,顏色,圓心位置,半徑)
    for i in range(72):
        if brickl[i][2] == "t":
            pygame.draw.rect(screen,orange,(brickl[i][0],brickl[i][1],96,26))

#顯示文字
def font(x):
    return pygame.font.SysFont('simhei',x)
    
#板子移動
def boardmove(): 
    global boardx,start
    if keys[pygame.K_LEFT]:
        boardx -= 15
    if keys[pygame.K_RIGHT]:
        boardx += 15
    if boardx < 10: boardx = 0 
    if boardx > 680: boardx = 680
    
#球移動
def ballmove():
    global ballx,bally,vx,vy,ballbound,live,point,start
    ballbound += 1
    speed = 12 / (vx**2 + vy**2)**0.5 
    ballx -= vx * speed
    bally -= vy * speed
    if ballx > 775 or ballx < 25:
        vx = -vx
    if bally < 25:
        vy = -vy
    if boardx-10 < ballx < (boardx + 120+10) and abs(bally +20 - 550) < abs(vy) +2 and ballbound > 5:
        vy = -vy
        ballbound = 1
        print(abs(ballx - (boardx+60)))
        if 1 < abs((ballx+20) - (boardx+60)) <= 20:
            ballm2(3)
        elif 20 < abs((ballx+20) - (boardx+60)) <= 40:
            ballm2(7)
        elif 40 < abs((ballx+20) - (boardx+60)) <= 70:
            ballm2(10)
    elif bally > 600:
        live -= 1
        ballx,bally = 400,530
        start = False
    for i in range(71,-1,-1): #球半徑=20,磚塊寬=96,磚塊高=26
        if ( (brickl[i][0]-20) <= ballx <= (brickl[i][0]+96+20)) and (abs(brickl[i][1] -20 - bally) < abs(vy)+2  or abs(brickl[i][1] + 26 + 20 - bally) < abs(vy)+2) and (brickl[i][2] == "t"): #上下
            brickl[i][2] = "f"
            point += 1
            vy = -vy
            break
        elif (abs(brickl[i][0] -20 - ballx ) < abs(vx)+2 or abs(brickl[i][0] +96 +20 - ballx) < abs(vx)+2 ) and brickl[i][1] -20 <= bally <= (brickl[i][1]+26+20) and (brickl[i][2] == "t"): #左右
            brickl[i][2] = "f"
            point += 1
            vx = -vx
            break           
def ballm2(speed):
    global vx
    if vx > 0:
        vx = speed
    else:
        vx = -speed
        
#開始遊戲
def Start():
    global start,vx,vy
    if keys[pygame.K_UP]:
        start = True
        vx = random.randint(-10,10)
        vy = 10

#遊戲結束
def gameover():
    global end
    if point == 72 or live <=0 :
        end = True
        pygame.draw.rect(screen,darkblue,(100,100,590,450)) 
        pygame.draw.rect(screen,lightblue,(115,115,560,420))
        endpoint_text = font(80).render(f"You get {point} point!",True,white)
        screen.blit(endpoint_text,(170,240))
        pygame.draw.rect(screen,yellow,(270,350,230,100))
        playagain_text = font(60).render("play again",True,black)
        screen.blit(playagain_text,(282,375))
        if live <= 0:
            end_text = font(120).render("GAME OVER",True,white)
            screen.blit(end_text,(130,140))
        else:
            end_text = font(120).render("YOU WIN!",True,white)
            screen.blit(end_text,(180,140))
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(270,350,230,100)
            if event.button == 1 and button_rect.collidepoint(event.pos):
                end = False
                mainset()

while 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit() #將pygame殺掉
            sys.exit() #終止程式

    keys = pygame.key.get_pressed()
    #if not (keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                #pass
    screen.fill((30,30,30))
    draw(boardx,ballx,bally)
    if start==True:
        gameover()
        if end ==False:
            ballmove()
    else:
        gameover()
        if end == False:
            Start()
            start_text = font(60).render("press up to start",True,white)
            start_text2 = font(60).render("press right or left to move the board",True,white)
            boardx = 340
            screen.blit(start_text,(225,370))
            screen.blit(start_text2,(30,430))
            ballbound = 0 
    if end == False:
        boardmove()
        point_text = font(48).render(f"point:{point}",True,white)
        live_text = font(48).render(f"live={live}",True,white)
        screen.blit(point_text,(30,30))
        screen.blit(live_text,(30,70))
    pygame.display.flip()
    clock.tick(30)
    


