# Feature Specification: Angular ESLint — Best Practices Rules

**Feature Branch**: `002-angular-eslint-rules`
**Created**: 2026-02-19
**Status**: Draft
**Input**: User description: "Ajouter ESLint avec les meilleures règles Angular au frontend : interdiction des subscribes imbriqués, convention $ pour les Observables, règles Angular spécifiques, règles TypeScript strictes, règles générales de qualité. Intégrer dans le workflow CI (npm run lint doit passer à 0 erreur)."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Détection automatique des violations de qualité (Priority: P1)

En tant que développeur, lorsque j'écris du code qui viole une règle de qualité (subscribe imbriqué, usage de `any`, Observable sans `$`, etc.), je veux être immédiatement informé avec le fichier, la ligne et la règle concernée, afin de corriger le problème avant de commiter.

**Why this priority**: C'est la valeur fondamentale de la feature. Sans détection fiable des violations, les autres user stories n'ont pas de sens.

**Independent Test**: Introduire une violation connue (ex. subscribe dans un subscribe) → exécuter la commande de lint → vérifier que l'erreur est rapportée avec fichier + ligne + description.

**Acceptance Scenarios**:

1. **Given** du code contenant un `subscribe()` imbriqué dans un autre `subscribe()`, **When** la commande de lint est exécutée, **Then** une erreur est rapportée indiquant le fichier, la ligne et la règle violée.
2. **Given** une propriété Observable nommée sans suffixe `$` (ex. `data` au lieu de `data$`), **When** la commande de lint est exécutée, **Then** une erreur indique que la convention de nommage n'est pas respectée.
3. **Given** l'usage du type `any` dans un fichier TypeScript, **When** la commande de lint est exécutée, **Then** une erreur est rapportée.
4. **Given** du code conforme à toutes les règles, **When** la commande de lint est exécutée, **Then** aucune erreur n'est rapportée et la commande se termine avec succès.

---

### User Story 2 — Zéro erreur de lint sur le code existant (Priority: P1)

En tant que développeur, je veux que le code Angular actuel du projet soit conforme à toutes les règles définies, afin que la baseline soit saine et que chaque nouvelle violation soit clairement identifiable comme une régression.

**Why this priority**: Si le code existant contient des violations non corrigées, la commande de lint ne peut pas servir de gate CI et perd toute valeur.

**Independent Test**: Exécuter la commande de lint sur le projet — elle doit se terminer avec code de sortie 0 et afficher "0 errors, 0 warnings".

**Acceptance Scenarios**:

1. **Given** le code existant du projet frontend, **When** la commande de lint est exécutée après configuration et correction, **Then** le résultat affiche 0 erreurs et 0 avertissements.
2. **Given** une correction partielle du code, **When** la commande de lint est exécutée, **Then** seules les violations restantes sont rapportées (pas de faux positifs).

---

### User Story 3 — Intégration dans le workflow CI (Priority: P2)

En tant que tech lead, je veux que la commande de lint soit intégrée dans le workflow de développement (script `npm run lint`) et qu'elle échoue avec un code de sortie non-nul en cas de violation, afin de bloquer les commits ou les pipelines contenant du code non conforme.

**Why this priority**: Sans intégration CI, la conformité repose uniquement sur la discipline individuelle et n'est pas garantie.

**Independent Test**: Introduire une violation → exécuter `npm run lint` → vérifier que la commande retourne un code de sortie non-nul (échec).

**Acceptance Scenarios**:

1. **Given** un script `npm run lint` configuré, **When** le code est conforme, **Then** la commande retourne code de sortie 0.
2. **Given** un script `npm run lint` configuré, **When** une violation est présente, **Then** la commande retourne un code de sortie non-nul et liste les violations.
3. **Given** la commande de lint, **When** elle s'exécute sur l'ensemble du projet, **Then** elle se termine en moins de 30 secondes.

---

### Edge Cases

- Que se passe-t-il si un fichier généré automatiquement (build, node_modules) contient des violations ? → Ces fichiers doivent être exclus automatiquement de l'analyse.
- Comment gérer les rares cas légitimes où `any` est inévitable (interop librairie tierce sans types) ? → Une directive d'exception locale doit être disponible mais visible en revue de code.
- Que se passe-t-il si une règle génère des faux positifs sur du code Angular valide ? → La règle doit pouvoir être configurée en avertissement plutôt qu'erreur, sans la désactiver entièrement.
- Un observable retourné par une méthode doit-il aussi porter le `$` ? → Oui, la convention s'applique aux propriétés et aux méthodes dont le type de retour est Observable.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT détecter et signaler comme erreur tout `subscribe()` appelé à l'intérieur du callback d'un autre `subscribe()`.
- **FR-002**: Le système DOIT imposer la convention de nommage `$` (suffixe dollar) pour toutes les propriétés de classe dont le type est `Observable<T>`.
- **FR-003**: Le système DOIT imposer la convention de nommage `$` pour toutes les méthodes dont le type de retour est `Observable<T>`.
- **FR-004**: Le système DOIT interdire l'usage du type `any` explicite dans le code TypeScript de l'application.
- **FR-005**: Le système DOIT interdire l'usage de l'opérateur de non-null assertion `!` dans le code TypeScript.
- **FR-006**: Le système DOIT interdire les appels à `console.log`, `console.warn` et `console.error` dans le code de production.
- **FR-007**: Le système DOIT signaler les variables et paramètres déclarés mais jamais utilisés.
- **FR-008**: Le système DOIT imposer l'usage de `ChangeDetectionStrategy.OnPush` pour tous les composants Angular.
- **FR-009**: Le système DOIT imposer l'usage de la fonction `inject()` pour l'injection de dépendances, à la place de l'injection par constructeur.
- **FR-010**: Le système DOIT détecter les imports déclarés dans le tableau `imports` d'un composant standalone mais jamais utilisés dans son template.
- **FR-011**: Le système DOIT signaler les fonctions ou méthodes dont la complexité cyclomatique dépasse 10.
- **FR-012**: La commande de lint DOIT être exécutable via `npm run lint` sans paramètre supplémentaire.
- **FR-013**: Les répertoires générés (`dist/`, `node_modules/`, `.angular/`) DOIVENT être exclus automatiquement de l'analyse.
- **FR-014**: Le code existant du projet DOIT être corrigé pour respecter toutes les règles définies (zéro violation à la mise en place).

### Assumptions

- Le frontend est une application Angular 21 standalone avec TypeScript strict déjà activé.
- Les développeurs utilisent un éditeur compatible ESLint (VS Code avec extension ESLint) pour bénéficier du feedback en temps réel.
- Les règles relatives aux Observables nécessitent un plugin ESLint dédié RxJS.
- Les règles Angular spécifiques nécessitent un plugin ESLint dédié Angular.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La commande de lint se termine avec 0 erreurs et 0 avertissements sur le code existant après configuration et correction.
- **SC-002**: Toute nouvelle violation introduite dans le code est détectée par la commande de lint avec indication du fichier, de la ligne et de la règle.
- **SC-003**: La commande de lint s'exécute en moins de 30 secondes sur l'ensemble du projet frontend.
- **SC-004**: Un développeur peut identifier et corriger une violation en suivant uniquement le message d'erreur rapporté, sans documentation externe.
- **SC-005**: Zéro faux positif sur du code Angular 21 valide et idiomatique (signals, inject(), OnPush, @if/@for).
