# This file will store that class that handles the processing of all the entity actions
# This class will be responsible for just managing the entity action calls
# the entity class will store the overall logic for what to do
import random


from src.manager.entity import EntityTracker
from src.utils.enums import EntityFoodType, EntityActions

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

    
    def queue_voluntary_action(self):
        # in this phase all the entites will be given a chance to queue an action
        for entity_food_type, entities in self.entity_tracker.entity_objects.items():
            for identifier,entity in entities.items():
                action_decided = entity.decide_action()

                if action_decided:
                    self.entity_action_list.append(
                        (entity_food_type,identifier)
                    )

    def process_passive_actions(self):
        # for all the entities in the world call its passive action
        for entities in self.entity_tracker.entity_objects.values():
            for _,entity in entities.items():
                entity.passive_action()

    
    def process_voluntary_actions(self):
        # in order to make sure no entity gets an advantage due to spawing before
        # before processing the actions, we will shuffle the list

        random.shuffle(self.entity_action_list)
        
        for entity_details in self.entity_action_list:
            entity_instance = self.entity_tracker.get_entity_instance(
                entity_food_type=entity_details[0],
                identifier=entity_details[1]
            )

            if entity_instance != None:
                # if the entity is still present we will perform its queued action
                # if it is not idle
                if entity_instance.current_action != EntityActions.idle:
                    entity_instance.perform_action()
        
        # once all the action are completed, we will set the list to an empty state
        self.entity_action_list = []

