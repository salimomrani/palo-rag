# Ticket TKT-00455 — Performance dégradée sur le tableau de bord avec > 50 projets

**Statut** : Résolu
**Priorité** : P3 — Normale
**Date d'ouverture** : 2026-02-07 15:30
**Date de résolution** : 2026-02-12 11:00
**Organisation** : GlobalOps Group (Enterprise)
**Rapporteur** : Fatima Okonkwo (Admin)
**Ingénieur assigné** : Marco Ferretti

## Description du problème

Le tableau de bord principal met plus de 8 secondes à charger lorsque l'organisation a plus de 50 projets actifs. Pour GlobalOps Group qui gère 127 projets, le chargement prend parfois 12-15 secondes. L'objectif de performance est < 2s P95.

## Données de performance collectées

| Nombre de projets | Temps de chargement (médiane) |
|-------------------|-------------------------------|
| < 20 | 0.8s |
| 20-50 | 2.3s |
| 51-100 | 6.1s |
| > 100 | 12.4s |

## Analyse de cause racine

Pour chaque projet affiché sur le tableau de bord, une requête SQL séparée était effectuée pour récupérer les statistiques (nombre de tickets ouverts, membres actifs, dernière activité). Avec 127 projets, cela générait 127 requêtes SQL séquentielles au chargement de la page (N+1 query problem).

## Résolution

Remplacement des N+1 queries par une unique requête SQL avec agrégations JOIN. Ajout d'un cache Redis (TTL 5 minutes) pour les statistiques de projet. Implémentation du lazy-loading : seuls les 20 premiers projets sont chargés immédiatement, les suivants au scroll.

## Résultats après correctif

| Nombre de projets | Temps de chargement (après) |
|-------------------|-----------------------------|
| 127 projets | 0.9s |

Déployé en version 3.43.0. Les clients avec > 50 projets bénéficient automatiquement du correctif.
