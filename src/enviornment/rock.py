from src.enviornment.base import BaseEnviornment

class RockEnviornment(BaseEnviornment):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(128, 128, 128), 
            hunger_restore=0, 
            thirst_restore=0
        )