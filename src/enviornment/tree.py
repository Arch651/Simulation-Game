from src.enviornment.base import BaseEnviornment

class TreeEnviornment(BaseEnviornment):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(34, 139, 34), 
            hunger_restore=0, 
            thirst_restore=0
        )