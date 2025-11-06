import cv2 as cv
import numpy as np

# ------------------- Import effects from here -------------------

from effects.color_chaos_manipulator import ColorChaosManipulator
from effects.tracker import Tracker
from effects.vhs import VHS

class EffectManager:

    def __init__(self):
        self.effects = {
            "tracker" : Tracker(),
            "cc_manipulator" : ColorChaosManipulator,
            "vhs" : VHS()
        }

        self.active_effect = None
        self.effect_history = []

    def set_effect(self, effect_name):
        if effect_name in self.effects:
            self.active_effect = self.effects[effect_name]
            self.effect_history.append(self.effects[effect_name])

            return True
        else:
            print("Couldn't find effect!")
            return False
        
    def process_frame(self, frame, complexity):
        if self.active_effect:
            return self.active_effect.process_current_frame(frame, complexity)
        return frame
    
    def get_active_effect(self):
        return self.active_effect