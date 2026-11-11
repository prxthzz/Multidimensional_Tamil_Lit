# Disaster Recovery & Backup Plan

## 1. Backup Strategy
- **Frequency**: Daily automated database snapshots.
- **Location**: `backups/db_backup_YYYYMMDD_HHMMSS.db`

## 2. Backup Command
```bash
python scripts/backup_database.py
```

## 3. Restore Command
```bash
python scripts/restore_database.py backups/db_backup_20260927_125014.db
```

## 4. Recovery Objectives
- **RPO (Recovery Point Objective)**: 24 Hours.
- **RTO (Recovery Time Objective)**: 15 Minutes.
