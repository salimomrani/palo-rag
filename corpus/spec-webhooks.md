# Spécification Webhooks — PALO Platform

## Vue d'ensemble

Les webhooks permettent à votre application de recevoir des notifications en temps réel lorsque des événements se produisent sur PALO Platform. Au lieu de poller l'API, configurez une URL HTTPS sur votre serveur : PALO y enverra automatiquement un POST avec les données de l'événement.

## Configuration

### Créer un webhook
Via l'API : `POST /api/webhooks`
```json
{
  "url": "https://votre-serveur.com/palo-webhook",
  "events": ["ticket.created", "ticket.resolved", "system.incident"],
  "secret": "votre_secret_hmac_32_chars_min",
  "active": true,
  "description": "Webhook production"
}
```

Via l'interface : Paramètres → Développeurs → Webhooks → Nouveau webhook.

### Sécurisation des webhooks
Chaque delivery inclut le header `X-Palo-Signature` contenant le HMAC-SHA256 du payload signé avec votre secret. Validez toujours la signature avant de traiter le payload :

```python
import hmac, hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Structure du payload

Tous les webhooks suivent la même structure de base :
```json
{
  "event_id": "evt_01HX...",
  "event_type": "ticket.created",
  "timestamp": "2026-02-19T10:30:00Z",
  "organization_id": "org_...",
  "data": { /* données spécifiques à l'événement */ }
}
```

## Événements disponibles

### ticket.created
```json
{"data": {"ticket_id": "TKT-00512", "title": "...", "priority": "p3", "project_id": "...", "created_by": "user_id"}}
```

### ticket.status_changed
```json
{"data": {"ticket_id": "TKT-00512", "old_status": "open", "new_status": "in_progress", "changed_by": "user_id"}}
```

### ticket.resolved
```json
{"data": {"ticket_id": "TKT-00512", "resolved_by": "user_id", "resolution_time_hours": 2.5}}
```

### system.incident
```json
{"data": {"incident_id": "INC-001", "severity": "critical", "affected_services": ["api", "ui"], "status": "investigating"}}
```

## Gestion des livraisons

### Retries automatiques
En cas d'échec (timeout > 10s, réponse HTTP ≠ 2xx), PALO réessaie automatiquement selon le schéma :
- Retry 1 : +5 minutes
- Retry 2 : +30 minutes
- Retry 3 : +2 heures
- Retry 4 : +6 heures
- Abandon après 5 tentatives échouées

### Logs de livraison
Chaque tentative est journalisée (statut HTTP, durée, corps de la réponse). Consultez l'historique dans Paramètres → Développeurs → Webhooks → [webhook] → Deliveries. Vous pouvez re-déclencher manuellement une livraison échouée.

## Bonnes pratiques

- Répondez rapidement (< 5s) avec un `200 OK` et traitez l'événement de manière asynchrone
- Implémentez l'idempotence en utilisant `event_id` comme clé de déduplication
- Vérifiez toujours la signature HMAC avant traitement
- Configurez un endpoint de test distinct pour les essais (`/webhook-test`)
