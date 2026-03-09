#!/bin/bash
# Hook: SessionStart (once: true) — injects PALO constitution into context once per session.
# Avoids having to read constitution.md manually on every architectural decision.

CONSTITUTION="/Users/salimomrani/code/_Autres/PALO/.specify/memory/constitution.md"

if [ -f "$CONSTITUTION" ]; then
  echo "=== PALO Architecture Constitution (auto-loaded) ==="
  cat "$CONSTITUTION"
  echo "=== End Constitution ==="
fi
