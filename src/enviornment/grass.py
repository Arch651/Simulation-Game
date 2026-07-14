from src.enviornment.base import BaseEnviornment

class GrassEnviornment(BaseEnviornment):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(76, 175, 80), 
            hunger_restore=1, 
            thirst_restore=0
        )