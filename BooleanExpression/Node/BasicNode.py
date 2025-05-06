from abc import abstractmethod
from uuid import uuid4

class BasicNode:
    """
    Classe abstraite modélisant un sommet d'un arbre syntaxique qui représente une expression booléenne.

    Attributs
    ---------
    _uuid: Objet UUID immuable et unique identifiant le sommet

    Méthodes
    --------
    node_id: Retourne l'identifiant unique

    get_copy(): Retourne une copie de l'objet courant

    has_children: Retourne False si l'objet courant est une feuille de l'arbre (n'a pas d'enfant)
    """

    def __init__(self):
        self._uuid = uuid4()

    @property
    def node_id(self):
        return self._uuid

    @abstractmethod
    def get_copy(self):
        pass

    @abstractmethod
    def has_children(self):
        pass