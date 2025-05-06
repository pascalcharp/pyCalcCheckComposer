from BooleanExpression.Node.ENode import ENode
from gui.NodeViewer import NodeViewer



class ENodeViewer(NodeViewer):
    def __init__(self, enode, parent=None):
        assert(isinstance(enode, ENode))
        super().__init__(enode, parent)


    def _configure(self):
        super()._configure()


    def _onClicked(self):
        super()._onClicked()
        print("ENodeViewer clicked")


