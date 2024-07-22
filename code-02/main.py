import eventmanager
import model
import view
import controller

def run():
    ev_manager = eventmanager.EventManager()
    gamemodel = model.GameEngine(ev_manager)
    keyboard = controller.Keyboard(ev_manager, gamemodel)
    graphics = view.GraphicalView(ev_manager, gamemodel)
    gamemodel.run()

if __name__ == '__main__':
    run()
