import pygame
pygame.init()       
pygame.font.init()  

display = pygame.display.set_mode((1280,720))

player1_img = pygame.image.load("assets/player1.png")
player2_img = pygame.image.load("assets/player2.png")
ball_img = pygame.image.load("assets/ball.png")
campo_img = pygame.image.load("assets/bg.png")
campo = campo_img.get_rect()
gameover_img = pygame.image.load("assets/gameover.png")
gameover = gameover_img.get_rect()
menu_img = pygame.image.load("assets/menu.png")
menu = menu_img.get_rect()

player1 = player1_img.get_rect()
player1_score = 0
player1_speed = 10

player2 = player2_img.get_rect(right = 1280) # mete na direita
player2_score = 0
player2_speed = 10

ball = ball_img.get_rect(center = [640, 360]) # meio da tela
ball_dir_x = 10 # velocidades da bolinha
ball_dir_y = 10

font = pygame.font.Font(None, 70) # None - padrão do sistema
placar_player1 = font.render(str(player1_score), True, "blue") # texto, antialias, cor
placar_player2 = font.render(str(player2_score), True, "red")

# Pra fazer um fade, cria uma imagem preta e vai alterando o alpha dela quando quiser:
fade_img = pygame.Surface((1280,720)).convert_alpha() # cria uma Surface vazia com controle de transparencia
fade_img.fill("black") # pinta de preto
fade_alpha = 255 # nível de transparencia inicial, depois vou decrescendo
fade = fade_img.get_rect() # rect pro tamanho da Surface

music = pygame.mixer.Sound("assets/music.ogg")
music.play(-1) # loop

cena = "menu" 

fps = pygame.time.Clock() # Trabalha junto com as variaveis de velocidades aqui

loop = True
while loop: 

    if cena == "jogo":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # botão fechar
                loop = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1_speed = -10
                elif event.key == pygame.K_s:
                    player1_speed = 10
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2_speed = -10
                elif event.key == pygame.K_DOWN:
                    player2_speed = 10
                    
        if player1_score >= 3:
            cena = "gameover"
            fade_alpha = 255
            
        if player2_score >= 3:
            cena = "gameover"
            fade_alpha = 255
        
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_dir_x *= -1
            hit = pygame.mixer.Sound("assets/pong.wav")
            hit.play()
        
        if player1.y <= 0: 
            player1.y = 0
        elif player1.y >= 700 - 150:
            player1.y = 700 - 150

        player1.y += player1_speed

        if ball.x <= 0:
            player2_score += 1
            # Olha a chinelagem: se não mandar atualizar, ele não atualiza:
            placar_player2 = font.render(str(player2_score), True, "red")
            ball.x = 600
            ball_dir_x *= -1
        elif ball.x >= 1280:
            player1_score += 1
            placar_player1 = font.render(str(player1_score), True, "blue")
            ball.x = 600
            ball_dir_x *= -1

        if ball.y <= 0:
            ball_dir_y *= -1
        elif ball.y >= 700 - 15:
            ball_dir_y *= -1

        ball.x += ball_dir_x 
        ball.y += ball_dir_y 

        #player2.y = ball.y - 75 # segue a bola na metade do rect do player2
        player2.y += player2_speed

        if player2.y <= 0:
            player2.y = 0
        elif player2.y >= 720 - 150:
            player2.y = 720 - 150
            
        if fade_alpha > 0:
            fade_alpha -= 10 # decresce a transparencia
            fade_img.set_alpha(fade_alpha) # aplica a transparencia na tela preta 
        
        # Te liga que tudo tem ordem!!!
        display.fill((0,0,0))
        display.blit(campo_img, campo)
        display.blit(player1_img, player1)
        display.blit(player2_img, player2)
        display.blit(ball_img, ball)
        display.blit(placar_player1, (500, 50))
        display.blit(placar_player2, (780, 50))
        display.blit(fade_img, fade)
        
    elif cena == "gameover": 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    cena = "menu"
                    fade_alpha = 255
                    
        if fade_alpha > 0:
            fade_alpha -= 10 
            fade_img.set_alpha(fade_alpha) 
                
        display.blit(gameover_img, gameover)
        display.blit(fade_img, fade) 
        
    elif cena == "menu": 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loop = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # se pressionar enter, reseta as coisas:
                    player1_score = 0
                    placar_player1 = font.render(str(player1_score), True, "blue")
                    player2_score = 0
                    placar_player2 = font.render(str(player2_score), True, "red")
                    player1.y = 0
                    player2.y = 0
                    ball.x = 640
                    ball.y = 320
                    cena = "jogo"
                    fade_alpha = 255
                    start = pygame.mixer.Sound("assets/start.wav")
                    start.play()
        
        if fade_alpha > 0:
            fade_alpha -= 1 
            fade_img.set_alpha(fade_alpha) 
                
        display.fill((0,0,0)) 
        display.blit(menu_img, menu)
        display.blit(fade_img, fade) 

    fps.tick(60)
    pygame.display.flip() # atualiza a tela constantemente