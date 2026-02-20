# FAQ Support — PALO Platform

## Ouverture de tickets

**Comment créer un ticket de support ?**
Les tickets peuvent être ouverts via trois canaux : le portail support (support.palo.io), l'intégration Slack en utilisant la commande `/palo-support`, ou par email à support@palo.io. Les tickets ouverts via Slack sont automatiquement liés à votre espace de travail et organisation.

**Quels niveaux de priorité existent ?**
Quatre niveaux : P1 Critique (service inaccessible, perte de données — SLA 1h), P2 Haute (fonctionnalité majeure indisponible — SLA 4h), P3 Normale (bug non bloquant — SLA 24h), P4 Basse (question ou amélioration — SLA 72h). Les SLA s'appliquent aux heures ouvrées sauf pour P1 (24/7).

**Comment suivre l'avancement d'un ticket ?**
Chaque ticket reçoit un identifiant unique (format `TKT-XXXXX`). Le statut est visible sur le portail support et mis à jour automatiquement dans Slack si l'intégration est activée. Des notifications email sont envoyées à chaque changement de statut.

## Intégration Slack

**Comment configurer l'intégration Slack ?**
Dans votre espace PALO, allez dans Paramètres → Intégrations → Slack. Cliquez sur "Connecter Slack" et autorisez l'application dans votre espace de travail. Sélectionnez ensuite les canaux qui recevront les alertes (incidents, tickets, notifications produit).

**Quelles commandes Slack sont disponibles ?**
`/palo-support [description]` — crée un ticket support. `/palo-status` — affiche l'état des services. `/palo-docs [recherche]` — recherche dans la documentation. `/palo-ticket TKT-XXXXX` — affiche les détails d'un ticket.

**Peut-on recevoir des alertes de monitoring dans Slack ?**
Oui, les alertes de monitoring (disponibilité, performance, quota) peuvent être routées vers des canaux Slack spécifiques. La configuration se fait dans Paramètres → Monitoring → Notifications.

## Export de données

**Comment exporter l'historique de mes tickets ?**
Dans le portail support, allez dans Mon Historique → Exporter. Formats disponibles : CSV (tous champs), JSON (complet avec métadonnées), PDF (rapport formaté). La limite d'export est de 10 000 tickets par requête.

**Les pièces jointes sont-elles incluses dans l'export ?**
Les pièces jointes ne sont pas incluses dans l'export tabulaire. Elles peuvent être téléchargées individuellement depuis chaque ticket, ou en lot via l'API (endpoint `GET /api/tickets/{id}/attachments`).

**Combien de temps les tickets sont-ils conservés ?**
Les tickets sont conservés 2 ans pour le plan Starter, 5 ans pour Business, indéfiniment pour Enterprise. Après expiration, les tickets sont archivés et accessibles sur demande pendant 1 an supplémentaire.

## Escalade et escalation

**Comment escalader un ticket ?**
Sur la page du ticket, cliquez sur "Escalader". Fournissez une justification et le niveau de priorité souhaité. L'escalade notifie automatiquement un ingénieur senior. Les escalades abusives peuvent entraîner un rappel des conditions d'utilisation.

**Y a-t-il un support téléphonique ?**
Le support téléphonique est disponible pour les clients Enterprise (numéro dédié fourni dans le contrat). Les clients Business peuvent demander un rappel via le portail (délai max 2h en heures ouvrées).
