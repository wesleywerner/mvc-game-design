#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import pygame
from pygame.locals import *
from same_model import Same_M

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
PURPLE = (220, 0, 220)
COLORS = (BLACK, PURPLE, GREEN, BLUE)

BG_COLOR = BLACK
SELECTION_COLOR = WHITE


class Same_V(object):
    def __init__(self, pixel_width, pixel_height, model):

        # we may observe the model
        self.model = model

        # listen for model events
        model.register_listener(self.model_event)

        # calculate each block size, and set our viewport size.
        self.screen_size = pixel_width, pixel_height
        self.block_size = pixel_width / model.cols

        # keep a matrix of selected blocks
        self.selection = None

        # init pygame
        pygame.init()
        pygame.display.set_caption('same game')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # draw game widgets on a surface to blit on screen
        # so we dont re-loop inside the screen update.
        self.game_surf = pygame.Surface(self.screen_size)
        self.game_surf.set_colorkey(TRANSPARENT)

        # draw selection regions on a surface to blit, too.
        self.select_surf = pygame.Surface(self.screen_size)
        self.select_surf.set_colorkey(TRANSPARENT)

    def __draw_blocks(self):
        # clear the game surface.
        # possibly use transparency color later.
        self.game_surf.fill(TRANSPARENT)
        # use a local variable to make reading easier
        mx = self.model.matrix

        for j in range(len(mx)):
            for k in range(len(mx[j])):
                value = mx[j][k]
                if value:
                    # create a square matching size and position of our screen
                    block_rect = pygame.Rect(k * self.block_size,
                        j * self.block_size,
                        self.block_size, self.block_size)
                    # fill this square with a border. it looks selected.
                    self.game_surf.fill(COLORS[value], block_rect)

    def __draw_selection(self):
        self.select_surf.fill(TRANSPARENT)
        if not self.selection:
            return
        for j in range(len(self.selection)):
            for k in range(len(self.selection[j])):
                if self.selection[j][k]:
                    block_rect = pygame.Rect(k * self.block_size,
                        j * self.block_size,
                        self.block_size, self.block_size)
                    #pygame.draw.rect(self.select_surf, WHITE, block_rect, 4)
                    self.select_surf.fill(SELECTION_COLOR, block_rect)

    def convert_mousepos(self, pos):
        """ convert window (x, y) coords into game field (row, col) values. """
        return pos[1] / self.block_size, pos[0] / self.block_size

    def redraw(self):
        self.__draw_blocks()
        self.__draw_selection()

    def blit(self):
        # we blank the screen, we may draw a nice background later in time
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.game_surf, (0, 0))
        if self.selection:
            self.screen.blit(self.select_surf, (0, 0))
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    def model_event(self, event_name, data):
        if event_name == "drop_cell":
            # data = [[from x, y], [to x, y]]
            # draw each movement step for a basic drop animation.
            self.__draw_blocks()
            self.blit()

if __name__ == "__main__":
    model = Same_M(8, 8, [1, 2, 3], 1)
    view = Same_V(300, 300, model)
    view.redraw()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                row, col = view.convert_mousepos(event.pos)
                view.selection = model.get_neighbours(row, col)
                view.redraw()
        view.blit()
