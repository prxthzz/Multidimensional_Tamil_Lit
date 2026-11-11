import shutil
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_FILE = BASE_DIR / "data" / "production_tamil_knowledge.db"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    target_backup = BACKUP_DIR / f"db_backup_{timestamp}.db"
    
    if DB_FILE.exists():
        shutil.copy2(DB_FILE, target_backup)
        print(f"Backup created successfully: {target_backup}")
        return str(target_backup)
    else:
        print("Production database file not found. Nothing to backup.")
        return None

if __name__ == "__main__":
    backup()
