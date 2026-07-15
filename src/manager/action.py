# This file will store that class that handles the processing of all the entity actions
# This class will be responsible for just managing the entity action calls
# the entity class will store the overall logic for what to do

from src.manager.entity import EntityTracker
from src.utils.enums import EntityFoodType

class EntityAction:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        entity_tracker: EntityTracker
    ):
        
        if self._initialized:
            return 
        
        self.entity_tracker: EntityTracker = entity_tracker
        self.entity_action_list: list[tuple[EntityFoodType | str]] = []

    
    def queue_action(self):
        # in this phase all the entites will be given a chance to queue an action
        for entity_food_type, entities in self.entity_tracker.entity_objects.items():
            if len(entities) == 0:
                continue

            for identifier,entity in entities.items():
                action_decided = entity.decide_action()

                if action_decided:
                    self.entity_action_list.append(
                        (entity_food_type,identifier)
                    )
    
    def process_actions(self):
        for entity_details in self.entity_action_list:
            entity_instance = self.entity_tracker.get_entity_instance(
                entity_food_type=entity_details[0],
                identifier=entity_details[1]
            )

            entity_instance.perform_action()
        
        # once all the action are completed, we will set the list to an empty state
        self.entity_action_list = []

