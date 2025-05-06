from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.IdNode import IdNode
from BooleanExpression.Node.OpNode import OpNode

from ENodeViewer import ENodeViewer
from IdNodeViewer import IdNodeViewer
from OpNodeViewer import OpNodeViewer

class NodeViewerGenerator:

    @staticmethod
    def getNodeViewer(node, parent):
        if isinstance(node, ENode):
            return ENodeViewer(node, parent)
        if isinstance(node, IdNode):
            return IdNodeViewer(node, parent)
        if isinstance(node, OpNode):
            return OpNodeViewer(node, parent)