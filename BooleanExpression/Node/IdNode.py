from BooleanExpression.Node.TerminalNode import TerminalNode

class IdNode(TerminalNode):

    def __init__(self, name):
        super().__init__()
        self._lexeme = name

    def substitute_lexeme(self, new_name):
        self._lexeme = new_name

    def get_copy(self):
        return IdNode(self._lexeme)