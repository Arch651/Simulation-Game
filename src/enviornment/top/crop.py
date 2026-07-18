from src.enviornment.base_env import EnviornmentBase

class CropEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(237, 145, 33), 
            hunger_restore=2, 
            thirst_restore=0,
            top_layers={}
        )