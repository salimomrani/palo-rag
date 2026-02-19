# Politique de Sécurité — PALO Platform

## Classification des données

PALO Platform classe les données en quatre niveaux :

**Niveau 1 — Public** : Documentation publique, blog, pages marketing. Aucune restriction.

**Niveau 2 — Interne** : Données opérationnelles non sensibles (métriques d'usage agrégées, logs de performance). Accès limité aux employés PALO.

**Niveau 3 — Confidentiel** : Données clients (contenu tickets, documents, commentaires), données personnelles des utilisateurs. Chiffrement au repos et en transit obligatoire. Accès sur besoin d'en connaître.

**Niveau 4 — Strictement confidentiel** : Credentials, clés de chiffrement, données de paiement, configurations SSO. Accès restreint à l'équipe sécurité. Journalisation de tous les accès.

## Contrôles techniques

### Chiffrement
- **En transit** : TLS 1.3 minimum (TLS 1.2 accepté temporairement). Certificats renouvelés automatiquement via Let's Encrypt.
- **Au repos** : AES-256 pour les données stockées. Les clés de chiffrement sont gérées via AWS KMS avec rotation annuelle.
- **Mots de passe** : Bcrypt (cost factor 12) pour les mots de passe utilisateurs.

### Accès et identité
- Principe du moindre privilège appliqué à tous les accès systèmes
- MFA obligatoire pour tous les accès à l'infrastructure (Bastion SSH, AWS Console, CI/CD)
- Revue trimestrielle des accès et suppression des comptes inactifs > 90 jours
- PAM (Privileged Access Management) pour les accès root et administrateur

### Réseau
- WAF (Web Application Firewall) devant tous les endpoints publics
- DDoS protection via Cloudflare
- Segmentation réseau : prod/staging/dev isolés
- Pas d'accès SSH direct en production (Jump host obligatoire avec audit log)

## Gestion des incidents de sécurité

### Processus de réponse
1. **Détection** : Monitoring SIEM 24/7 (alertes automatiques sur comportements anormaux)
2. **Classification** : Critique (données exposées), Haute (accès non autorisé), Normale (tentative bloquée)
3. **Confinement** : Isolation des systèmes affectés dans les 15 minutes (incidents critiques)
4. **Investigation** : Analyse forensique, identification de la cause racine
5. **Remédiation** : Correctif, durcissement, test de validation
6. **Post-mortem** : Document partagé en interne dans les 5 jours ouvrés

### Contacts sécurité
- **Email** : security@palo.io
- **Bug bounty** : hackerone.com/palo-platform (récompenses jusqu'à 10 000€)
- **Signalement urgent** : Ligne directe sécurité disponible 24/7 pour les clients Enterprise

## Tests de sécurité

- Pentest externe annuel par un cabinet certifié CREST
- Scan de vulnérabilités hebdomadaire (DAST sur les endpoints publics)
- Revue de code sécurité (SAST) intégrée dans la CI/CD pipeline
- Audit des dépendances (CVE) : alertes automatiques et patch dans les 48h pour les vulnérabilités critiques

## Conformité

PALO Platform est conforme à : ISO 27001 (certification en cours), SOC 2 Type II (rapport disponible sous NDA), RGPD (voir politique données), PCI-DSS Niveau 4 (paiements via Stripe, hors scope direct).
