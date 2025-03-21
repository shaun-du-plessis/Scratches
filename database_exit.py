import os
import sqlite3
import zipfile
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database_exit")

def backup_database(db_path="data.db", backup_dir="backups"):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"data_backup_{timestamp}.db")
    try:
        shutil.copy2(db_path, backup_file)
        logger.info(f"Database backed up to {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return None

def compress_database(db_path="data.db"):
    zip_path = f"{db_path}.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_path, arcname=os.path.basename(db_path))
        logger.info(f"Database compressed to {zip_path}")
        return zip_path
    except Exception as e:
        logger.error(f"Compression failed: {str(e)}")
        return None

def close_database_connections():
    # If you actively manage database connections, close them here.
    try:
        logger.info("Closing database connections (if any)")
        # For this example, we assume no long-lived connections.
        return True
    except Exception as e:
        logger.error(f"Error closing connections: {str(e)}")
        return False

def safe_exit():
    logger.info("Starting safe exit procedure")
    close_database_connections()
    backup_database()  # Optionally force backup here
    compress_database()
    logger.info("Safe exit completed")