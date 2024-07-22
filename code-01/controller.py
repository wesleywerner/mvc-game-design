"""
Controller
"""

import pygame
import eventmanager as evmgr

class Keyboard:
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
            for ev in pygame.event.get():
                # handle window manager closing our window
                if ev.type == pygame.QUIT:
                    self.ev_manager.post(evmgr.QuitEvent())
                    # The GraphicalView calls pygame.quit() upon
                    # receiving the QuitEvent. We shouldn't return to
                    # the top of the loop here. `pygame.event` might be
                    # undefined.
                    break
                # handle key down evs
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.ev_manager.post(evmgr.QuitEvent())
                        break
                    else:
                        # post any other keys to the message queue for everyone else to see
                        self.ev_manager.post(evmgr.InputEvent(ev.unicode, None))
