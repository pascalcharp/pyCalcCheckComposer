# Journal de développement — pyCalcCheckComposer

## Étape 2 — Classe de base `NodeWidget` *(2026-05-05)*

**Objectif :** Définir le contrat commun à tous les widgets de nœuds (modes Display/Input, signaux) sans aucune dépendance au modèle.

### Fichiers créés

#### `gui/NodeWidget.py`
- `NodeWidget(QWidget)` — classe abstraite avec `QStackedWidget` interne.
- `enter_display_mode()` / `enter_input_mode()` / `is_in_input_mode()` — gestion des modes.
- `_request_input_mode()` — émet `input_mode_requested(self)` ; appelé par le bouton Display de la sous-classe.
- `_commit_action(action, payload=None)` — émet `action_committed(action, payload)` puis revient en Display.
- Sous-classes doivent implémenter `_build_display_widget()` et `_build_input_widget()`.

#### `tests/gui/NodeWidgetTests.py`
9 tests répartis en 2 classes :
- `NodeWidgetModeTests` — état initial, bascule Display↔Input, stockage du `node_id`
- `NodeWidgetSignalTests` — émission de `input_mode_requested`, `action_committed`, payload None, retour automatique en Display, indépendance des signaux

### Résultat des tests
```
Ran 9 tests — OK
```

---

## Étape 1 — Extensions du modèle *(2026-05-05)*

**Objectif :** Préparer le modèle pour supporter les nouvelles interactions (changer d'opérateur, revenir à un ENode) sans toucher à la GUI.

### Fichiers modifiés

#### `BooleanExpression/Node/OpNode.py`
- Ajout de `substitute_operator(new_op)` : change l'opérateur et le lexème d'un `OpNode` en place, à l'image de `IdNode.substitute_lexeme`.

#### `BooleanExpression/ExpressionTree.py`
- Ajout du dict `_parents` (maintenu dans toutes les méthodes `generate_*` et nettoyé dans `aux_collapse_node`).
- Les `OpNode` sont désormais enregistrés dans `_nodes` — ils ne l'étaient pas, ce qui empêchait de les retrouver par ID.
- Ajout de `get_parent_id(node_id)` : retourne l'ID du nœud parent.
- Ajout de `change_operator(op_node_id, new_op)` : délègue à `OpNode.substitute_operator`.
- Ajout de `revert_id_to_enode(id_node_id)` : retrouve le parent ENode via `_parents` et appelle `collapse_node`.

### Fichiers créés

#### `tests/BooleanExpressionTests/ModelExtensionsTests.py`
15 nouveaux tests répartis en 4 classes :
- `OpNodeSubstituteOperatorTests` — substitution d'opérateur, isolation entre instances, opérateur invalide
- `ParentTrackingTests` — tracking du parent pour toutes les productions (id, binaire, unaire, parenthèses), absence de parent pour la racine
- `ChangeOperatorTests` — changement d'opérateur et préservation de la structure de l'expression
- `RevertIdToEnodeTests` — retour à ENode, ré-expansion possible, nettoyage de `_nodes` et `_parents`

### Résultat des tests
```
Ran 19 tests in 0.001s — OK
```
(4 anciens + 15 nouveaux)
