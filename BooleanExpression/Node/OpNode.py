from BooleanExpression.Node.TerminalNode import TerminalNode

BooleanOperators = dict(Leftparen=" ( ",
                        Rightparen=" ) ",
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

    def substitute_operator(self, new_op):
        self._op = new_op
        self._lexeme = BooleanOperators[new_op]

    def get_copy(self):
        return OpNode(self._op)
