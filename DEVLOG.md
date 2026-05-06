# Journal de développement — pyCalcCheckComposer

## Étape 8 — Nettoyage *(2026-05-05)*

**Objectif :** Supprimer tout le code devenu mort après les étapes précédentes.

### Fichiers supprimés
- `gui/ExpandNodeDialog.py`
- `gui/NodeButton.py`

### Fichiers modifiés

#### `gui/ExpressionWidget.py`
- Suppression des imports `ExpandNodeDialog`, `NodeButton`, `QPushButton` (inutilisé).
- Suppression des méthodes legacy `display_popup_to_expand` et `modify_expression`.

#### `gui/GuiConstants.py`
- Suppression de toutes les constantes devenues inutilisées : `COLOR_NODE_BUTTON_*`, `DIALOG_*`, `BUTTON_WIDTH/HEIGHT`, `CANCEL_BUTTON_TEXT`, `GRID_COLUMNS`, `GRID_BUTTON_MAX`, `BUTTON_OPERATOR_*`, `BUTTON_OPACITY_DISABLED`, `NODE_BUTTON_TEXT`, `NODE_ALIGNMENT`, `STYLE_BUTTON_NODE*`, `SPACER_*_POLICY`.
- Ne conserve que les 13 constantes utilisées par `ProofWindow`.

### Vérification
```
grep sur tout le projet (hors poubelle/) — 0 référence cassée
```

---

## Étapes 6 & 7 — `ExpressionWidget` + `ProofController` *(2026-05-05)*

**Objectif :** Brancher les nouveaux widgets dans l'expression, gérer un seul nœud en mode Input à la fois, et router les actions vers le contrôleur.

### Fichiers modifiés

#### `BooleanExpression/Node/OpNode.py`
- Ajout de la propriété `op_key` — expose `_op` en lecture pour `ExpressionWidget`.

#### `gui/ExpressionWidget.py`
- `render_expression()` réécrit : utilise `takeAt()` au lieu de `deleteLater()` seul (correction d'un bug où les anciens widgets restaient dans le layout) ; instancie `ENodeWidget`, `OpNodeWidget` ou `IdNodeWidget` selon le type du nœud.
- `_create_node_widget(node)` — factory privée.
- `_on_input_mode_requested(widget)` — ferme le widget précédemment ouvert, ouvre le demandeur ; gère l'invariant "un seul en mode Input".
- `_on_action_committed(widget, action, payload)` — dispatch vers la bonne méthode du contrôleur via `if/elif`.
- Méthodes legacy (`display_popup_to_expand`, `modify_expression`) conservées pour l'étape 8.

#### `controllers/ProofController.py`
- Refactorisé avec `_refresh(expression_index, operation)` — centralise le try/except + `update_expression_widget`.
- `expand_node` mis à jour : gère maintenant tous les opérateurs binaires (plus seulement And/Or).
- Ajout de `convert_to_id`, `change_operator`, `rename_id`, `revert_to_enode`.

### Fichiers créés

#### `tests/gui/ExpressionWidgetTests.py`
18 tests en 3 classes :
- `ExpressionWidgetRenderTests` — types de widgets créés (ENode, OpNode, IdNode), texte affiché, re-rendu
- `ExpressionWidgetInputModeTests` — invariant "un seul actif", tracking de `_active_node_widget`, nettoyage au re-rendu
- `ExpressionWidgetRoutingTests` — chaque action (`expand`, `to_id`, `change_op`, `rename`, `revert`) appellée sur le contrôleur avec les bons arguments ; `_active_node_widget` remis à None après action

### Résultat des tests
```
Ran 18 tests — OK  (vérifiés dans l'IDE)
```

---

## Étape 5 — `IdNodeWidget` *(2026-05-05)*

**Objectif :** Widget pour les nœuds `IdNode` (variables) avec renommage inline et retour à ENode.

### Fichiers créés

#### `gui/IdNodeWidget.py`
- Display : bouton affichant le nom de la variable, clic → `input_mode_requested`.
- Input : champ texte pré-rempli avec le nom courant + bouton `✓` (ou Enter) → `("rename", new_name)` ; bouton `→E` → `("revert", None)` ; bouton `✕` → retour Display sans signal.
- Chaîne vide ou espaces seuls : pas d'action.

#### `tests/gui/IdNodeWidgetTests.py`
18 tests en 4 classes :
- `IdNodeWidgetDisplayTests` — état initial, texte du bouton, bouton activé, signal `input_mode_requested`, cohérence du nom
- `IdNodeWidgetRenameTests` — pré-remplissage, confirmation par bouton ou Enter, strip, chaîne vide/espaces, retour en Display
- `IdNodeWidgetRevertTests` — signal `revert`, payload None, retour en Display
- `IdNodeWidgetCancelTests` — retour en Display sans signal

### Résultat des tests
```
Ran 18 tests — OK  (vérifiés dans l'IDE)
```

---

## Étape 4 — `OpNodeWidget` *(2026-05-05)*

**Objectif :** Widget pour les nœuds `OpNode` avec changement d'opérateur de même valence.

### Fichiers créés

#### `gui/OpNodeWidget.py`
- `_BINARY_OPERATORS` : ensemble des opérateurs binaires (And, Or, Xor, Impl, Cons, Eq, Neq).
- Display : bouton affichant le lexème ; cliquable pour les binaires, désactivé pour NOT et parenthèses.
- Input : boutons pour tous les autres opérateurs binaires + bouton `✕` annuler (retour Display sans signal).
- `_op_key` posé avant `super().__init__()` pour que les méthodes `_build_*` y aient accès.

#### `tests/gui/OpNodeWidgetTests.py`
16 tests en 4 classes :
- `OpNodeWidgetBinaryDisplayTests` — état initial, bouton activé, texte lexème, signal
- `OpNodeWidgetNonBinaryDisplayTests` — NOT, `(`, `)` désactivés
- `OpNodeWidgetInputTests` — alternatives excluent l'opérateur courant, signal `change_op`, retour Display, annuler sans signal
- `OpNodeWidgetVariantTests` — cohérence pour différents opérateurs initiaux

### Résultat des tests
```
Ran 16 tests — OK  (vérifiés dans l'IDE)
```

---

## Étape 3 — `ENodeWidget` *(2026-05-05)*

**Objectif :** Widget pour les nœuds ENode (expansion avec opérateur ou conversion en variable).

### Fichiers créés

#### `gui/ENodeWidget.py`
- `_ENODE_EXPANSIONS` : liste ordonnée `(op_key, label)` pour les 9 options (NOT, binaires, parenthèses).
- Display : bouton `?`, clic → `input_mode_requested`.
- Input : un bouton par expansion (`_op_buttons[op_key]`) + champ texte `_var_input` + bouton `→` (`_var_confirm`).
- Actions : `("expand", op_key)` ou `("to_id", name)` (strip, rejet si vide).

#### `tests/gui/ENodeWidgetTests.py`
13 tests en 3 classes :
- `ENodeWidgetDisplayTests` — état initial, signal `input_mode_requested`
- `ENodeWidgetExpandTests` — présence de tous les boutons, clé correcte, retour en Display
- `ENodeWidgetVariableTests` — confirmation bouton/Enter, strip, vide/espaces, champ vidé, retour en Display

### Résultat des tests
```
Ran 13 tests — OK  (vérifiés dans l'IDE)
```

---

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
