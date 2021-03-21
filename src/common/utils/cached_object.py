import logging
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

TObject = TypeVar("TObject")


class CachedObject(Generic[TObject], ABC):
    __cache: Optional[TObject] = None

    @abstractmethod
    def load(self) -> TObject:
        """ Loads the object and returns it """
        ...

    # noinspection PyMethodMayBeStatic
    def is_reload_needed(self) -> bool:
        # use the first loaded object forever by default
        return False

    @property
    def instance(self):
        if self.__cache is None or self.is_reload_needed():
            logging.info(f"{self.__class__.__name__} is reloading. Old: {self.__cache}.")
            self.__cache = self.load()

        return self.__cache
