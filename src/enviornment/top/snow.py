from src.enviornment.base_env import EnviornmentBase

class SnowEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(245, 248, 250), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={}
        )