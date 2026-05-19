# Journal de développement — pyCalcCheckComposer

## Symboles Unicode pour les opérateurs booléens *(2026-05-19)*

**Objectif :** Remplacer les lexèmes textuels (`and`, `or`, `impl`…) par leurs équivalents Unicode logiques, cohérents avec la notation LaTeX utilisée dans Overleaf.

### Correspondances appliquées

| Opérateur | Avant | Après |
|---|---|---|
| NOT | `not` | ¬ |
| AND | `and` | ∧ |
| OR | `or` | ∨ |
| XOR | `^` | ⊕ |
| IMPL | `impl` | ⇒ |
| CONS | `cons` | ⇐ |
| EQ | `eq` | ≡ |
| NEQ | `neq` | ≢ |

### Fichiers modifiés

#### `BooleanExpression/Node/OpNode.py`
- `BooleanOperators` : valeurs mises à jour avec les caractères Unicode.

#### `gui/ENodeWidget.py`
- `_ENODE_EXPANSIONS` remplacé par un calcul dynamique depuis `BooleanOperators` via `_enode_label(op_key)`, éliminant les labels codés en dur et garantissant la cohérence avec les nœuds en mode Display.

**Test :** validation visuelle — nœuds Display et boutons Input affichent les mêmes symboles.

---

## Compaction du mode Input *(2026-05-19)*

**Objectif :** Réduire la disparité de taille entre le mode Display (bouton ~40 px) et le mode Input (grille de boutons), pour que l'utilisateur perçoive une transformation du nœud plutôt qu'une substitution par un nouveau widget.

### Fichiers modifiés

#### `gui/GuiConstants.py`
- `NODE_INPUT_BUTTON_HEIGHT` : 35 → 22
- `NODE_ACTION_BUTTON_WIDTH` : 30 → 22
- `NODE_INPUT_LAYOUT_SPACING` : 4 → 2
- `NODE_INPUT_CONTAINER_PADDING` : 4 → 2
- Ajout de `ENODE_INPUT_GRID_COLUMNS = 5` (grille spécifique à `ENodeWidget`)
- Ajout de `NODE_INPUT_FONT_SIZE = 10`
- Ajout dans `APP_STYLESHEET` : `QWidget#nodeInput QPushButton { font-size: 10px; padding: 1px 2px; }`

#### `gui/ENodeWidget.py`
- Utilise `ENODE_INPUT_GRID_COLUMNS` (5 colonnes) au lieu de `NODE_INPUT_GRID_COLUMNS` (3).
- `var_row` calculé par division plafond `(len + cols - 1) // cols` pour éviter le chevauchement avec la rangée texte quand la grille n'est pas divisible parfaitement.
- Résultat : les 9 boutons d'opérateurs tiennent sur 2 rangées (5 + 4) au lieu de 3.

**Test :** validation visuelle — le mode Input de `ENodeWidget`, `OpNodeWidget` et `IdNodeWidget` est nettement plus compact.

---

## Étape 5 — Câblage de l'action au contrôleur *(2026-05-07)*

**Objectif :** Connecter «Réduire en E» au modèle via le contrôleur, et vérifier que l'expression se collapse correctement.

### Fichiers modifiés

#### `controllers/ProofController.py`
- `collapse_subtree(expression_index, enode_id)` : appelle `tree.collapse_node(enode_id)` puis `_refresh`.

#### `gui/ExpressionWidget.py`
- `_on_collapse_to_enode(ancestor_id)` : remplace le stub par `controller.collapse_subtree(expression_index, ancestor_id)`.

**Test :** construire `p AND q`, ⌘+cliquer les trois nœuds, clic-droit → «Réduire en E» → l'expression redevient `?`.

---

## Étape 4 — Menu contextuel sur clic-droit *(2026-05-07)*

**Objectif :** Afficher un `QMenu` sur clic-droit dans l'expression, avec l'item «Réduire en E» actif si la sélection forme un sous-arbre complet, grisé sinon.

