from abc import ABC, abstractmethod

class AnimalState(ABC):
    @abstractmethod
    def get_animal_type(self):
        pass

class UnicornState(AnimalState):
    def get_animal_type(self):
        return "Unicorn"

class PandaState(AnimalState):
    def get_animal_type(self):
        return "Panda"