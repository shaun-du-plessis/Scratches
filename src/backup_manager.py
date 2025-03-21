import os
import sqlite3
import logging
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('backup_manager')

class BackupManager:
    """
    Manages database backups, integrity checks, and user notifications.
    """
    def __init__(self, db_path="data.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.latest_backup = None
        self.backup_status = {
            "exists": False,
            "is_valid": False,
            "age_days": None,
            "size_diff_percent": None
        }
        
        # Ensure backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def find_latest_backup(self):
        """
        Find the most recent backup file in the backup directory.
        
        Returns:
            str: Path to the latest backup or None if no backups exist
        """
        if not os.path.exists(self.backup_dir):
            return None
            
        backup_files = [f for f in os.listdir(self.backup_dir) 
                       if f.startswith("data_backup_") and f.endswith(".db")]
        
        if not backup_files:
            return None
            
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.backup_dir, f)), reverse=True)
        self.latest_backup = os.path.join(self.backup_dir, backup_files[0])
        return self.latest_backup
    
    def check_backup_integrity(self):
        """
        Check if the latest backup exists and is valid.
        
        Returns:
            dict: Status information about the backup
        """
        # Find the latest backup
        latest_backup = self.find_latest_backup()
        
        # Check if backup exists
        if not latest_backup:
            self.backup_status["exists"] = False
            logger.info("No backup files found")
            return self.backup_status
            
        self.backup_status["exists"] = True
        
        # Check backup age
        backup_time = datetime.fromtimestamp(os.path.getmtime(latest_backup))
        age = datetime.now() - backup_time
        self.backup_status["age_days"] = age.days
        
        # Check if current database exists
        if not os.path.exists(self.db_path):
            self.backup_status["is_valid"] = True  # Backup is our only option
            logger.info(f"No current database found. Latest backup is {age.days} days old.")
            return self.backup_status
        
        # Compare sizes
        current_size = os.path.getsize(self.db_path)
        backup_size = os.path.getsize(latest_backup)
        
        if current_size > 0 and backup_size > 0:
            size_diff = abs(current_size - backup_size) / max(current_size, backup_size) * 100
            self.backup_status["size_diff_percent"] = size_diff
        
        # Basic integrity check - try to open the backup database
        try:
            conn = sqlite3.connect(latest_backup)
            cursor = conn.cursor()
            # Check if we can read from the database
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            
            self.backup_status["is_valid"] = (result and result[0].lower() == "ok")
            if self.backup_status["is_valid"]:
                logger.info(f"Backup integrity check passed. Backup is {age.days} days old.")
            else:
                logger.warning(f"Backup integrity check failed: {result}")
        except Exception as e:
            self.backup_status["is_valid"] = False
            logger.error(f"Error checking backup integrity: {str(e)}")
        
        return self.backup_status
    
    def create_backup(self):
        """
        Create a new backup of the current database.
        
        Returns:
            str: Path to the new backup file or None if backup failed
        """
        if not os.path.exists(self.db_path):
            logger.warning("Cannot create backup: database file does not exist")
            return None
                
        # Create a timestamped backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(self.backup_dir, f"data_backup_{timestamp}.db")
        
        try:
            # Copy the database file to the backup location
            shutil.copy2(self.db_path, backup_filename)
            logger.info(f"Database backed up to {backup_filename}")
            
            # Update latest backup reference
            self.latest_backup = backup_filename
            return backup_filename
        except Exception as e:
            logger.error(f"Database backup failed: {str(e)}")
            return None
    
    def restore_from_backup(self):
        """
        Restore the database from the latest backup.
        
        Returns:
            bool: True if restoration was successful, False otherwise
        """
        if not self.latest_backup or not os.path.exists(self.latest_backup):
            logger.error("Cannot restore: No valid backup found")
            return False
            
        try:
            # Create a backup of the current database first (if it exists)
            if os.path.exists(self.db_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pre_restore_backup = os.path.join(self.backup_dir, f"pre_restore_{timestamp}.db")
                shutil.copy2(self.db_path, pre_restore_backup)
                logger.info(f"Created pre-restore backup at {pre_restore_backup}")
            
            # Copy the backup to the main database location
            shutil.copy2(self.latest_backup, self.db_path)
            logger.info(f"Database restored from {self.latest_backup}")
            return True
        except Exception as e:
            logger.error(f"Database restoration failed: {str(e)}")
            return False
    
    def get_user_notification(self):
        """
        Generate a user notification message based on backup status.
        
        Returns:
            tuple: (notification_message, notification_level)
            where notification_level is one of: "info", "warning", "error"
        """
        if not self.backup_status["exists"]:
            return ("No previous backups found. It's recommended to create a backup after adding data.", "warning")
            
        if not self.backup_status["is_valid"]:
            return ("Your most recent backup appears to be corrupted. Please create a new backup as soon as possible.", "error")
            
        if self.backup_status["age_days"] is not None:
            if self.backup_status["age_days"] > 7:
                return (f"Your most recent backup is {self.backup_status['age_days']} days old. Consider creating a new backup.", "warning")
            elif self.backup_status["age_days"] > 1:
                return (f"Your most recent backup is {self.backup_status['age_days']} days old.", "info")
                
        if self.backup_status["size_diff_percent"] is not None and self.backup_status["size_diff_percent"] > 20:
            return (f"Your current database differs significantly from the backup (size difference: {self.backup_status['size_diff_percent']:.1f}%). Consider creating a new backup.", "warning")
            
        return ("Your backup is up to date.", "info")
