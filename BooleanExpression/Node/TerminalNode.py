from BooleanExpression.Node.BasicNode import BasicNode


class TerminalNode(BasicNode):
    def __init__(self):
        super().__init__()
        self._lexeme = ""

    def has_children(self):
        return False

    def __str__(self):
        return self._lexeme