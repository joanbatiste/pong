import pygame, sys, random
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

def pause():
    paused = True
    while paused :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                
               

def player_animation():
    player.y += player_speed 
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ia():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def draw_text(text, font, surface, x, y, main_color, background_color=None):
    textobj = font.render(text, True, main_color, background_color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)


def start_screen():
    pantalla_inicio = True
    while pantalla_inicio:
        title_font = pygame.font.Font(None, 75)
        big_font = pygame.font.Font(None, 45)
        draw_text('THE REAL PONG', title_font, screen, screen_width / 2, screen_height / 3, blue, black)                  
        draw_text('Use space for start       Use P to pause', big_font, screen, screen_width / 2, screen_height / 2, blue, black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pantalla_inicio = False
                    
        pygame.display.update()
                
def win_screen():
    victory_screen = True
    while victory_screen:
        if score_player == 5:
            title_font = pygame.font.Font(None, 75)
            big_font = pygame.font.Font(None, 45)            
            draw_text('!!!  PLAYER   WINS  !!!', title_font, screen, screen_width / 2, screen_height / 3, red, black)
            draw_text('Use space for re-start       Use Q to quit game', big_font, screen, screen_width / 2, screen_height / 2, red, black)

        if score_opponent == 5:
            title_font = pygame.font.Font(None, 75)
            big_font = pygame.font.Font(None, 45)            
            draw_text('!!!  MACHINE   WINS  !!!', title_font, screen, screen_width / 2, screen_height / 3, blue, black)
            draw_text('Use space for re-start       Use Q to quit game', big_font, screen, screen_width / 2, screen_height / 2, blue, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    victory_screen = False
                    running = True
        pygame.display.flip()
    return running


        
running = True
while running:

    # Ventana de juego

    screen_width = 1200
    screen_height = 960
    screen = pygame.display.set_mode( ( screen_width, screen_height ) )
    pygame.display.set_caption('Pong')

    # Colors
    white = (255,255,255)
    light_grey = (200,200,200)
    bg_color = pygame.Color("grey12")
    red = (255,50,50)
    blue = (50,50,255)
    black = (0,0,0)

    #Elementos de Juego
    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
    player = pygame.Rect(screen_width - 20, screen_height / 2-70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2-70, 10, 140)

    # Marcador
    score_player = 0
    score_opponent = 0
    score_player_fin = score_player  #probar marcador final
    score_opponent_fin = score_opponent #probar marcador final

    #Fuentes
    score_font = pygame.font.SysFont("arial", 60)


    #Sonidos
    golpeo_player = pygame.mixer.Sound('1.mp3.wav')
    golpeo_opponent = pygame.mixer.Sound('3.mp3.wav')
    golpeo_pared = pygame.mixer.Sound('2.mp3.wav')
    punto_ganador = pygame.mixer.Sound('win.mp3.wav')

    #Valores de juego
    player_speed = 0
    opponent_speed = 15
    ball_speed_x = 7 * random.choice((1,-1))
    ball_speed_y = 7 * random.choice((1,-1))

    start_screen()



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed -= 8
                if event.key == pygame.K_DOWN:
                    player_speed += 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed += 8
                if event.key == pygame.K_DOWN:
                    player_speed -= 8
            if event.type == pygame.KEYDOWN:
                if event.key ==K_p:
                    pause()

        
        # Animaciones
        player_animation()
        opponent_ia()
            
        ball.x += ball_speed_x
        ball.y += ball_speed_y

            
        if (ball.top <= 0 or ball.bottom >= screen_height):
            ball_speed_y *= -1
            golpeo_pared.play()

        if ball.right >= screen_width:        
            ball.center = (screen_width / 2, screen_height / 2)
            ball_speed_x = 7 * random.choice((1,-1))
            ball_speed_y = 7 * random.choice((1,-1))
            score_opponent +=1
            punto_ganador.play()
                
        if ball.left <= 0:
            ball.center = (screen_width / 2, screen_height / 2)
            ball_speed_x = 7 * random.choice((1,-1))
            ball_speed_y = 7 * random.choice((1,-1))
            score_player += 1
            punto_ganador.play()

        if ball.colliderect(player):
            ball_speed_x *= -1.125      
            golpeo_player.play()

        if ball.colliderect(opponent):
            ball_speed_x *= -1.125       
            golpeo_opponent.play()
        if score_player == 5 or score_opponent == 5:
            
            running = False
            



        # Dibujar
        screen.fill(bg_color)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.rect(screen, red, player)
        pygame.draw.rect(screen, blue, opponent)
        pygame.draw.aaline(screen, light_grey,(screen_width/2, 0), (screen_width/2, screen_height))
        score1 = score_font.render(str(score_opponent), 1, blue)
        score2 = score_font.render(str(score_player), 1, red)
    
                
        screen.blit(score1, (screen_width/2-100,50))
        screen.blit(score2, (660,50))


        pygame.display.flip()
        clock.tick(60)

    running = win_screen()
          

