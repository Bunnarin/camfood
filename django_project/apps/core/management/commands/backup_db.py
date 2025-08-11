import os
import subprocess
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the database backup script'

    def handle(self, *args, **options):
        # Try multiple possible locations for the backup script
        possible_locations = [
            Path(settings.BASE_DIR).parent / 'backup.sh',  # For Docker (in /app/backup.sh)
            Path(settings.BASE_DIR) / 'backup.sh',         # For local development
            Path('/app/backup.sh'),                        # Fallback for Docker
            'backup.sh',                                   # Last resort, will use PATH
        ]
        
        backup_script = None
        for location in possible_locations:
            if isinstance(location, str):
                # If it's a string (like 'backup.sh'), use which to find it in PATH
                path = shutil.which(location)
                if path:
                    backup_script = Path(path)
                    break
            elif location.exists():
                backup_script = location
                break
        
        if not backup_script or not backup_script.exists():
            error_msg = f'Backup script not found. Tried: {[str(loc) for loc in possible_locations if str(loc) != "backup.sh"]}'
            self.stderr.write(self.style.ERROR(error_msg))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Using backup script at: {backup_script}'))
        
        try:
            # Make the script executable
            backup_script.chmod(0o755)
            
            # Get the directory containing the script
            script_dir = backup_script.parent
            
            # Run the backup script
            self.stdout.write(self.style.SUCCESS('Starting database backup...'))
            
            # Set up environment with current environment plus PYTHONUNBUFFERED
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            # Run the script
            process = subprocess.Popen(
                [str(backup_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(script_dir),  # Run from the script's directory
                env=env,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Stream the output in real-time
            for line in process.stdout:
                self.stdout.write(line.strip())
            
            # Wait for the process to complete
            return_code = process.wait()
            
            if return_code == 0:
                self.stdout.write(self.style.SUCCESS('Backup completed successfully'))
            else:
                self.stderr.write(self.style.ERROR(f'Backup failed with return code {return_code}'))
                
        except Exception as e:
            logger.exception('Error during backup')
            self.stderr.write(self.style.ERROR(f'Error during backup: {str(e)}'))
            raise
