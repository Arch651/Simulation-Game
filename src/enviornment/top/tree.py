from src.enviornment.base_env import EnviornmentBase

class TreeEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(34, 139, 34), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={}
        )