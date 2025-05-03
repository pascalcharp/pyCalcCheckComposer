from BooleanExpression.Node.NonTerminalNode import NonTerminalNode


class ENode(NonTerminalNode):
    def __init__(self):
        super().__init__()


    def get_copy(self):
        copied_node = ENode()
        for child in self._children:
            copied_node.add_child(child.get_copy())
        return copied_node

    def __str__(self):
        return "E"
