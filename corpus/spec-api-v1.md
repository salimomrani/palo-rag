# Spécification API REST v1 — PALO Platform

## Informations générales

**Base URL** : `https://api.palo.io/v1`
**Format** : JSON (Content-Type: application/json)
**Authentification** : Bearer token (JWT) dans le header `Authorization`
**Rate limiting** : 1000 req/jour (Business), illimité (Enterprise), 0 (Starter)
**Version** : v1.0 — stable depuis 2025-01-01

## Authentification

### POST /auth/token
Génère un token d'accès JWT.

**Body** :
```json
{"client_id": "string", "client_secret": "string"}
```
**Réponse 200** :
```json
{"access_token": "eyJ...", "expires_in": 3600, "token_type": "Bearer"}
```
**Erreurs** : 401 (credentials invalides), 429 (trop de tentatives)

### POST /auth/refresh
Renouvelle un token expirant. Requiert le header `Authorization: Bearer {token}`.

## Endpoints Projets

### GET /projects
Liste les projets accessibles. Paramètres query : `limit` (défaut 20, max 100), `offset`, `status` (active|archived).

### POST /projects
Crée un nouveau projet.
**Body** :
```json
{"name": "string", "description": "string", "template": "software|ops|marketing|custom"}
```

### GET /projects/{id}
Détails d'un projet. Inclut les membres, le statut et les métadonnées.

### PATCH /projects/{id}
Mise à jour partielle d'un projet. Champs modifiables : name, description, status, settings.

### DELETE /projects/{id}
Archive un projet (soft delete). Données conservées 90 jours avant suppression définitive.

## Endpoints Tickets

### GET /tickets
Liste les tickets. Filtres disponibles : `project_id`, `status` (open|in_progress|resolved|closed), `priority` (p1|p2|p3|p4), `assignee_id`, `created_after`, `created_before`.

### POST /tickets
Crée un ticket.
**Body** :
```json
{
  "title": "string",
  "description": "string",
  "project_id": "uuid",
  "priority": "p3",
  "assignee_id": "uuid (optionnel)"
}
```

### GET /tickets/{id}
Détails complets d'un ticket incluant commentaires et historique.

### PATCH /tickets/{id}
Mise à jour du ticket. Génère automatiquement un événement d'audit.

### POST /tickets/{id}/comments
Ajoute un commentaire. Supporte le Markdown. Mentionne avec `@user_id`.

## Gestion des erreurs

Tous les endpoints retournent des erreurs au format :
```json
{"error": "error_code", "message": "description lisible", "request_id": "uuid"}
```

Codes HTTP utilisés : 200 (succès), 201 (créé), 204 (supprimé), 400 (paramètre invalide), 401 (non authentifié), 403 (non autorisé), 404 (ressource introuvable), 422 (validation échouée), 429 (rate limit), 500 (erreur serveur).

## Pagination

Toutes les listes sont paginées. La réponse inclut :
```json
{"data": [...], "pagination": {"total": 150, "limit": 20, "offset": 0, "has_more": true}}
```

## Webhooks

Configurables via `POST /webhooks`. Événements disponibles : `ticket.created`, `ticket.updated`, `ticket.resolved`, `project.created`, `member.invited`. Payload signé avec HMAC-SHA256 (header `X-Palo-Signature`).
