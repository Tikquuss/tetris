from Grid import  *
from Tetrimino import  *
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

while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        if scene_player.game_over == False:
            scene_player.eventTick(event)

    # Update
    if scene_player.game_over == False:
        last_time = scene_player.update(last_time)

    # Draw / render
    screen.fill(BLUE_CLOUD)
    if scene_player.game_over == False:
        scene_player.draw(screen)

    #after drawing everything, flip the scree
    pygame.display.flip()
    if scene_player.game_over == False:
        scene_player.update_last_time()