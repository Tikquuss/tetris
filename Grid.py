import pygame
from pygame.locals import *
import numpy as np
import  copy

from Utils import *

class Grid_Game:
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.number_row = NBR_ROW
        self.number_line = NBR_LINE
        self.table_color = np.full((self.number_row, self.number_line), 0)

    def __init__(self, indexColor, xPosition, yPosition, nbrRow, nbrLine):
        self.position_x = xPosition
        self.position_y = yPosition
        self.number_row = nbrRow
        self.number_line = nbrLine
        self.table_color = np.full((self.number_row, self.number_line), indexColor)

    def draw_me(self, screen_draw, gridPalette, size_block):
        for j in range(self.number_line):
            for i in range(self.number_row):
                pygame.draw.rect(screen_draw, gridPalette[self.table_color[i][j]], Rect(self.position_x + i * size_block, self.position_y + j * size_block, size_block, size_block))

    def change_color_index(self, index_i, index_j, indexColor):
        self.table_color[index_i][index_j] = indexColor

    def change_Color_Line(self, indexColor):
        for i in range(self.number_row):
            self.table_color[i][self.number_line] = indexColor

    def update(self, tetrimino, indexColorGrid):
        for j in range(tetrimino.height):
            for i in range(tetrimino.width):
                if tetrimino.color_index_compare(i, j, indexColorGrid) == False:
                    self.table_color[tetrimino.position_x + i][tetrimino.position_y + j] = tetrimino.get_index(i, j)

    def collision_to_border_grid(self, tetrimino):
        if tetrimino.position_x < 0 or tetrimino.position_x + tetrimino.width >= self.number_row or \
                tetrimino.position_y + tetrimino.height >= self.number_line:
            return True
        return False

    def collision_to_Grid_Tetrimino(self, tetrimino, indexColorG):
        xr = 0
        yr = 0

        if tetrimino.position_x >= 0 and tetrimino.position_x + tetrimino.width <= self.number_row and \
                tetrimino.position_y + tetrimino.height <= self.number_line and tetrimino.position_y > 0:
            for j in range(tetrimino.height):
                if self.table_color[tetrimino.position_x][tetrimino.position_y + j] != indexColorG and \
                        tetrimino.color_index_compare(0, j, indexColorG) == False:
                    xr = -1
                    break
                if self.table_color[tetrimino.position_x + tetrimino.width - 1][tetrimino.position_y + j] != indexColorG and \
                        tetrimino.color_index_compare(tetrimino.width - 1, j, indexColorG) == False:
                    xr = 1
                    break
            for i in range(tetrimino.width):
                for j in range(tetrimino.height):
                    if self.table_color[tetrimino.position_x + i][tetrimino.position_y + j] != indexColorG and tetrimino.color_index_compare(i, j, indexColorG) == False:
                        yr = 1
                        return xr, yr
        return xr, yr

    def line_delete(self, indexColorG):
        newGrid = np.full((self.number_row, self.number_line), indexColorG)
        actualPosition = self.number_line - 1
        for j in range(self.number_line):
            for i in range(self.number_row):
                if self.table_color[i][self.number_line - j - 1] == indexColorG:
                    for k in range(self.number_row):
                        newGrid[k][actualPosition] = self.table_color[k][self.number_line - j - 1]
                    actualPosition -= 1
                    break
        del self.table_color
        self.table_color = copy.deepcopy(newGrid)
        del newGrid
