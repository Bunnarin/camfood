import os
import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the database backup script'

    def handle(self, *args, **options):
        # Get the project root directory (where manage.py is located)
        backup_script = settings.BASE_DIR / 'backup.sh'
        
        if not backup_script.exists():
            self.stderr.write(self.style.ERROR(f'Backup script not found at {backup_script}'))
            return
        
        try:
            # Make the script executable
            backup_script.chmod(0o755)
            
            # Run the backup script
            self.stdout.write(self.style.SUCCESS('Starting database backup...'))
            
            # Capture the output in real-time
            process = subprocess.Popen(
                [str(backup_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=settings.BASE_DIR,
                env=os.environ.copy()
            )
            
            # Stream the output
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
