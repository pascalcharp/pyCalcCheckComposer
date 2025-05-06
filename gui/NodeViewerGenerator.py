from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.IdNode import IdNode
from BooleanExpression.Node.OpNode import OpNode

from gui.ENodeViewer import ENodeViewer
from gui.IdNodeViewer import IdNodeViewer
from gui.OpNodeViewer import OpNodeViewer

class NodeViewerGenerator:

    @staticmethod
    def getNodeViewer(node, parent):
        if isinstance(node, ENode):
            return ENodeViewer(node, parent)
        if isinstance(node, IdNode):
            return IdNodeViewer(node, parent)
        if isinstance(node, OpNode):
            return OpNodeViewer(node, parent)