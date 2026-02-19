# Guide d'Onboarding — PALO Platform

## Étape 1 : Création du compte

Rendez-vous sur app.palo.io/signup. Renseignez votre email professionnel, un mot de passe (minimum 12 caractères, avec majuscule, chiffre et symbole) et le nom de votre organisation. Une vérification par email est envoyée immédiatement — vérifiez vos spams si elle n'arrive pas dans les 2 minutes.

Une fois le compte activé, vous accédez au tableau de bord avec un workspace "Sandbox" pré-configuré contenant des données d'exemple pour explorer les fonctionnalités sans risque.

## Étape 2 : Configuration de l'organisation

Dans Paramètres → Organisation, renseignez :
- **Nom de l'organisation** : visible dans les emails et rapports
- **Fuseau horaire** : utilisé pour les notifications et les planifications
- **Domaine autorisé** : ex. `votre-entreprise.com` pour activer l'auto-provisioning des membres
- **Logo** : formats PNG/SVG, dimensions recommandées 200×60px

Activez le SSO si votre organisation utilise un fournisseur d'identité (Okta, Azure AD, Google Workspace) — voir la section "Authentification SSO" dans la documentation technique.

## Étape 3 : Invitation des membres

Allez dans Paramètres → Membres → Inviter. Vous pouvez :
- **Invitation individuelle** : entrez l'email et choisissez le rôle (Viewer, Editor, Admin)
- **Invitation en masse** : importez un CSV avec colonnes email, role, team
- **Lien d'invitation** : générez un lien valide 7 jours pour partage direct

Les rôles disponibles : Viewer (lecture seule), Editor (création et modification), Admin (accès complet incluant facturation et paramètres), Owner (1 seul par organisation).

## Étape 4 : Connexion des intégrations

Pour intégrer Slack : Paramètres → Intégrations → Slack → Connecter. Autorisez l'application PALO dans votre workspace Slack. Choisissez le canal par défaut pour les notifications.

Pour intégrer Jira : Paramètres → Intégrations → Jira. Entrez l'URL de votre instance Jira et vos credentials API. Configurez la synchronisation bidirectionnelle des tickets si souhaitée.

Intégrations disponibles en natif : Slack, Teams, Jira, GitHub, GitLab, Salesforce, Zapier, PagerDuty.

## Étape 5 : Premier projet

Cliquez sur "+ Nouveau Projet" depuis le tableau de bord. Donnez un nom au projet, sélectionnez un template (Projet Logiciel, Opérations, Marketing, Personnalisé) et assignez les membres. Les templates incluent des workflows prédéfinis que vous pouvez adapter.

La configuration de base est terminée. Pour aller plus loin :
- **Import de données** : Fichiers → Importer (CSV, Jira, Trello, Asana, Linear)
- **Automatisations** : Paramètres Projet → Automatisations (déclencheurs basés sur des événements)
- **Webhooks** : Paramètres → Développeurs → Webhooks (pour vos intégrations custom)

## Ressources supplémentaires

- Documentation complète : docs.palo.io
- Tutoriels vidéo : palo.io/academy
- Communauté : community.palo.io (forum, FAQ, retours d'expérience)
- Support : support.palo.io ou Slack `/palo-support`

L'équipe Customer Success vous contactera dans les 48h suivant votre inscription pour planifier une session d'onboarding personnalisée (30 min, optionnel mais recommandé pour les plans Business et Enterprise).
