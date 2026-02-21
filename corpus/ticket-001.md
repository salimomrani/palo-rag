# Ticket TKT-00142 — Connexion SSO impossible après migration Okta

**Référence interne** : ticket-001

**Statut** : Résolu
**Priorité** : P1 — Critique
**Date d'ouverture** : 2026-01-08 09:14
**Date de résolution** : 2026-01-08 11:47
**Durée de résolution** : 2h33
**Organisation** : Acme Corp (Enterprise)
**Rapporteur** : Marie Lefort (Admin)
**Ingénieur assigné** : Thomas Remy

## Description du problème

Après la migration de notre instance Okta vers un nouveau tenant (`acme-corp-v2.okta.com`), les utilisateurs ne peuvent plus se connecter via SSO. L'erreur affichée est "SAML assertion validation failed - Issuer mismatch". Les connexions locales (email/mot de passe) fonctionnent normalement.

## Analyse de cause racine

L'Issuer dans la nouvelle configuration SAML d'Okta était `https://acme-corp-v2.okta.com` alors que la configuration PALO référençait l'ancien Issuer `https://acme-corp.okta.com`. La validation SAML échoue si les Issuers ne correspondent pas exactement.

## Résolution

Mise à jour de l'Issuer dans Paramètres → Sécurité → SSO → Configuration SAML de PALO pour correspondre au nouvel Issuer Okta. Après sauvegarde et test, le SSO fonctionne normalement.

## Actions préventives recommandées

1. Toujours tester le SSO sur un compte de test avant une migration d'IdP
2. Planifier les migrations d'IdP en dehors des heures de bureau
3. Conserver les credentials locaux actifs pendant la période de transition
4. Documenter la procédure de migration dans le runbook interne

## Notes techniques

La validation SAML vérifie : Issuer, AudienceRestriction, NotBefore/NotOnOrAfter, Signature. Tous ces champs doivent correspondre exactement à la configuration enregistrée dans PALO. En cas de doute, utiliser le mode "debug SAML" (disponible Enterprise) pour voir l'assertion complète.
