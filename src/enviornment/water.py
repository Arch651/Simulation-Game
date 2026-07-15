from src.enviornment.base import BaseEnviornment

class WaterEnviornment(BaseEnviornment):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(64, 164, 223), 
            hunger_restore=0, 
            thirst_restore=5
        )