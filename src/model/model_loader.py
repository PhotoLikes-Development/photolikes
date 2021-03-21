from abc import ABC, abstractmethod

from tensorflow.python.keras.models import Model


class ModelLoader(ABC):
    @abstractmethod
    def get_instance(self) -> Model:
        ...

    @abstractmethod
    def tensorflow_warmup(self):
        """ A method to preload tensorflow beforehand (on app startup, for example), not on first model request """
        ...
