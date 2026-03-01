#!/usr/bin/env bash
# Reset complet : ChromaDB + tables PostgreSQL + logs
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. ChromaDB
echo "Suppression ChromaDB..."
rm -rf "$SCRIPT_DIR/backend/chroma_data"

# 2. Logs
echo "Suppression logs..."
rm -rf "$SCRIPT_DIR/backend/logs"

# 3. PostgreSQL
echo "Reset tables PostgreSQL..."
docker exec palo-db-1 psql -U palo -d palo_rag -c "
DO \$\$ BEGIN
  IF EXISTS (SELECT FROM pg_tables WHERE tablename = 'documents') THEN
    TRUNCATE documents, query_logs, evaluation_results RESTART IDENTITY CASCADE;
    RAISE NOTICE 'Tables vidées.';
  ELSE
    RAISE NOTICE 'Tables absentes, rien à faire.';
  END IF;
END \$\$;"

echo "Reset terminé. Lance l'ingestion : cd backend && .venv/bin/python scripts/ingest_corpus.py"
