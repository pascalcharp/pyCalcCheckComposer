from PyQt6.QtWidgets import QMessageBox
from BooleanExpression.ExpressionTree import BooleanExpressionTree
from gui.ExpressionWidget import ExpressionWidget


class ProofController:
    def __init__(self, proof_window):
        """
        Initialise le contrôleur pour gérer la logique et les interactions
        entre la vue (ProofWindow) et les modèles (BooleanExpressionTree).
        """
        self.proof_window = proof_window  # Référence à la vue
        self.proofs = []  # Liste des modèles (BooleanExpressionTree)

    def add_new_expression(self):
        """
        Crée un nouvel arbre logique (modèle) et un widget associé (vue), puis les connecte.
        """
        # Créer un nouveau modèle (arbre logique)
        new_expression_tree = BooleanExpressionTree()

        # Ajouter à la liste des preuves
        self.proofs.append(new_expression_tree)

        # Créer un widget pour affichage/modification
        expression_index = len(self.proofs) - 1
        new_expression_widget = ExpressionWidget(new_expression_tree, self.proof_window, expression_index)

        # Ajouter le widget à la fenêtre
        self.proof_window.add_expression_widget(new_expression_widget)

    def expand_node(self, expression_index, node_id):
        """
        Demande au modèle d'expandre le nœud d'une expression donnée.

        :param expression_index: Index de l'expression (BooleanExpressionTree) dans la liste.
        :param node_id: ID du nœud à expandre.
        """
        # Récupérer l'arbre logique correspondant
        expression_tree = self.proofs[expression_index]

        try:
            # Demander au modèle d'expandre le nœud
            expression_tree.generate_binary_operator_production(node_id, "AndOperator")

            # Demander à la vue de rafraîchir le widget
            self.proof_window.update_expression_widget(expression_index)

        except Exception as e:
            QMessageBox.critical(self.proof_window, "Erreur", f"Impossible d'expandre le nœud : {e}")
