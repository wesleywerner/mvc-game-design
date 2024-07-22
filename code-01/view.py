"""
View
"""

import pygame
import eventmanager as evmgr

class GraphicalView:
    """
    Draws the model state onto the screen.
    """

    def __init__(self, ev_manager, model):
        """
        ev_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, evmgr.InitializeEvent):
            self.initialize()
        elif isinstance(event, evmgr.QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, evmgr.TickEvent):
            self.renderall()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

    def renderall(self):
        """
        Draw the current game state on screen.
        Does nothing if isinitialized == False (pygame.init failed)
        """

        if not self.isinitialized:
            return
        # clear display
        self.screen.fill((0, 0, 0))
        # draw some words on the screen
        somewords = self.smallfont.render(
                    'The View is busy drawing on your screen',
                    True,
                    (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        # flip the display to show whatever we drew
        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((600, 60))
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True
