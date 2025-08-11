import os
import subprocess
import sys
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the database backup script with detailed debugging'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug output',
        )

    def debug_print(self, message, force=False):
        """Print debug messages if debug is enabled"""
        if self.debug or force:
            self.stdout.write(self.style.WARNING(f"[DEBUG] {message}"))

    def find_script(self, script_name):
        """Search for the script in common locations"""
        possible_paths = [
            Path(settings.BASE_DIR).parent / script_name,  # /app/backup.sh in Docker
            Path(settings.BASE_DIR) / script_name,         # Project root
            Path('/app') / script_name,                    # Common Docker app dir
            Path.cwd() / script_name,                      # Current working directory
        ]
        
        self.debug_print(f"Searching for {script_name} in:")
        for path in possible_paths:
            exists = path.exists()
            self.debug_print(f"- {path}: {'FOUND' if exists else 'not found'}")
            if exists:
                return path
        return None

    def handle(self, *args, **options):
        self.debug = options.get('debug', False)
        script_name = 'backup.sh'
        
        # Debug environment
        self.debug_print("\n=== Environment Debug ===")
        self.debug_print(f"Current working directory: {Path.cwd()}")
        self.debug_print(f"BASE_DIR: {settings.BASE_DIR}")
        self.debug_print(f"Python executable: {sys.executable}")
        
        # Debug file system
        self.debug_print("\n=== Directory Contents ===")
        for path in [Path(settings.BASE_DIR).parent, settings.BASE_DIR, Path('/app')]:
            if path.exists():
                try:
                    contents = "\n  " + "\n  ".join(str(p) for p in path.iterdir())
                    self.debug_print(f"Contents of {path}:{contents}")
                except Exception as e:
                    self.debug_print(f"Could not list {path}: {str(e)}")
        
        # Find the script
        self.debug_print("\n=== Searching for Script ===")
        script_path = self.find_script(script_name)
        
        if not script_path:
            error_msg = f"{script_name} not found in any standard location"
            self.stderr.write(self.style.ERROR(error_msg))
            return
            
        self.debug_print(f"\n=== Script Found ===")
        self.debug_print(f"Using script at: {script_path}")
        self.debug_print(f"Script exists: {script_path.exists()}")
        self.debug_print(f"Script is file: {script_path.is_file()}")
        self.debug_print(f"Script permissions: {oct(script_path.stat().st_mode)[-3:]}")
        
        try:
            # Make the script executable
            script_path.chmod(0o755)
            
            self.stdout.write(self.style.SUCCESS(f'Starting backup with script: {script_path}'))
            
            # Run the script with real-time output
            process = subprocess.Popen(
                [str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
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
            self.stderr.write(self.style.ERROR(f'Error during backup: {str(e)}'))
            if self.debug:
                import traceback
                self.stderr.write(traceback.format_exc())
            raise