from src.enviornment.base_env import EnviornmentBase

class MarshEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(74, 93, 63), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={}
        )