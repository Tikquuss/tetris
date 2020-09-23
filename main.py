from Scene import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
clock_break = pygame.time.Clock()

# initialize variable
player_one = Player(1, int((NBR_ROW - 3)/2), 0, 1, 0)
scene_player = Scene_Player(player_one)

# Game loop
last_time = pygame.time.get_ticks()
updateTetrimino = False
running = True

font = pygame.font.Font("datas/comfortaa.ttf", 50)
GameOverX = int((WIDTH - ( 5 * 50))/2)
GameOverY = int((HEIGHT - 50)/2)

game_pause = False

while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        if scene_player.game_over == False and game_pause == False:
            scene_player.eventTick(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if scene_player.game_over == False:
                    game_pause = not game_pause
                else:
                    del scene_player
                    del player_one
                    player_one = Player(1, int((NBR_ROW - 3) / 2), 0, 1, 0)
                    scene_player = Scene_Player(player_one)


    # Update
    if scene_player.game_over == False and game_pause == False:
        last_time = scene_player.update(last_time)

    # Draw / Render
    screen.fill(BLUE_CLOUD)
    scene_player.draw(screen)

    if scene_player.game_over and game_pause == False:
        gameOver_render = font.render("Game Over", True, (255, 0, 255))
        screen.blit(gameOver_render, (GameOverX, GameOverY))

    if game_pause and scene_player.game_over == False:
        gamePause_render = font.render("Game Pause", True, (255, 0, 255))
        screen.blit(gamePause_render, (GameOverX, GameOverY))

    #after drawing everything, flip the scree
    pygame.display.flip()
    if scene_player.game_over == False and game_pause == False:
        scene_player.update_last_time()

pygame.quit()