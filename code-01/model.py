"""
Model
"""
import eventmanager as evmgr

class GameEngine:
    """
    Tracks the game state.
    """

    def __init__(self, ev_manager):
        """
        ev_manager(EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.running = False

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, evmgr.QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.ev_manager.post(evmgr.InitializeEvent())
        while self.running:
            new_tick = evmgr.TickEvent()
            self.ev_manager.post(new_tick)
