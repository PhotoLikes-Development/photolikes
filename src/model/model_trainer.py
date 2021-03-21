from abc import ABC, abstractmethod
from os import PathLike
from typing import Union


class ModelTrainer(ABC):
    @abstractmethod
    def train_model(self):
        ...

    @abstractmethod
    def update_saved_model(self, target_path: Union[PathLike, str]):
        ...
