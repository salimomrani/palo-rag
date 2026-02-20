# Spécification Authentification & Sécurité — PALO Platform

## Méthodes d'authentification supportées

### Authentification locale (email + mot de passe)
Disponible sur tous les plans. Politique de mots de passe : minimum 12 caractères, au moins une majuscule, un chiffre et un caractère spécial. Rotation forcée tous les 90 jours pour les comptes Admin et Owner. Historique des 10 derniers mots de passe (réutilisation interdite).

### SSO SAML 2.0
Disponible sur le plan Enterprise uniquement. Fournisseurs pré-configurés : Okta, Azure Active Directory, Google Workspace, OneLogin, Ping Identity. Configuration via Paramètres → Sécurité → SSO. Requiert un certificat X.509 et les endpoints IdP (SSO URL, SLO URL). Le provisioning automatique des comptes (SCIM 2.0) est inclus avec le SSO Enterprise.

### SSO OAuth 2.0 / OIDC
Disponible à partir du plan Business. Fournisseurs supportés : Google, Microsoft, GitHub. Scope minimal requis : `openid email profile`. Les tokens sont validés côté serveur à chaque requête.

## Authentification à deux facteurs (2FA)

### TOTP (Time-based One-Time Password)
Méthode recommandée. Compatible avec Google Authenticator, Authy, 1Password, Bitwarden. Activation dans Profil → Sécurité → Configurer 2FA. Des codes de récupération (10 codes à usage unique) sont générés à l'activation — à conserver en lieu sûr.

### SMS OTP
Disponible comme méthode alternative. Numéros supportés : France (+33), Belgique (+32), Suisse (+41), Canada (+1), US (+1). Les SMS OTP sont valides 5 minutes. Maximum 5 tentatives avant blocage temporaire (15 minutes).

### 2FA obligatoire
Les Admins et Owners peuvent imposer le 2FA à tous les membres de l'organisation via Paramètres → Sécurité → Politique 2FA. Les membres sans 2FA configuré ont 7 jours pour se mettre en conformité avant restriction d'accès.

## Gestion des sessions

Les sessions JWT expirent après 8 heures d'inactivité (configurable entre 1h et 24h). Les tokens de rafraîchissement sont valides 30 jours. Déconnexion de toutes les sessions active depuis Profil → Sécurité → Sessions actives. Les sessions sont listées avec IP, user-agent et dernière activité.

## Politique de verrouillage de compte

Après 5 tentatives de connexion échouées consécutives, le compte est verrouillé temporairement pendant 15 minutes. Après 10 tentatives sur 24h, verrouillage de 24h avec notification email. Les Admins peuvent déverrouiller manuellement depuis le panneau de gestion des membres.

## Mots de passe et réinitialisation

Réinitialisation par email : lien valide 30 minutes, usage unique. L'email est envoyé à l'adresse de secours si l'email principal est inaccessible. En cas de perte totale d'accès, contacter le support avec justification d'identité (délai de traitement : 24-48h).

## Journaux d'audit sécurité

Tous les événements de sécurité sont journalisés (connexions, échecs, changements de mot de passe, activations/désactivations 2FA, modifications des paramètres SSO). Rétention : 1 an (Business), 3 ans (Enterprise). Exportables via Paramètres → Sécurité → Journaux d'audit.