### Fichier modifié : `gui/ExpressionWidget.py`

- Import de `QMenu`.
- `eventFilter` restructuré : `RightButton` et `LeftButton` traités séparément.
  - `RightButton` dans les bornes du widget : ferme le mode Input si actif, appelle `_show_context_menu`, consomme l'événement (`return True`). Couvre le clic-droit natif **et** le Ctrl+clic macOS (tous deux signalés comme `RightButton`).
  - `LeftButton` sans ⌘ : vide la sélection + ferme le mode Input si hors nœud actif.
- `_show_context_menu(global_pos)` : calcule `find_collapsible_ancestor`, crée le `QMenu`, active ou grise l'item selon le résultat, déclenche `_on_collapse_to_enode` si l'item est choisi.
- `_on_collapse_to_enode(ancestor_id)` : stub vide — câblage au contrôleur à l'étape 5.

**Test :** clic-droit sur expression avec sélection valide (⌘+clic sur tous les nœuds d'un sous-arbre) → menu avec «Réduire en E» actif ; clic-droit sans sélection ou sélection partielle → item grisé.

---

## Étape 3 — `find_collapsible_ancestor()` dans `ExpressionTree` *(2026-05-07)*

**Objectif :** Déterminer si un ensemble de nœuds visibles forme exactement le sous-arbre d'un ENode ancêtre, et retourner l'id de cet ENode.

**Algorithme :**
1. Pour chaque `node_id` sélectionné, remonter la chaîne de parents jusqu'à la racine.
2. Calculer l'intersection de toutes les chaînes = ancêtres communs.
3. Le LCA est le premier élément d'une chaîne qui appartient à cette intersection (le plus profond).
4. Vérifier que l'ensemble des feuilles du LCA == exactement `node_ids`. Sinon → `None`.

### Fichiers modifiés

#### `BooleanExpression/ExpressionTree.py`
- `find_collapsible_ancestor(node_ids: set) -> node_id | None`

#### `tests/BooleanExpressionTests/ModelExtensionsTests.py`
- `FindCollapsibleAncestorTests` : 7 tests couvrant sélection vide, arbre plat, sélection partielle, sous-arbre imbriqué, toutes les feuilles, sélection transversale invalide, nœud unique.

**Test :** lancer `ModelExtensionsTests.py` — tous les tests doivent passer.

---

## Étape 2 — `ExpressionWidget` gère l'ensemble de nœuds sélectionnés *(2026-05-07)*

**Objectif :** Maintenir un ensemble cohérent de nœuds sélectionnés ; vider la sélection sur clic normal ou clic extérieur.

### Fichier modifié : `gui/ExpressionWidget.py`

- `_selected_node_ids: set` et `_node_widgets: dict` (node_id → NodeWidget) ajoutés dans `__init__` et réinitialisés dans `render_expression`.
- `render_expression` : connecte `selection_toggled` de chaque widget à `_on_selection_toggled` et peuple `_node_widgets`.
- `_on_selection_toggled(widget)` : ajoute ou retire le `node_id` de `_selected_node_ids` selon `widget.is_selected()`.
- `_clear_selection()` : appelle `set_selected(False)` sur chaque widget sélectionné, puis vide le set.
- `eventFilter` : sur tout `MouseButtonPress` sans modificateur ⌘, appelle `_clear_selection()`. Les ⌘+clics sont laissés passer sans vider la sélection.
- `_on_input_mode_requested` : appelle `_clear_selection()` avant d'entrer en mode Input.

**Test :** ⌘+clic plusieurs nœuds → tous jaunes ; clic normal n'importe où → tous dé-sélectionnés.

---

## Étape 1 — État de sélection visuel dans `NodeWidget` *(2026-05-07)*

**Objectif :** Permettre la sélection individuelle d'un nœud par Ctrl+clic, avec retour visuel (fond jaune), sans perturber le comportement existant (clic normal → mode Input).

### Fichiers modifiés

#### `gui/GuiConstants.py`
- `COLOR_SELECTED_BG = "#ffe082"` — fond jaune ambré pour un nœud sélectionné.
- `COLOR_SELECTED_BORDER = "#ffc107"` — bordure dorée.

#### `gui/NodeWidget.py`
- Signal `selection_toggled(object)` ajouté.
- Attribut `_is_selected: bool` initialisé à `False`.
- `installEventFilter(self)` posé sur `_display_widget` dans `__init__`.
- `eventFilter` : intercepte `MouseButtonPress` avec modificateur `Ctrl` sur le bouton Display ; bascule `_is_selected`, émet `selection_toggled`, retourne `True` (consomme l'événement — le mode Input n'est pas déclenché).
- `set_selected(bool)` : applique ou efface un `setStyleSheet` sur `_display_widget` (jaune ambré si sélectionné, `""` sinon pour retomber sur `APP_STYLESHEET`).
- `is_selected() -> bool`.

**Test :** Ctrl+clic un nœud → fond jaune ; Ctrl+clic à nouveau → retour normal ; clic normal → mode Input, pas de sélection.

---

## Correctif : rendu incohérent sur macOS dark mode *(2026-05-07)*

**Symptôme :** En mode Input, le fond vert clair est visible, mais les boutons n'ont pas de fond (labels blancs flottants) et le champ texte est noir. En mode Display, le bouton `?` reste invisible.

**Cause :** Le style natif macOS (Cocoa) respecte le thème sombre du système (dark mode). Quand PyQt6 utilise ce style, les widgets enfants héritent des couleurs du thème sombre (texte blanc, fond de champ sombre), en conflit avec les stylesheets explicites (fond vert clair). La combinaison rend les boutons transparents et les labels illisibles.

**Approche retenue :** plutôt que corriger les cas au cas par cas, définir explicitement tous les paramètres visuels dans `GuiConstants` et les appliquer globalement — l'app ne dépend ainsi d'aucun thème de plateforme.

### Fichiers modifiés

#### `gui/GuiConstants.py`
- Ajout de la palette générale : `COLOR_TEXT`, `COLOR_BUTTON_BG`, `COLOR_BUTTON_BG_HOVER`, `COLOR_BUTTON_BG_PRESSED`, `COLOR_BUTTON_DISABLED_FG`, `COLOR_WIDGET_BORDER`, `COLOR_INPUT_BG`.
- Ajout de `APP_STYLESHEET` : stylesheet globale couvrant `QPushButton` (normal, hover, pressed, disabled), `QLineEdit`, et `QWidget#nodeInput`.
- Suppression de `NODE_INPUT_CONTAINER_STYLE` (absorbé par `APP_STYLESHEET`).

#### `gui/NodeWidget.py`
- Suppression du `setStyleSheet(...)` par widget sur `_input_widget` — l'`objectName("nodeInput")` suffit pour que `APP_STYLESHEET` s'applique.

#### `ProofApp.py`
- Ajout de `self._qt_app.setStyle("Fusion")` (base cross-platform) et `self._qt_app.setStyleSheet(GuiConstants.APP_STYLESHEET)`.

---

## Correctif : `_display_widget` invisible au démarrage *(2026-05-07)*

**Symptôme :** Sur cette machine (Darwin 25.3.0), les nœuds n'apparaissent pas en mode Display à la création — ils deviennent visibles seulement après un premier passage en mode Input. Sur le MacBook, le comportement est normal.

**Cause :** Dans `NodeWidget.__init__`, le `_display_widget` était créé visible par défaut (comportement Qt standard), mais jamais appelé avec `.show()` explicitement. Sur certaines versions de Qt / macOS, un widget fils créé avant que le parent soit attaché à la hiérarchie de fenêtres ne s'affiche pas automatiquement. La méthode `enter_display_mode()` corrigeait le problème car elle appelle `_display_widget.show()` — ce que `__init__` n'avait jamais fait.

**Correctif — `gui/NodeWidget.py`**
- Ajout à la fin de `__init__`, après `setLayout` :
  ```python
  self._display_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
  self._display_widget.show()
  ```
- Cela garantit l'état Display initial sur toutes les plateformes, sans modifier la logique existante.

---

## Classe `ProofApp` — point d'entrée et câblage MVC *(2026-05-06)*

**Objectif :** Éliminer le couplage circulaire entre `ProofWindow` et `ProofController` ; préparer l'ouverture de plusieurs fenêtres indépendantes.

### Problème antérieur
`ProofWindow.__init__` créait `ProofController(self)` et `ProofController` stockait `self.proof_window` — les deux objets ne pouvaient pas exister l'un sans l'autre.

### Fichiers modifiés

#### `controllers/ProofController.py`
- `__init__()` ne prend plus d'argument ; `self.proof_window = None` initialement.

#### `gui/ProofWindow.py`
- `__init__(self, controller)` reçoit le contrôleur par injection au lieu de le créer.
- Import de `ProofController` supprimé.
- Bloc `__main__` supprimé (plus le point d'entrée).

### Fichier créé

#### `ProofApp.py`
- `ProofApp.__init__()` crée la `QApplication` et initialise la liste `_windows`.
- `open_proof_window()` — factory : crée un `ProofController`, un `ProofWindow`, injecte chacun dans l'autre (`controller.proof_window = window`), ajoute la paire à `_windows` (prévient le GC), affiche la fenêtre.
- `run()` — ouvre la première fenêtre et lance la boucle Qt.
- Bloc `__main__` : `ProofApp().run()`.
- La liste `_windows` permettra d'ouvrir plusieurs fenêtres indépendantes dans une version future.

---

## Fermeture du mode Input par clic extérieur *(2026-05-06)*

**Objectif :** Permettre à l'utilisateur de quitter le mode Input en cliquant n'importe où hors du nœud actif.

### Fichier modifié

#### `gui/ExpressionWidget.py`
- Installation d'un event filter au niveau de `QApplication` dans `__init__`.
- `eventFilter()` intercepte `MouseButtonPress` : si le clic est hors du `_active_node_widget` (testé via `mapFromGlobal`), appelle `enter_display_mode()` et remet `_active_node_widget` à `None`.
- L'événement n'est pas consommé (`return False`) — le clic s'exécute normalement après la fermeture.

---

## Layout grille pour le mode Input *(2026-05-06)*

**Objectif :** Réduire la largeur du widget en mode Input pour que l'utilisateur voie encore une partie de l'expression, tout en permettant une expansion verticale.

### Fichiers modifiés

#### `gui/ENodeWidget.py`
- `_build_input_widget()` : `QHBoxLayout` → `QGridLayout` à 3 colonnes.
- Les 9 boutons d'expansion occupent les lignes 0–2 (3 par ligne).
- `_var_input` s'étire sur les colonnes 0–1 de la ligne 3 ; `_var_confirm` en colonne 2.
- Suppression de `setFixedWidth(NODE_TEXT_INPUT_WIDTH)` sur `_var_input`.

#### `gui/OpNodeWidget.py`
- `_build_input_widget()` : `QHBoxLayout` → `QGridLayout` à 3 colonnes.
- Ajout de `_BINARY_OPERATOR_ORDER` (liste ordonnée) pour un affichage déterministe des alternatives.
- Le bouton `✕` suit immédiatement le dernier bouton d'alternative dans la grille.

#### `gui/IdNodeWidget.py`
- `_build_input_widget()` : `QHBoxLayout` → `QGridLayout` 2×2.
- Disposition : `[_name_input | ✓]` / `[→E | ✕]`.
- Suppression de `setFixedWidth(NODE_TEXT_INPUT_WIDTH)` sur `_name_input`.

#### `gui/GuiConstants.py`
- Suppression de `NODE_TEXT_INPUT_WIDTH` (devenu inutile).
- Ajout de `NODE_INPUT_CONTAINER_PADDING = 4` et `NODE_INPUT_GRID_COLUMNS = 3`.
- Suppression de `padding: 2px` dans le template CSS `NODE_INPUT_CONTAINER_STYLE`.

---

## Fine tuning visuel *(2026-05-06)*

### Centrage des nœuds dans `ExpressionWidget`
Les nœuds s'étiraient sur toute la largeur du widget. Ajout d'un `addStretch(1)` de chaque côté dans `render_expression()` — les nœuds se regroupent maintenant au centre.

### Encadrement du mode Input dans `NodeWidget`
En mode Input, le conteneur est désormais visuellement distingué des autres nœuds : bordure verte + fond vert pâle, appliqués via `setStyleSheet` avec le sélecteur `QWidget#nodeInput` (n'affecte pas les boutons et champs enfants).

### Constantes ajoutées dans `GuiConstants`
| Constante | Valeur |
|---|---|
| `NODE_INPUT_BORDER_COLOR` | `#4CAF50` |
| `NODE_INPUT_BACKGROUND_COLOR` | `#e8f5e9` |
| `NODE_INPUT_CONTAINER_STYLE` | template CSS pour le conteneur Input |

---

## Centralisation des constantes GUI *(2026-05-05)*

**Objectif :** Éliminer toutes les valeurs numériques codées en dur dans les widgets ; préparer la migration vers une configuration JSON.

### Constantes ajoutées dans `gui/GuiConstants.py`

| Constante | Valeur | Sémantique |
|---|---|---|
| `ENODE_DISPLAY_BUTTON_SIZE` | 40 | Taille du bouton `?` carré (ENodeWidget) |
| `NODE_DISPLAY_BUTTON_HEIGHT` | 40 | Hauteur des boutons Display (OpNodeWidget, IdNodeWidget) |
| `NODE_INPUT_BUTTON_HEIGHT` | 35 | Hauteur de tous les boutons en mode Input |
| `NODE_ACTION_BUTTON_WIDTH` | 30 | Largeur des petits boutons `✓` `→` `✕` |
| `NODE_TEXT_INPUT_WIDTH` | 80 | Largeur des champs texte (variable, nom) |
| `NODE_INPUT_LAYOUT_SPACING` | 4 | Espacement du layout en mode Input |

### Fichiers mis à jour
- `gui/ENodeWidget.py`, `gui/OpNodeWidget.py`, `gui/IdNodeWidget.py` — plus aucune valeur numérique littérale dans les appels `setFixedSize/Height/Width` et `setSpacing`.

---

## Correctif sizing `NodeWidget` *(2026-05-05)*

**Problème :** En mode Display, les NodeWidgets occupaient la largeur du mode Input (QStackedWidget impose le max de toutes ses pages). Première tentative de correction via `sizeHint()` + size policy → régression inverse : seul le quart supérieur gauche des boutons était visible (conflit entre le `setFixedSize` des boutons et la taille imposée par le layout interne).

**Solution :** Suppression du `QStackedWidget`. Les deux widgets (Display et Input) coexistent dans un `QHBoxLayout` ; le widget inactif est caché (`hide()`) **et** marqué `Ignored` pour ne pas influencer la taille du layout. `updateGeometry()` propage le changement au parent. Un flag `_is_in_input_mode` remplace le check `currentWidget()`.

### Fichier modifié
#### `gui/NodeWidget.py`
- Remplacement de `QStackedWidget` par `QHBoxLayout` + show/hide + `setSizePolicy(Ignored)`.
- Ajout de `_is_in_input_mode` (bool) comme source de vérité pour `is_in_input_mode()`.
- Suppression des overrides `sizeHint()` / `minimumSizeHint()` (devenus inutiles).

---

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
