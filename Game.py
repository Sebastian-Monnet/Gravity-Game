from EngineClass import *
from DisplayClass import *
import pygame

Paused = False

ensemble = Ensemble(np.array([[900], [700]]))
display = Display(ensemble)
engine = Engine(ensemble)

ensemble.populate(20)

display.draw_ensemble()

while not engine.get_game_over():
    if Paused:
        continue
    else:
        engine.tick()
        display.draw_ensemble()
