import pygame
import eventmanager as evmgr
from model import STATE_MENU, STATE_HELP, STATE_PLAY

class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, ev_manager, model):
        """
        ev_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, evmgr.TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for pgev in pygame.event.get():
                # handle window manager closing our window
                if pgev.type == pygame.QUIT:
                    self.ev_manager.post(evmgr.QuitEvent())
                    # The GraphicalView calls pygame.quit() upon
                    # receiving the QuitEvent. We shouldn't return to
                    # the top of the loop here. `pygame.event` might be
                    # undefined.
                    break
                # handle key down events
                if pgev.type == pygame.KEYDOWN:
                    if pgev.key == pygame.K_ESCAPE:
                        self.ev_manager.post(evmgr.StateChangeEvent(None))
                        break
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == STATE_MENU:
                            self.keydownmenu(pgev)
                        if currentstate == STATE_PLAY:
                            self.keydownplay(pgev)
                        if currentstate == STATE_HELP:
                            self.keydownhelp(pgev)

    def keydownmenu(self, event):
        """
        Handles menu key events.
        """

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.ev_manager.post(evmgr.StateChangeEvent(None))
        # space plays the game
        if event.key == pygame.K_SPACE:
            self.ev_manager.post(evmgr.StateChangeEvent(STATE_PLAY))

    def keydownhelp(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.ev_manager.post(evmgr.StateChangeEvent(None))

    def keydownplay(self, event):
        """
        Handles play key events.
        """

        if event.key == pygame.K_ESCAPE:
            self.ev_manager.post(evmgr.StateChangeEvent(None))
        # F1 shows the help
        if event.key == pygame.K_F1:
            self.ev_manager.post(evmgr.StateChangeEvent(STATE_HELP))
        else:
            self.ev_manager.post(evmgr.InputEvent(event.unicode, None))
