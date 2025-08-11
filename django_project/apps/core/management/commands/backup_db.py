# myapp/management/commands/run_shell_script.py
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs a specified shell script.'

    def handle(self, *args, **options):
        script_path = settings.BASE_DIR / 'backup.sh'

        try:
            # Use subprocess.run to execute the shell script
            # capture_output=True captures stdout and stderr
            # text=True decodes stdout/stderr as text
            # check=True raises CalledProcessError if the command returns a non-zero exit code
            result = subprocess.run(
                [script_path],  # Or just [script_path] if the script is executable
                capture_output=True,
                text=True,
                check=True,
                shell=False  # Set to True if you need shell features like wildcards, pipes, etc.
            )
            self.stdout.write(self.style.SUCCESS(f'Script executed successfully: {script_path}'))
            if result.stdout:
                self.stdout.write(f'STDOUT:\n{result.stdout}')
            if result.stderr:
                self.stderr.write(f'STDERR:\n{result.stderr}')

        except subprocess.CalledProcessError as e:
            raise CommandError(f'Error executing script: {script_path}\n'
                                f'Return Code: {e.returncode}\n'
                                f'STDOUT: {e.stdout}\n'
                                f'STDERR: {e.stderr}')
        except FileNotFoundError:
            raise CommandError(f'Script not found: {script_path}')
        except Exception as e:
            raise CommandError(f'An unexpected error occurred: {e}')