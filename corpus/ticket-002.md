# Ticket TKT-00287 — Export CSV tronqué pour les projets avec plus de 5000 tickets

**Statut** : Résolu
**Priorité** : P2 — Haute
**Date d'ouverture** : 2026-01-15 14:22
**Date de résolution** : 2026-01-17 10:30
**Durée de résolution** : ~44h
**Organisation** : TechStart SAS (Business)
**Rapporteur** : Jean-Pierre Morin (Editor)
**Ingénieur assigné** : Amina Bouchard

## Description du problème

L'export CSV via l'interface (Tickets → Exporter → CSV) ne retourne que 5000 lignes exactement, même quand le projet contient 12 000 tickets. Le fichier téléchargé s'arrête brusquement sans message d'erreur. L'export via l'API REST avec pagination retourne tous les tickets correctement.

## Reproduction

1. Projet avec > 5000 tickets (statuts mixtes)
2. Tickets → Exporter → CSV → Télécharger
3. Ouvrir le fichier : exactement 5000 lignes (+ en-tête)
4. Comparer avec GET /api/tickets?project_id=xxx&limit=100 : 12 000 tickets disponibles

## Analyse de cause racine

Un hard-limit de 5000 enregistrements était appliqué silencieusement dans le service d'export UI, héritage d'une limitation de performance de 2024 qui n'avait pas été correctement supprimée lors de la mise à niveau des serveurs d'export en décembre 2025.

## Résolution

Suppression du hard-limit dans le service d'export. Le nouveau comportement exporte jusqu'à 100 000 enregistrements, avec streaming du fichier pour éviter les timeouts. Pour les exports > 100 000 lignes, l'export est mis en file d'attente et envoyé par email.

## Workaround temporaire (pendant le correctif)

Utiliser l'API REST avec pagination :
```bash
curl -H "Authorization: Bearer {token}" \
  "https://api.palo.io/v1/tickets?project_id={id}&limit=100&offset=0" | jq '.data'
```

## Statut déploiement

Correctif déployé en production le 2026-01-17 à 10:00. Version : 3.42.1.
