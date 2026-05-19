# TODO — pyCalcCheckComposer

## Ordre de réalisation suggéré

| Priorité | Item                       | Raison                                                              |
|----------|----------------------------|---------------------------------------------------------------------|
| ~~P1~~   | ~~Compaction du mode Input~~   | ✅ Terminé                                                          |
| **P1**   | Suggestions de variables   | Gain immédiat, périmètre réduit, aucune dépendance                  |
| **P1**   | Extension / annexion       | Friction quotidienne élevée, périmètre contenu                      |
| **P2**   | Hints entre expressions    | Structure sémantique centrale ; doit précéder la sérialisation      |
| **P2**   | Menu + gestion de preuve   | Nécessite que les hints soient définis pour la sérialisation complète |
| **P3**   | Undo / Redo                | Mieux fait quand toutes les opérations sont stables                 |
| **P3**   | Sélection par rectangle    | Amélioration UX ; le ⌘+clic est fonctionnel en attendant            |

---

## P1 — Compaction du mode Input (réduction du choc visuel)

En mode Input, les widgets (`ENodeWidget`, `OpNodeWidget`, `IdNodeWidget`) sont beaucoup plus grands que leur équivalent Display. Ce saut de taille est désorientant : l'utilisateur a l'impression qu'un nouveau widget a explosé à l'écran plutôt que le même nœud a changé d'état.

**Objectif :** réduire au maximum la taille du mode Input par compaction inline (approche A), sans supprimer de fonctionnalité.

**Leviers de compaction envisagés :**
- Réduire la taille des boutons d'opérateurs (`NODE_INPUT_BUTTON_HEIGHT`, largeur).
- Réduire les marges et espacements internes (`NODE_INPUT_LAYOUT_SPACING`).
- Réduire la taille de police des boutons (via `GuiConstants` / `APP_STYLESHEET`).
- Limiter la largeur du champ texte variable au strict nécessaire.

**Critère de succès :** après le clic sur un nœud, le widget input occupe une surface proche de celle du widget display — l'utilisateur perçoit une transformation, pas une substitution.

**Travail requis :**
- Ajuster les constantes dans `gui/GuiConstants.py`.
- Vérifier visuellement sur `ENodeWidget`, `OpNodeWidget` et `IdNodeWidget`.
- Aucun test automatisé requis (validation visuelle suffisante).

---

## P1 — Suggestions de variables en mode Input

Dans `ENodeWidget` (zone de saisie de variable), remplacer ou enrichir le `QLineEdit` par un widget avec autocomplétion ou menu déroulant :

- Proposer en priorité les variables **déjà utilisées** dans la preuve courante (collectées depuis tous les `IdNode` de toutes les expressions).
- Si aucune variable n'est encore définie : proposer un ensemble par défaut (`p`, `q`, `r`, `s`, `t`…).
- La saisie libre reste possible (l'utilisateur peut toujours taper un nom arbitraire).

**Travail requis :**
- `ProofController` expose une méthode `get_used_variables() -> list[str]` qui parcourt tous les arbres.
- `ENodeWidget` reçoit cette liste au moment de l'entrée en mode Input (via `ExpressionWidget` qui fait le pont).

---

## P1 — Extension d'un sous-arbre existant (annexion)

Permettre d'annexer un opérateur à une expression partiellement construite sans la collapser.

**Exemple :** l'utilisateur a `p ET q` et réalise qu'il voulait `p ET q OU s`.

**Mécanique envisagée :** sélectionner le sous-arbre cible (ex. : les nœuds de `p ET q`), puis choisir «Annexer opérateur» dans le menu contextuel. L'arbre est restructuré : le contenu actuel de l'ENode racine du sous-arbre est enveloppé comme opérande gauche d'un nouveau nœud binaire, et un nouvel ENode vide est ajouté comme opérande droit — sans passer par un collapse/rebuild.

**Travail modèle :** nouvelle méthode `annex_operator(enode_id, op)` dans `BooleanExpressionTree` qui réorganise les enfants de l'ENode visé sans détruire ce qui existe.

---

## P2 — Hints entre expressions

Entre chaque paire d'expressions consécutives, afficher un **hint** : une règle justifiant la transformation.

### Étapes prévues

1. **Grammaire des hints** — définir les formes possibles d'un hint (ex. : règle nommée, axiome, hypothèse, référence à une étape précédente…).
2. **Modèle** — implanter la grammaire sous forme de classes Python (dans un nouveau module `Hint/` ou similaire).
3. **HintWidget** — widget PyQt6 affiché entre deux `ExpressionWidget`.
4. **Intégration dans `ProofWindow` / `ProofController`** — intercaler un `HintWidget` entre chaque paire d'expressions lors de l'ajout d'une nouvelle expression.

---

## P2 — Menu principal et gestion de preuve

**Menu Fichier**
- Nouvelle preuve (reset à zéro)
- Enregistrer la preuve (sérialisation — format à définir, JSON probable)
- Charger une preuve

**Menu Édition** (manipulations de la liste d'expressions)
- Insérer une expression (avant ou après la position courante)
- Supprimer l'expression sélectionnée
- Reset la preuve à zéro (avec confirmation)

**Travail requis :**
- Sérialisation/désérialisation de `BooleanExpressionTree` (et des hints).
- Notion d'«expression courante» au niveau de `ProofWindow` pour cibler les opérations d'édition.
- Gestion des modifications non sauvegardées (dialogue «Voulez-vous enregistrer ?»).

---

## P3 — Undo / Redo

- Chaque opération sur l'arbre (`expand`, `collapse`, `rename`, `change_op`, `revert`, `annex`…) doit être réversible.
- Approche envisagée : patron **Command** — chaque action encapsule un `do()` et un `undo()` ; `ProofController` maintient une pile d'historique par expression (ou globale).
- Raccourcis clavier : ⌘Z / ⌘⇧Z (macOS standard).
- À coordonner avec la sérialisation : l'historique n'est probablement pas sauvegardé, seulement l'état courant.

---

## P3 — Sélection par rectangle (rubber band)

- Remplacer ou compléter le ⌘+clic par un glisser-déposer qui dessine un rectangle de sélection sur l'`ExpressionWidget`.
- Les nœuds dont le widget est recoupé par le rectangle sont ajoutés à la sélection.
- L'aspect de la sélection change dès que `find_collapsible_ancestor` retourne un résultat valide (ex. : contour vert au lieu de jaune) pour indiquer que le collapse est disponible.
