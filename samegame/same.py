#!/bin/env python3
"""
This is the Same Game
"""
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
#
# This code demonstrates the mvc pattern for making games.
# It lives at https://github.com/wesleywerner/mvc-game-design

import same_model
import same_view
import same_controller

if __name__ == "__main__":
    COLUMNS = 20
    ROWS = 20
    NUM_VALUES = [1, 2, 3]
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 300

    model = same_model.Same_M(COLUMNS, ROWS, NUM_VALUES, 1)
    view = same_view.Same_V(SCREEN_WIDTH, SCREEN_HEIGHT, model)
    controller = same_controller.Same_C(model, view)
    view.redraw()

    while controller.running:
        controller.process_input()
        view.blit()
