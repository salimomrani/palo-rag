# Spécification Système de Notifications — PALO Platform

## Canaux de notification disponibles

### Email
Canal par défaut pour tous les utilisateurs. Les emails sont envoyés depuis `notifications@palo.io`. Chaque utilisateur peut configurer ses préférences dans Profil → Notifications → Email. Support du mode "digest" : regroupement des notifications sur des périodes de 1h, 4h, 24h ou désactivation des notifications temps réel.

### Notifications push navigateur
Disponibles sur Chrome, Firefox, Safari, Edge. Activation en cliquant sur le bouton "Activer les notifications" dans le header de l'application. Requiert l'autorisation du navigateur. Les notifications push fonctionnent même lorsque l'onglet est inactif.

### Slack
Après configuration de l'intégration Slack (voir guide onboarding), les notifications peuvent être routées vers des canaux spécifiques. Configuration par événement : certains événements peuvent aller vers `#general`, d'autres vers `#alertes-critiques`.

### Microsoft Teams
Similaire à Slack. Intégration via webhook entrant Teams. Supporte les cartes adaptatives (Adaptive Cards) pour un affichage enrichi des notifications de tickets et d'incidents.

### Webhooks personnalisés
Pour les intégrations custom, configurez un webhook (URL HTTPS + secret HMAC) dans Paramètres → Développeurs → Webhooks. Le payload est signé et inclut un `event_type`, `timestamp`, `organization_id` et les données de l'événement.

## Types d'événements et déclencheurs

| Événement | Description | Canaux disponibles |
|-----------|-------------|-------------------|
| ticket.created | Nouveau ticket créé | Email, Slack, Teams, Webhook |
| ticket.assigned | Ticket assigné à un membre | Email, Push, Slack |
| ticket.status_changed | Changement de statut | Email, Push, Slack, Webhook |
| ticket.commented | Nouveau commentaire | Email, Push |
| ticket.resolved | Ticket résolu | Email, Slack, Webhook |
| project.member_added | Nouveau membre ajouté | Email |
| system.incident | Incident de service | Email, Push, Slack, Teams, Webhook |
| quota.warning | 80% du quota atteint | Email, Push |
| quota.exceeded | Quota dépassé | Email, Push, Slack |

## Limites de notifications

**Plan Starter** : 500 notifications/mois (email uniquement, pas de Slack ni Teams)
**Plan Business** : 50 000 notifications/mois tous canaux
**Plan Enterprise** : illimité

Les notifications dépassant le quota Starter sont mises en file d'attente et envoyées le mois suivant. Un email d'avertissement est envoyé à 80% du quota.

## Personnalisation des templates

Les templates email sont personnalisables pour le plan Enterprise (logo, couleurs, footer). Les variables disponibles dans les templates : `{{user_name}}`, `{{organization_name}}`, `{{ticket_id}}`, `{{ticket_title}}`, `{{ticket_url}}`, `{{event_timestamp}}`.

## Préférences utilisateur

Chaque utilisateur contrôle ses propres préférences dans Profil → Notifications. Les Admins peuvent définir des politiques de notification au niveau organisation (ex. : forcer les notifications critiques), qui s'appliquent en plus des préférences individuelles. Les utilisateurs ne peuvent pas désactiver les notifications obligatoires définies par l'organisation.

## Fréquence et anti-spam

Un mécanisme anti-spam regroupe automatiquement les événements identiques sur une fenêtre de 5 minutes (ex. : 20 commentaires sur le même ticket = 1 notification groupée). La fréquence maximale est de 60 notifications push/heure par utilisateur. Au-delà, les notifications sont groupées dans un résumé horaire.
