
from abc import ABC, abstractmethod
from typing import Any, Optional

class ANode(ABC):
    def __init__(self, data: Optional[Any] = None) -> None:
        self._data: Optional[Any] = data
        self._right: Optional["ANode"] = None


    @abstractmethod
    def get_right(self):
        pass
    @abstractmethod
    def get_data(self):
        pass
    @abstractmethod
    def set(self, data):
        pass
    @abstractmethod
    def set_right(self, node):
        pass

