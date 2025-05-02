from TerminalNode import TerminalNode

BooleanOperators = dict(Leftparen=" ( ",
                        Rightparen=" ( ",
                        NotOperator=" not ",
                        AndOperator=" and ",
                        OrOperator=" or ",
                        XorOperator=" ^ ",
                        ImplicationOperator=" impl ",
                        ConsequenceOperator=" cons ",
                        EquivalentOperator=" eq ",
                        NotEquivalentOperator=" neq ")

class OpNode(TerminalNode):
    def __init__(self, op):
        super().__init__()
        self._op = op
        self._lexeme = BooleanOperators[self._op]

    def get_copy(self):
        return OpNode(self._op)
