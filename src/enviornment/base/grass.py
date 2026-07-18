from src.utils.enums import EnviornmentalAttributes
from src.enviornment.base_env import EnviornmentBase, TopEnviornmentTypes, EnvTickType

class GrassEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(76, 175, 80), 
            hunger_restore=1, 
            thirst_restore=0,
            top_layers={
                EnviornmentalAttributes.hydration: {
                    EnvTickType.passive: [TopEnviornmentTypes.mud]
                },
                EnviornmentalAttributes.fertility: {
                    EnvTickType.active:[TopEnviornmentTypes.crop, TopEnviornmentTypes.tree]
                }
            }
        )

    