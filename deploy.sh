#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Desplegando stack desde $SCRIPT_DIR"
docker stack deploy -c stack.yml angel_troy

echo "Estado de servicios:"
docker service ps angel_troy_app

echo "Logs del servicio app:"
docker service logs --tail=50 angel_troy_app
