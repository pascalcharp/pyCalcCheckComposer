from abc import ABC

from BooleanExpression.Node.BasicNode import BasicNode


class NonTerminalNode(BasicNode, ABC):
    def __init__(self):
        super().__init__()
        self._children = []

    def get_children(self):
        return self._children

    def add_children(self, children):
        self._children.extend(children)

    def add_child(self, child):
        self._children.append(child)

    def clear_children(self):
        self._children = []

    def has_children(self):
        return len(self._children) > 0

