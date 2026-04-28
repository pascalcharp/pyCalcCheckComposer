from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

from gui.NodeButton import NodeButton

class ExpressionWidget(QWidget):
    def __init__(self, expression_tree, proof_window, expression_index):
        """
        Initialise un widget pour une expression logique et une fenêtre associée.

        :param expression_tree: Instance de BooleanExpressionTree.
        :param proof_window: Référence à la ProofWindow pour communication.
        :param expression_index: Index de l'expression dans la liste (ProofController).
        """
        super().__init__()
        self.tree = expression_tree  # L'arbre logique
        self.proof_window = proof_window  # Référence à la ProofWindow
        self.expression_index = expression_index  # Index dans ProofController

        # Layout horizontal pour les noeuds de l'expression
        self.node_layout = QHBoxLayout()

        # Afficher les noeuds de l'expression
        self.render_expression()

        # Ajouter le layout horizontal au widget
        self.setLayout(self.node_layout)

    def render_expression(self):
        """
        Reconstruit l'affichage graphique de l'arbre logique dans ce widget,
        chaque noeud est disposé horizontalement.
        """
        # Nettoyer les nodes existants (avant affichage ou modification)
        for i in reversed(range(self.node_layout.count())):
            self.node_layout.itemAt(i).widget().deleteLater()

        # Obtenir tous les noeuds de l'expression
        expression_nodes = self.tree.get_expression()

        # Ajouter chaque noeud à la disposition horizontale
        for node in expression_nodes:
            if isinstance(node, str):  # Si le node est un opérateur ou une parenthèse
                button = QPushButton(node)
                button.setFixedSize(40, 40)
                button.setEnabled(False)  # Non cliquable
            else:  # Si c'est un Enode
                button = NodeButton(
                    node_id=node.node_id,
                    text="E",  # Texte affiché pour chaque Enode
                    on_click=self.display_popup_to_expand  # Action effectuée si on clique dessus
                )

            self.node_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def display_popup_to_expand(self, node_id):
        """
        Affiche une fenêtre de dialogue pour demander l'expansion d'un noeud spécifique.

        :param node_id: ID du noeud à modifier.
        """
        result = QMessageBox.question(
            self,
            "Expansion du nœud",
            "Voulez-vous expandre ce nœud en 'E AND E' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if result == QMessageBox.StandardButton.Yes:
            # Notifier le contrôleur pour effectuer l'expansion
            self.proof_window.controller.expand_node(self.expression_index, node_id)

            # Rafraîchir l'affichage après modification
            self.render_expression()

    def modify_expression(self):
        """
        Méthode préservée (optionnel) mais non utilisée directement dans la nouvelle structure.
        """
        try:
            root_id = self.tree.get_root_id()
            self.tree.generate_binary_operator_production(root_id, "AndOperator")
            print("Expression modifiée :", self.tree)
        except KeyError as e:
            print(f"Erreur : Opérateur inexistant dans BooleanOperators ({e})")
        except Exception as e:
            print("Erreur lors de la modification de l'expression :", e)
