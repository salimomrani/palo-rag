# FAQ Produits — PALO Platform

## Plans tarifaires

**Quels sont les plans disponibles ?**
PALO Platform propose trois plans : Starter (gratuit, jusqu'à 3 utilisateurs, 1 Go de stockage), Business (29€/utilisateur/mois, utilisateurs illimités, 100 Go, support prioritaire) et Enterprise (tarif sur mesure, SSO, conformité RGPD avancée, SLA 99,9%).

**Peut-on changer de plan en cours d'abonnement ?**
Oui, la mise à niveau est immédiate. Le rétrogradage prend effet à la prochaine période de facturation. Les données sont conservées dans les deux cas. En cas de rétrogradation vers Starter, les projets dépassant les limites passent en lecture seule.

**Y a-t-il une période d'essai ?**
Le plan Business bénéficie d'un essai gratuit de 14 jours, sans carte bancaire requise. Le plan Enterprise dispose d'un pilote de 30 jours avec un Customer Success Manager dédié.

## Langues supportées

**Quelles langues sont disponibles dans l'interface ?**
L'interface est disponible en français, anglais, espagnol, allemand et portugais (Brésil). La langue est détectée automatiquement depuis les paramètres du navigateur et peut être modifiée dans Paramètres → Profil → Langue.

**Les notifications sont-elles localisées ?**
Oui, les emails et notifications push respectent la langue choisie par chaque utilisateur, indépendamment de la langue du compte organisation.

## Politique de sauvegarde

**À quelle fréquence les données sont-elles sauvegardées ?**
Les sauvegardes automatiques sont effectuées toutes les 6 heures pour les plans Business et Enterprise. Le plan Starter bénéficie d'une sauvegarde quotidienne. Les snapshots sont conservés 30 jours (Starter), 90 jours (Business), 365 jours (Enterprise).

**Comment restaurer une sauvegarde ?**
La restauration s'effectue via Paramètres → Organisation → Sauvegardes. Sélectionnez le snapshot souhaité et cliquez sur "Restaurer". La restauration est disponible en test sur un environnement de staging avant application en production. Délai de restauration : moins de 30 minutes pour les projets inférieurs à 10 Go.

**Les exports manuels sont-ils inclus ?**
Oui, tous les plans permettent l'export en CSV, JSON et PDF depuis chaque module. Les exports planifiés (hebdomadaires/mensuels par email) sont disponibles à partir du plan Business.

## Intégrations

**Quels outils tiers sont intégrables ?**
PALO Platform s'intègre nativement avec Slack, Microsoft Teams, Jira, GitHub, GitLab, Salesforce et Zapier. Les intégrations Slack et Teams sont disponibles sur tous les plans. Jira, GitHub et GitLab nécessitent le plan Business ou supérieur.

**L'API REST est-elle incluse dans tous les plans ?**
L'accès API est inclus dans le plan Business (1000 req/jour) et Enterprise (illimité). Le plan Starter n'inclut pas l'accès API public.
