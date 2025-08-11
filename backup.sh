#!/bin/sh

# Exit on error
set -e

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Configuration with default values
export DB_NAME=${DB_NAME}
export DB_USER=${DB_USER}
export DB_PASSWORD=${DB_PASSWORD}
export DB_HOST=postgresql
export DB_PORT=5432
export BACKUP_DIR=backup
export RETENTION_DAYS=1


# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup file name with timestamp
TIMESTAMP=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
BACKUP_FILE="${DB_NAME}_${TIMESTAMP}.dump"
FULL_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Start backup
log "Starting backup of database: $DB_NAME"

# Set PGPASSWORD as environment variable for psql/pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Create backup
if pg_dump -Fc -Z 9 -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" > "$FULL_PATH"; then
    # Set proper permissions
    chmod 600 "$FULL_PATH"
    
    log "Backup completed successfully: $FULL_PATH"
    
    # Find and delete old backups
    DELETED=$(find "$BACKUP_DIR" -name "${DB_NAME}_*.dump" -type f -mtime +"$RETENTION_DAYS" -delete -print | wc -l)
    
    if [ "$DELETED" -gt 0 ]; then
        log "Deleted $DELETED old backup(s)"
    fi
    
    # List current backups
    log "Current backups in $BACKUP_DIR:"
    ls -lh "$BACKUP_DIR"/"${DB_NAME}"_*.dump 2>/dev/null || echo "No backup files found"
else
    log "ERROR: Backup failed"
    exit 1
fi

exit 0