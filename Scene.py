from Grid import *
from Tetrimino import *

class Scene_Player:
    def __init__(self, tetrimino):
        self.grid_game_player = Grid_Game(0, (WIDTH - NBR_ROW*TETRIMINO_BASIC_SIZE)/2, (HEIGHT - NBR_LINE*TETRIMINO_BASIC_SIZE)/2, NBR_ROW, NBR_LINE)
        self.player_tetrimino = tetrimino
        self.next_tetrimino = Tetriminos(1, NBR_ROW + 2, 4, 1, 0)
        self.next_tetrimino.randomChange(4, 0)
        self.player_tetrimino.copyTetrimino(self.next_tetrimino)
        self.next_tetrimino.randomChange(4, 0)
        self.userAction = False
        self.userAction2 = False
        self.updateTetrimino = False
        self.game_over = False

    def eventTick(self, event):
        self.userAction, self.userAction2 = self.player_tetrimino.eventTick(event)

    def update(self, last_time):
        lt = last_time
        if self.userAction == True:
            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if yc == 1:
                self.player_tetrimino.position_y -= 1
                self.updateTetrimino = True
                if self.player_tetrimino.position_y < 0:
                    self.game_over = True
        if self.userAction2 == True:
            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if xc == -1:
                self.player_tetrimino.position_x += 1

            xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

            if xc == 1:
                self.player_tetrimino.position_x -= 1

        now = pygame.time.get_ticks()
        if now - lt > 1000:
            lt = now
            self.player_tetrimino.position_y += 1

        xc, yc = self.grid_game_player.collision_to_Grid_Tetrimino(self.player_tetrimino, 0)

        if yc == 1:
            self.updateTetrimino = True
            self.player_tetrimino.position_y -= 1
            if self.player_tetrimino.position_y < 0:
                self.game_over = True

        if self.grid_game_player.collision_to_border_grid(self.player_tetrimino):
            k = self.player_tetrimino.limiteBoundari(0, 0, NBR_ROW, NBR_LINE)
            if self.updateTetrimino == False:
                self.updateTetrimino = k

        if self.updateTetrimino == True:
            self.grid_game_player.update(self.player_tetrimino, 0)

        return lt

    def draw(self, screen):
        self.grid_game_player.draw_me(screen, GRID_PALETTE, TETRIMINO_BASIC_SIZE)
        self.player_tetrimino.drawTetrimino(screen, GRID_PALETTE, 0, TETRIMINO_BASIC_SIZE, self.grid_game_player)
        self.next_tetrimino.drawTetrimino(screen, GRID_PALETTE, 0, TETRIMINO_BASIC_SIZE, self.grid_game_player)

    def update_last_time(self):
        if self.updateTetrimino == True:
            self.updateTetrimino = False

            self.grid_game_player.line_delete(0)
            self.player_tetrimino.set_position(int((NBR_ROW - self.player_tetrimino.width) / 2), 0)
            self.player_tetrimino.copyTetrimino(self.next_tetrimino)
            self.next_tetrimino.randomChange(4, 0)

        self.userAction = False
        self.userAction2 = False