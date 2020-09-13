# https://youtu.be/_1UMXx39Jxk?t=136
from abc import abstractmethod, ABC, abstractproperty
from typing import List


class MemoryOwnerMixin(ABC):
    @abstractproperty
    @property
    def memory_start_location(self) -> int:
        pass

    @abstractproperty
    @property
    def memory_end_location(self) -> int:
        pass

    @abstractmethod
    def get_memory(self) -> List[int]:
        pass

    def get(self, position: int) -> int:
        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int):
        self.get_memory()[position - self.memory_start_location] = value
