from abc import abstractmethod
from uuid import uuid4


class BasicNode:
    def __init__(self):
        self._uuid = uuid4()

    @property
    def node_id(self):
        return self._uuid

    @abstractmethod
    def get_copy(self):
        pass

    @abstractmethod
    def has_children(self):
        pass