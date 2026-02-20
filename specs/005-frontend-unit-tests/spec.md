# Feature Specification: Tests Unitaires Frontend

**Feature Branch**: `005-frontend-unit-tests`
**Created**: 2026-02-20
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Configuration et exécution de la suite de tests (Priority: P1)

Un développeur peut lancer la suite de tests avec une seule commande depuis le dossier frontend, et obtenir un rapport clair indiquant quels tests passent ou échouent.

**Why this priority**: Sans infrastructure de test fonctionnelle, aucun test ne peut être écrit ni exécuté. C'est le prérequis bloquant.

**Independent Test**: Exécuter `npm test` dans le frontend → la commande s'exécute sans erreur de configuration et affiche un rapport de résultats.

**Acceptance Scenarios**:

1. **Given** un dépôt cloné proprement, **When** le développeur exécute la commande de test, **Then** la suite démarre sans erreur de configuration et un rapport s'affiche
2. **Given** un test qui échoue intentionnellement, **When** la suite tourne, **Then** l'échec est clairement identifié avec le nom du test et la cause

---

### User Story 2 — Tests du composant Chat (Priority: P2)

Les comportements clés du composant Chat sont couverts par des tests : envoi de message, affichage des chips de suggestion, et rendu Markdown des réponses assistant.

**Why this priority**: Le Chat est le composant principal de l'application — ses régressions ont le plus d'impact utilisateur.

**Independent Test**: Exécuter uniquement les tests Chat → tous passent, les comportements critiques sont vérifiés sans lancer l'application.

**Acceptance Scenarios**:

1. **Given** le composant Chat initialisé, **When** la conversation est vide, **Then** les chips de suggestion sont visibles
2. **Given** les chips visibles, **When** l'utilisateur clique sur un chip, **Then** le message est envoyé et les chips disparaissent
3. **Given** le composant Chat, **When** `sendMessage()` est appelé avec un prompt vide, **Then** aucun message n'est ajouté
4. **Given** une réponse assistant reçue, **When** le contenu est affiché, **Then** les messages assistant utilisent le rendu riche et les messages utilisateur restent en texte brut
5. **Given** le composant en cours de chargement, **When** `isLoading` est vrai, **Then** le bouton d'envoi est désactivé

---

### User Story 3 — Tests du composant Ingest (Priority: P3)

Les comportements de sélection et suppression groupée du composant Ingest sont couverts : sélection individuelle, sélection totale, état du bouton de suppression.

**Why this priority**: L'Ingest contient une logique d'état complexe (signals dérivés, Set mutable) — les tests protègent contre les régressions de cette logique.

**Independent Test**: Exécuter uniquement les tests Ingest → les scénarios de sélection et de suppression passent sans lancer l'API.

**Acceptance Scenarios**:

1. **Given** une liste de documents, **When** l'utilisateur coche une ligne, **Then** `selectedIds` contient cet ID et `noneSelected` devient faux
2. **Given** tous les documents cochés, **When** `allSelected` est évalué, **Then** il retourne vrai
3. **Given** une sélection partielle, **When** `someSelected` est évalué, **Then** il retourne vrai et `allSelected` retourne faux
4. **Given** aucune sélection, **When** l'état est évalué, **Then** le bouton "Supprimer la sélection" est désactivé
5. **Given** une sélection active, **When** `toggleAll()` est appelé, **Then** tous les documents sont sélectionnés ; un second appel vide la sélection

---

### Edge Cases

- Que se passe-t-il si un test dépend d'un service HTTP réel ? → Les appels HTTP doivent être interceptés/mockés, jamais exécutés réellement
- Que se passe-t-il si un composant utilise `inject()` ? → L'injection de dépendances doit fonctionner dans le contexte de test
- Que se passe-t-il si les signaux Angular ne se mettent pas à jour synchronement dans les tests ? → Les assertions sur les signaux doivent être faites après propagation des changements

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La suite de tests DOIT s'exécuter avec une commande unique sans configuration manuelle supplémentaire
- **FR-002**: Les tests DOIVENT être isolés — aucun test ne doit dépendre de l'état d'un autre test
- **FR-003**: Les appels réseau (API RAG) DOIVENT être interceptés et remplacés par des données fictives dans tous les tests
- **FR-004**: Les tests du composant Chat DOIVENT couvrir : état vide (chips), envoi de message, validation du prompt vide, distinction assistant/utilisateur, état de chargement
- **FR-005**: Les tests du composant Ingest DOIVENT couvrir : sélection individuelle, computed signals (`allSelected`, `someSelected`, `noneSelected`), `toggleAll()`, état des boutons de suppression
- **FR-006**: Les tests DOIVENT s'exécuter en moins de 30 secondes pour l'ensemble de la suite
- **FR-007**: Un rapport de couverture DOIT être disponible sur demande (commande séparée)

### Assumptions

- L'outil de test (Vitest) est déjà installé — seule la configuration manque
- Les composants sont standalone Angular 21 avec signals et OnPush — les utilitaires de test doivent le supporter
- Aucune base de données ni serveur réel n'est requis pour les tests unitaires

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La commande de test s'exécute en moins de 30 secondes sur un poste de développement standard
- **SC-002**: 100% des scénarios d'acceptance définis dans les user stories sont couverts par au moins un test
- **SC-003**: 0 appel réseau réel effectué durant l'exécution des tests
- **SC-004**: Chaque test peut être exécuté indépendamment et produit le même résultat
- **SC-005**: Un test en échec identifie clairement le composant, le scénario et la valeur attendue vs reçue
