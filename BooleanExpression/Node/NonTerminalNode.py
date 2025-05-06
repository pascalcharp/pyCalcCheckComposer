from abc import ABC

from BooleanExpression.Node.BasicNode import BasicNode


class NonTerminalNode(BasicNode, ABC):
    """
    Classe abstraite servant à représenter une variable non-terminale dans un arbre syntaxique utilisant une grammaire
    non contextuelle.

    Attributs
    ---------
    _children: Liste des sommets enfants dans l'arbre.

    Méthodes
    --------
    get_children(): retourne la liste des enfants

    add_children(): rajoute à la liste actuelle une liste d'enfants additionnels

    add_child(): rajoute à la liste des enfants un enfant supplémentaire

    clear_children(): vide la liste des enfants

    has_children(): retourne True si la liste des enfants contient au-moins un enfant.
    """

    def __init__(self):
        super().__init__()
        self._children = []

    def get_children(self):
        return self._children

    def add_children(self, children):
        self._children.extend(children)

    def add_child(self, child):
        self._children.append(child)

    def clear_children(self):
        self._children = []

    def has_children(self):
        return len(self._children) > 0

