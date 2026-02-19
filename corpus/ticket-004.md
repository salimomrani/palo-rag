# Ticket TKT-00401 — 2FA SMS non reçu sur numéros belges

**Statut** : En cours
**Priorité** : P2 — Haute
**Date d'ouverture** : 2026-02-03 09:45
**Dernière mise à jour** : 2026-02-05 14:20
**Organisation** : BelgiumFintech SA (Business)
**Rapporteur** : Pierre Vandenberghe (Owner)
**Ingénieur assigné** : Ingrid Santos

## Description du problème

Les utilisateurs belges avec des numéros au format `+32 4X XX XX XX` (opérateurs Proximus, Base, Orange) ne reçoivent plus les SMS OTP depuis le 2026-01-31. Les utilisateurs français et suisses ne sont pas affectés. Les codes TOTP (Google Authenticator) fonctionnent normalement pour les utilisateurs ayant configuré cette méthode.

## Impact

12 utilisateurs de BelgiumFintech SA sont bloqués pour se connecter (2FA uniquement SMS, sans TOTP configuré). Les connexions depuis des IPs de confiance (bureau) fonctionnent grâce au "remember this device" encore actif.

## Investigations en cours

- Le fournisseur SMS (Twilio) confirme que les messages sont bien envoyés depuis leur côté (statut "delivered" dans leur dashboard)
- Tests effectués depuis 3 opérateurs belges différents : aucun SMS reçu
- Hypothèse actuelle : filtrage anti-spam au niveau des agrégateurs SMS belges post-01/31

## Workaround proposé au client

1. Se connecter depuis une IP de confiance (bureau) avec "remember this device"
2. Une fois connecté, activer TOTP via Profil → Sécurité → Configurer 2FA (Google Authenticator)
3. Désactiver le SMS OTP une fois TOTP activé

## Prochaines étapes

- Escalade vers Twilio pour investigation agrégateur belge (ETA : 48h)
- Évaluation d'un second fournisseur SMS pour les numéros +32 comme fallback
- Date de résolution estimée : 2026-02-10
