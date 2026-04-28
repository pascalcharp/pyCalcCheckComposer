from gui.NodeViewer import NodeViewer


class OpNodeViewer(NodeViewer):
    def __init__(self, opnode, parent=None):
        super().__init__(opnode, parent)
        self._configure()


    def _configure(self):
        super()._configure()

    def onClicked(self):
        super().onClicked()
        print("OpNodeViewer::_onClicked")
