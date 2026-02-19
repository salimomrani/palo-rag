# Ticket TKT-00334 — Notifications Slack envoyées en double

**Statut** : Résolu
**Priorité** : P3 — Normale
**Date d'ouverture** : 2026-01-20 11:05
**Date de résolution** : 2026-01-22 16:15
**Organisation** : InnovateLab (Business)
**Rapporteur** : Sofia Marquez (Admin)
**Ingénieur assigné** : Lucas Dupont

## Description du problème

Depuis la mise à jour 3.41 (déployée le 2026-01-18), toutes les notifications Slack pour les événements `ticket.status_changed` sont reçues deux fois avec un délai de 3-5 secondes entre les deux messages. Les autres types d'événements (ticket.created, ticket.resolved) semblent normaux.

## Impact

L'organisation reçoit ~200 tickets/jour, soit environ 400 messages Slack dupliqués par jour dans le canal `#support-alerts`. Les membres ignorent de plus en plus les alertes, ce qui réduit la réactivité de l'équipe.

## Analyse de cause racine

Dans la version 3.41, un refactoring du système d'événements a introduit deux listeners distincts pour l'événement `ticket.status_changed` : l'ancien listener (non supprimé) et le nouveau. Chaque changement de statut déclenchait donc deux appels Slack.

## Résolution

Suppression du listener dupliqué dans le module d'événements. Ajout d'un test d'intégration vérifiant l'unicité des notifications pour chaque type d'événement.

## Validation

Test effectué : modification de statut de 10 tickets → 10 notifications Slack reçues (1 par ticket). Déployé en version 3.41.2.

## Recommandation

Mettre en place un monitoring du volume de notifications Slack (alerter si > 2x la baseline sur une fenêtre de 5 minutes) pour détecter rapidement ce type de régression.
