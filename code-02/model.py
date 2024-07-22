import eventmanager as evmgr

class GameEngine(object):
    """
    Tracks the game state.
    """

    def __init__(self, ev_manager):
        """
        ev_manager (EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, evmgr.QuitEvent):
            self.running = False
        if isinstance(event, evmgr.StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.ev_manager.post(evmgr.QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.ev_manager.post(evmgr.InitializeEvent())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = evmgr.TickEvent()
            self.ev_manager.post(newTick)


# State machine constants for the StateMachine class below
STATE_INTRO = 1
STATE_MENU = 2
STATE_HELP = 3
STATE_ABOUT = 4
STATE_PLAY = 5

class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """

    def __init__ (self):
        self.statestack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.statestack.append(state)
        return state
