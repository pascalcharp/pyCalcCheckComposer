from BooleanExpression.Node.TerminalNode import TerminalNode

BooleanOperators = dict(Leftparen=" ( ",
                        Rightparen=" ) ",
                        NotOperator=" ¬ ",
                        AndOperator=" ∧ ",
                        OrOperator=" ∨ ",
                        XorOperator=" ⊕ ",
                        ImplicationOperator=" ⇒ ",
                        ConsequenceOperator=" ⇐ ",
                        EquivalentOperator=" ≡ ",
                        NotEquivalentOperator=" ≢ ")

class OpNode(TerminalNode):
    def __init__(self, op):
        super().__init__()
        self._op = op
        self._lexeme = BooleanOperators[self._op]

    @property
    def op_key(self):
        return self._op

    def substitute_operator(self, new_op):
        self._op = new_op
        self._lexeme = BooleanOperators[new_op]

    def get_copy(self):
        return OpNode(self._op)
