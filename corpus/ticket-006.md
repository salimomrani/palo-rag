# Ticket TKT-00512 — Intégration GitHub : les PR ne se ferment pas automatiquement

**Statut** : En cours
**Priorité** : P3 — Normale
**Date d'ouverture** : 2026-02-14 10:22
**Dernière mise à jour** : 2026-02-17 09:15
**Organisation** : DevStream Inc (Business)
**Rapporteur** : Carlos Mendez (Editor)
**Ingénieur assigné** : Nadia Petrov

## Description du problème

L'intégration GitHub est configurée pour fermer automatiquement les tickets PALO lorsqu'une Pull Request liée est mergée. La liaison fonctionne (les PR apparaissent bien dans le ticket avec le format `[PALO-XXX]` dans le titre), mais le ticket ne passe pas automatiquement en statut "Résolu" lors du merge.

## Configuration actuelle

- Intégration GitHub activée depuis Paramètres → Intégrations → GitHub
- Organisation GitHub : `devstream-inc`
- Repos connectés : `backend-api`, `frontend-app`, `infra`
- Webhook GitHub configuré et actif (dernière livraison il y a 2h, statut 200)

## Tests effectués

1. PR avec titre `[PALO-523] Fix login bug` → mergée → ticket TKT-00523 : toujours "In Progress"
2. Vérification des logs webhook PALO : l'événement `pull_request.closed` est bien reçu
3. L'événement contient `"merged": true` et `"state": "closed"`

## Hypothèse actuelle

Le parsing du numéro de ticket depuis le titre de la PR semble échouer pour les titres contenant `[PALO-XXX]` (avec crochets). Le format attendu pourrait être `PALO-XXX` sans crochets.

## Workaround

Utiliser le format sans crochets dans les titres de PR : `PALO-523 Fix login bug` (confirmé fonctionnel par tests).

## Prochaines étapes

- Vérification du regex de parsing dans le service d'intégration GitHub
- Si confirmé, correction du regex pour accepter les deux formats `PALO-XXX` et `[PALO-XXX]`
- Mise à jour de la documentation pour indiquer les deux formats supportés
- ETA correctif : 2026-02-21
