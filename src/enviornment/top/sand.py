from src.enviornment.base_env import EnviornmentBase

class SandEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(238, 214, 175), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={}
        )