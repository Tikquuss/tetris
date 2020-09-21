import copy
import numpy as np
import pygame
from pygame.locals import *
import random

from Utils import *

'''
    create a I tetriminos :     *
                                *
                                *
                                *
'''
def set_Tetrimino_I(color_index):
    TETRIMINO_TYPE = 1
    TETRIMINO = np.full((1, 4), color_index)
    return TETRIMINO
'''
    create a O tetriminos :     **
                                **
'''
def set_Tetrimino_O(color_index):
    TETRIMINO_TYPE = 2
    TETRIMINO = np.full((2, 2), color_index)
    return  TETRIMINO

'''
    create a T tetriminos :     ***
                                 *
'''
def set_Tetrimino_T(color_index, color_indexG):
    TETRIMINO_TYPE = 3
    TETRIMINO = np.full((3, 2), color_index)
    TETRIMINO[0][1] = color_indexG
    TETRIMINO[2][1] = color_indexG
    return TETRIMINO

'''
    create a L tetriminos :     *
                                *
                                **
'''
def set_Tetrimino_L(color_index, color_indexG):
    TETRIMINO_TYPE = 4
    TETRIMINO = np.full((2, 3), color_index)
    TETRIMINO[1][0] = color_indexG
    TETRIMINO[1][1] = color_indexG
    return TETRIMINO

'''
    create a J tetriminos :     *
                                *
                               **
'''
def set_Tetrimino_J(color_index, color_indexG):
    TETRIMINO_TYPE = 5
    TETRIMINO = np.full((2, 3), color_index)
    TETRIMINO[0][0] = color_indexG
    TETRIMINO[0][1] = color_indexG
    return TETRIMINO

'''
    create a Z tetriminos :     **
                                 **
'''
def set_Tetrimino_Z(color_index, color_indexG):
    TETRIMINO_TYPE = 6
    TETRIMINO = np.full((3, 2), color_index)
    TETRIMINO[2][0] = color_indexG
    TETRIMINO[0][1] = color_indexG
    return TETRIMINO

'''
    create a S tetriminos :     **
                               **
'''
def set_Tetrimino_S(color_index, color_indexG):
    TETRIMINO_TYPE = 7
    TETRIMINO = np.full((3, 2), color_index)
    TETRIMINO[0][0] = color_indexG
    TETRIMINO[2][1] = color_indexG
    return TETRIMINO

class Tetriminos:
    def __init__(self, type_t, xPosition, yPosition, indexColor, indexColorG):
        self.position_x = xPosition
        self.position_y = yPosition
        self.width = 0
        self.height = 0
        self.type = type_t
        self.tetrimino = np.full((self.width, self.height), indexColor)
        self.changeTetrimino(indexColorG, indexColor, self.type)

    def color_index_compare(self, index_i, index_j, index_color):
        return self.tetrimino[index_i][index_j] == index_color

    def get_index(self, i, j):
        return self.tetrimino[i][j]

    def randomChange(self, sizeIndex, indexColorG):
        self.type = random.randint(1, 7)
        color_index = random.randint(1, sizeIndex)
        self.changeTetrimino(indexColorG, color_index, self.type)

    def changeTetrimino(self, color_indexG, color_index, type):
        self.type = type
        del self.tetrimino
        if self.type == 5:
            self.tetrimino = set_Tetrimino_J(color_index, color_indexG)
        elif self.type == 2:
            self.tetrimino = set_Tetrimino_O(color_index)
        elif self.type == 3:
            self.tetrimino = set_Tetrimino_S(color_index, color_indexG)
        elif self.type == 4:
            self.tetrimino = set_Tetrimino_T(color_index, color_indexG)
        elif self.type == 6:
            self.tetrimino = set_Tetrimino_Z(color_index, color_indexG)
        elif self.type == 1:
            self.tetrimino = set_Tetrimino_I(color_index)
        elif self.type == 7:
            self.tetrimino = set_Tetrimino_L(color_index, color_indexG)
        self.width = self.tetrimino.shape[0]
        self.height = self.tetrimino.shape[1]

    def rotate_Tetrimino(self, xPosition, yPosition):
        if self.tetrimino.shape[1] != self.tetrimino.shape[0]:
            newTetrimino = np.full((self.tetrimino.shape[1], self.tetrimino.shape[0]), self.tetrimino[0][0])
            for i in range(self.tetrimino.shape[0]):
                for j in range(self.tetrimino.shape[1]):
                    newTetrimino[j][self.tetrimino.shape[0] - i - 1] = self.tetrimino[i][j]
            del self.tetrimino
            self.tetrimino = copy.deepcopy(newTetrimino)
            del newTetrimino
        self.width = self.tetrimino.shape[0]
        self.height = self.tetrimino.shape[1]

    def drawTetrimino(self, screen_draw, gridPalette, colorIndexG, sizeBlock, grid):
        for j in range(self.tetrimino.shape[1]):
            for i in range(self.tetrimino.shape[0]):
                if self.tetrimino[i][j] != colorIndexG:
                    pygame.draw.rect(screen_draw, gridPalette[self.tetrimino[i][j]],
                                     Rect(grid.position_x + (self.position_x + i) * sizeBlock,
                                          grid.position_y + (self.position_y + j) * sizeBlock, sizeBlock, sizeBlock))

    def copyTetrimino(self, otherTetrimino):
        del self.tetrimino
        self.tetrimino = copy.deepcopy(otherTetrimino.tetrimino)
        self.width = self.tetrimino.shape[0]
        self.height = self.tetrimino.shape[1]

    def set_position(self, xposition, yposition):
        self.position_x = xposition
        self.position_y = yposition

    def limiteBoundari(self, xLimite, yLimite, W_limite, H_limite):
        updateTetrimino = False
        if self.position_x < xLimite :
            self.position_x = xLimite
        elif self.position_x + self.tetrimino.shape[0] >= W_limite :
            self.position_x = W_limite - self.tetrimino.shape[0]

        if self.position_y + self.tetrimino.shape[1] >= NBR_LINE:
            self.position_y = H_limite - self.tetrimino.shape[1]
            updateTetrimino = True
        return  updateTetrimino

class Player(Tetriminos):
    def __init__(self, type_t, xPosition, yPosition, indexColor, indexColorG):
        super(Player, self).__init__(type_t, xPosition, yPosition, indexColor, indexColorG)

    def eventTick(self, event):
        userAction2 = False
        userAction = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.position_x += -1
                userAction2 = True
            elif event.key == pygame.K_RIGHT:
                self.position_x += 1
                userAction2 = True
            elif event.key == pygame.K_DOWN:
                self.position_y += 1
                userAction = True
            elif event.key == pygame.K_UP:
                self.rotate_Tetrimino(0,0)
        return  userAction, userAction2

class IA_Tetriminos(Tetriminos):
    def __init__(self, type_t, xPosition, yPosition, indexColor, indexColorG, grid):
        super(IA_Tetriminos, self).__init__(type_t, xPosition, yPosition, indexColor, indexColorG)
        self.grid_game = grid
    def eventTick(self, event):
        return 0