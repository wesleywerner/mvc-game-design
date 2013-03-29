import pygame
import model
from eventmanager import *

class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.Post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.Post(StateChangeEvent(None))
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == model.STATE_MENU:
                            self.keydownmenu(event)
                        if currentstate == model.STATE_PLAY:
                            self.keydownplay(event)
                        if currentstate == model.STATE_HELP:
                            self.keydownhelp(event)

    def keydownmenu(self, event):
        """
        Handles menu key events.
        """
        
        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        # space plays the game
        if event.key == pygame.K_SPACE:
            self.evManager.Post(StateChangeEvent(model.STATE_PLAY))
    
    def keydownhelp(self, event):
        """
        Handles help key events.
        """
        
        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.evManager.Post(StateChangeEvent(None))
    
    def keydownplay(self, event):
        """
        Handles play key events.
        """

        if event.key == pygame.K_ESCAPE:
            self.evManager.Post(StateChangeEvent(None))
        # F1 shows the help
        if event.key == pygame.K_F1:    
            self.evManager.Post(StateChangeEvent(model.STATE_HELP))
        else:
            self.evManager.Post(InputEvent(event.unicode, None))
