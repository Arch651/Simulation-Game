from src.enviornment.base_env import EnviornmentBase

class MudEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(70, 55, 42), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={}
        )