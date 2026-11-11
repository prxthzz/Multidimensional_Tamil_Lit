import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_FILE = BASE_DIR / "data" / "production_tamil_knowledge.db"

def restore(backup_path_str: str):
    backup_path = Path(backup_path_str)
    if not backup_path.exists():
        print(f"Error: Backup file '{backup_path}' does not exist.")
        return False
        
    shutil.copy2(backup_path, DB_FILE)
    print(f"Database successfully restored from: {backup_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python restore_database.py <path_to_backup.db>")
    else:
        restore(sys.argv[1])
