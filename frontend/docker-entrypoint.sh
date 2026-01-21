#!/bin/sh
set -e

BACKEND_HOST=${BACKEND_HOST:-backend}
BACKEND_PORT=${BACKEND_PORT:-8000}

echo "Aguardando backend estar disponível em $BACKEND_HOST:$BACKEND_PORT..."

max_attempts=30
attempt=0

until nc -z $BACKEND_HOST $BACKEND_PORT || [ $attempt -ge $max_attempts ]; do
  attempt=$((attempt + 1))
  echo "Tentativa $attempt/$max_attempts: Backend ainda não está disponível. Aguardando..."
  sleep 2
done

if [ $attempt -ge $max_attempts ]; then
  echo "Erro: Backend não ficou disponível após $max_attempts tentativas"
  exit 1
fi

echo "Backend está disponível! Iniciando frontend..."

exec "$@"
