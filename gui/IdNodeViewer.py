from BooleanExpression.Node.IdNode import IdNode
from gui.NodeViewer import NodeViewer

class IdNodeViewer(NodeViewer):
    def __init__(self, idnode, parent=None):
        assert (isinstance(idnode, IdNode))
        super().__init__(idnode, parent)



    def _configure(self):
        super()._configure()

    def _onClicked(self):
        super()._onClicked()
        print("IdNodeViewer::_onClicked")

