# Feature Specification: Rendu Markdown dans le Chat

**Feature Branch**: `004-chat-markdown-render`
**Created**: 2026-02-20
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Réponses assistant lisibles avec formatage riche (Priority: P1)

Lorsque l'assistant répond avec du texte formaté (listes, titres, blocs de code, gras, italique), l'utilisateur voit un rendu visuel structuré plutôt qu'une suite de caractères bruts comme `**bold**` ou `- item`.

**Why this priority**: C'est le besoin principal — sans ce rendu, les réponses du LLM sont illisibles dès qu'elles contiennent du formatage.

**Independent Test**: Poser une question qui génère une réponse avec une liste et un bloc de code. L'utilisateur doit voir les puces rendues et le code mis en forme, pas les symboles Markdown bruts.

**Acceptance Scenarios**:

1. **Given** l'assistant répond avec `**texte important**`, **When** la réponse est affichée, **Then** le texte apparaît en gras et non comme `**texte important**`
2. **Given** l'assistant répond avec une liste `- item1\n- item2`, **When** la réponse est affichée, **Then** une liste à puces HTML est rendue
3. **Given** l'assistant répond avec un bloc de code, **When** la réponse est affichée, **Then** le bloc est rendu avec un fond distinct et une police monospace
4. **Given** l'assistant répond avec des titres `## Section`, **When** la réponse est affichée, **Then** le titre est rendu hiérarchiquement

---

### User Story 2 — Messages utilisateur non affectés (Priority: P2)

Les messages envoyés par l'utilisateur continuent d'être affichés tels quels, en texte brut. Si un utilisateur tape `**hello**`, il voit `**hello**` et non du texte en gras.

**Why this priority**: Différencie clairement la bulle utilisateur de la bulle assistant. Cohérent avec les conventions des interfaces de chat IA.

**Independent Test**: Envoyer un message contenant des symboles Markdown. Le message utilisateur doit s'afficher en texte brut, non rendu.

**Acceptance Scenarios**:

1. **Given** l'utilisateur envoie `*hello*`, **When** le message est affiché, **Then** il s'affiche comme `*hello*` sans interprétation
2. **Given** l'assistant répond et l'utilisateur répond à nouveau, **When** les deux messages sont affichés, **Then** seul le message assistant est rendu en Markdown

---

### Edge Cases

- Que se passe-t-il si la réponse est vide ou ne contient aucun Markdown ? → Affichage du texte tel quel, sans erreur
- Que se passe-t-il si la réponse est en cours de streaming (tokens partiels) ? → Le rendu progressif reste stable et ne produit pas de HTML cassé
- Que se passe-t-il si le contenu Markdown est malformé ? → Rendu best-effort sans erreur visible

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT rendre le contenu Markdown des messages assistant en HTML visuel (gras, italique, listes, titres, blocs de code)
- **FR-002**: Les messages utilisateur DOIVENT être affichés en texte brut, sans interprétation Markdown
- **FR-003**: Le rendu DOIT fonctionner durant le streaming token-par-token sans casser l'affichage
- **FR-004**: Les styles du rendu Markdown DOIVENT être cohérents avec la charte graphique existante (thème sombre du chat)
- **FR-005**: Le rendu DOIT gérer gracieusement le Markdown malformé sans erreur d'interface

### Assumptions

- La bibliothèque de rendu Markdown est déjà disponible dans le projet frontend
- Les réponses du LLM peuvent contenir tout sous-ensemble de Markdown standard
- Aucune donnée sensible n'est impliquée dans ce rendu

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des éléments Markdown courants (gras, listes, code, titres) sont rendus visuellement dans les messages assistant
- **SC-002**: 0 régression sur les messages utilisateur — aucun symbole Markdown n'est interprété côté utilisateur
- **SC-003**: Le rendu fonctionne sans délai perceptible ni flash visuel durant le streaming
- **SC-004**: Les styles du rendu s'intègrent sans rupture visuelle dans l'interface existante
