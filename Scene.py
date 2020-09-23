from Grid import *
from Tetrimino import *

class Scene_Player:
    def __init__(self, tetrimino):
        self.grid_game_player = Grid_Game(0, (WIDTH - NBR_ROW*TETRIMINO_BASIC_SIZE)/2, (HEIGHT - NBR_LINE*TETRIMINO_BASIC_SIZE)/2, NBR_ROW, NBR_LINE)
        self.player_tetrimino = tetrimino
        self.next_tetrimino = Tetriminos(1, NBR_ROW + 2, 4, 1, 0)
        self.next_tetrimino.randomChange(4, 0)
        self.player_tetrimino.copyTetrimino(self.next_tetrimino)
        self.player_tetrimino.set_position(int((NBR_ROW - self.player_tetrimino.width) / 2),
                                           -self.player_tetrimino.height)
        self.next_tetrimino.randomChange(4, 0)
        self.userAction = False
        self.userAction2 = False
        self.updateTetrimino = False
        self.game_over = False
        self.speed_fale = 1000
        self.level = 1
        self.bonus_destruct = 0
        self.bonus = 0
        self.total_bonus = 0

        self.font = pygame.font.Font("datas/comfortaa.ttf", 24)
        self.scoreX = NBR_ROW + 2
        self.scoreY = 14
        self.timeX = NBR_ROW + 2
        self.timeY = 12
        self.time_evolution = 0
        self.delay_time = pygame.time.get_ticks()
        self.levelX = NBR_ROW + 2
        self.levelY = 10
    def eventTick(self, event):
        self.userAction, self.userAction2 = self.player_tetrimino.eventTick(event, self.userAction, self.userAction2)

    def update(self, last_time):
        lt = last_time
        self.player_tetrimino.update()
        if self.userAction2 == True:
            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if xc == -1:
                self.player_tetrimino.position_x += -self.player_tetrimino.speed_x
            elif xc == 1:
                self.player_tetrimino.position_x += -self.player_tetrimino.speed_x

        if self.userAction == True:
            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if yc == 1:
                self.player_tetrimino.position_y -= self.player_tetrimino.speed_y
                self.updateTetrimino = True

        now = pygame.time.get_ticks()
        if now - lt > self.speed_fale:
            lt = now
            self.player_tetrimino.position_y += 1

            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if yc == 1:
                self.updateTetrimino = True
                self.player_tetrimino.position_y -= 1

        if self.grid_game_player.collision_to_border_grid(self.player_tetrimino):
            k = self.player_tetrimino.limiteBoundari(0, 0, NBR_ROW, NBR_LINE)
            if self.updateTetrimino == False:
                self.updateTetrimino = k

        if self.updateTetrimino == True:
            self.grid_game_player.update(self.player_tetrimino, 0)

        now2 = pygame.time.get_ticks()
        if now2 - self.delay_time > 1000:
            self.delay_time = now2
            self.time_evolution += 1

        self.game_over = self.grid_game_player.isGameOver(0)

        return lt

    def draw(self, screen):
        self.grid_game_player.draw_me(screen, GRID_PALETTE, TETRIMINO_BASIC_SIZE)
        self.player_tetrimino.drawTetrimino(screen, GRID_PALETTE, 0, TETRIMINO_BASIC_SIZE, self.grid_game_player)
        self.next_tetrimino.drawTetrimino(screen, GRID_PALETTE, 0, TETRIMINO_BASIC_SIZE, self.grid_game_player)

        score_render = self.font.render("Score : "+str(self.total_bonus), True, GRID_PALETTE[1])
        screen.blit(score_render, (self.grid_game_player.position_x + self.scoreX*TETRIMINO_BASIC_SIZE,
                    self.grid_game_player.position_y + self.scoreY*TETRIMINO_BASIC_SIZE))
        time_render = self.font.render("Time : " + str(self.time_evolution), True, GRID_PALETTE[1])
        screen.blit(time_render, (self.grid_game_player.position_x + self.timeX * TETRIMINO_BASIC_SIZE,
                    self.grid_game_player.position_y + self.timeY * TETRIMINO_BASIC_SIZE))
        level_render = self.font.render("Level : " + str(self.level), True, GRID_PALETTE[1])
        screen.blit(level_render, (self.grid_game_player.position_x + self.levelX * TETRIMINO_BASIC_SIZE,
                                  self.grid_game_player.position_y + self.levelY * TETRIMINO_BASIC_SIZE))

    def update_last_time(self):
        if self.updateTetrimino == True:
            self.updateTetrimino = False

            k = BONUS_DESTRUCTION*self.grid_game_player.line_delete(0)
            if k != 0:
                self.bonus_destruct += k
                if self.bonus_destruct % 100 == 0:
                    self.level += 1
                    if self.level <= 90 :
                        self.speed_fale -= 10

                self.total_bonus = self.bonus_destruct + self.bonus

            self.player_tetrimino.copyTetrimino(self.next_tetrimino)
            self.player_tetrimino.set_position(int((NBR_ROW - self.player_tetrimino.width) / 2),
                                               -self.player_tetrimino.height)
            self.next_tetrimino.randomChange(4, 0)