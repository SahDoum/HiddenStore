# Log function for better readability
log() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Applying database migrations..."
alembic upgrade head

log "Starting application..."
uvicorn apps.server.router:app --host 0.0.0.0 --port 8000
