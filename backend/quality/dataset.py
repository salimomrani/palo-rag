"""Reference Q&A dataset for quality evaluation (15 questions covering all corpus docs)."""

REFERENCE_DATASET = [
    {
        "question": "Quels sont les produits proposés par Palo IT ?",
        "expected_source": "faq-produits.md",
    },
    {
        "question": "Comment contacter le support technique ?",
        "expected_source": "faq-support.md",
    },
    {
        "question": "Quelles sont les étapes d'onboarding pour un nouveau client ?",
        "expected_source": "faq-onboarding.md",
    },
    {
        "question": "Quels sont les endpoints disponibles dans l'API v1 ?",
        "expected_source": "spec-api-v1.md",
    },
    {
        "question": "Comment fonctionne l'authentification dans le système ?",
        "expected_source": "spec-auth.md",
    },
    {
        "question": "Comment sont envoyées les notifications aux utilisateurs ?",
        "expected_source": "spec-notifications.md",
    },
    {
        "question": "Comment configurer un webhook pour recevoir des événements ?",
        "expected_source": "spec-webhooks.md",
    },
    {
        "question": "Quel est le problème décrit dans le ticket 001 ?",
        "expected_source": "ticket-001.md",
    },
    {
        "question": "Quelle est la résolution du ticket 002 ?",
        "expected_source": "ticket-002.md",
    },
    {
        "question": "Quel bug a été signalé dans le ticket 003 ?",
        "expected_source": "ticket-003.md",
    },
    {
        "question": "Quelle fonctionnalité est demandée dans le ticket 004 ?",
        "expected_source": "ticket-004.md",
    },
    {
        "question": "Quel est le contenu du ticket 005 ?",
        "expected_source": "ticket-005.md",
    },
    {
        "question": "Quelle est la priorité du ticket 006 ?",
        "expected_source": "ticket-006.md",
    },
    {
        "question": "Quelles données personnelles sont collectées et comment sont-elles protégées ?",
        "expected_source": "politique-donnees.md",
    },
    {
        "question": "Quelles sont les mesures de sécurité mises en place pour protéger les accès ?",
        "expected_source": "politique-securite.md",
    },
]
