import os
from django.core.management.base import BaseCommand
from django.conf import settings
from nativo_english.db_scripts_automate.models import ExecutedSQLScript
import glob
import time
from django.db import connection

class Command(BaseCommand):
    help = 'Automatically generates migration file for running SQL scripts'

    def handle(self, *args, **kwargs):
        # Fetch all migrations from the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT app, name FROM django_migrations WHERE app = 'db_scripts_automate' ORDER BY app, name ")
            all_migrations = cursor.fetchall()  # Returns a list of (app_name, migration_name)

        # Format dependencies as a Python list of tuples
        formatted_dependencies = ",\n        ".join(
            [f"('{app}', '{name}')" for app, name in all_migrations]
        )

        migration_counter = int(all_migrations[-1][1].split('_')[0])

        # Define the directory for migration files inside the app
        migration_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'migrations'
        )
        print(migration_dir)
        
        # Create the directory if it does not exist
        if not os.path.exists(migration_dir):
            os.makedirs(migration_dir)

        # Get the path to the db_scripts folder located at the root of the project
        project_root = os.path.dirname(os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ))  # 3 levels up from current location
        
        db_scripts_folder = os.path.join(project_root, 'db_scripts', settings.BUILD_VERSION, 'deploy')
        
        # Get all SQL files recursively in the deploy folder
        sql_files = glob.glob(os.path.join(db_scripts_folder, '**', '*.sql'), recursive=True)

        # Debugging
        print(f"SQL Files Path: {db_scripts_folder}")
        print(f"SQL Files Found: {sql_files}")

        if not sql_files:
            self.stdout.write(self.style.SUCCESS("No SQL files found to migrate."))
            return
        
         # Check if any SQL file is not already executed
        for sql_file in sql_files:
            file_name = os.path.basename(sql_file)  # Get the file name only
            build_number = settings.BUILD_VERSION  # Current build number from settings
        
            # Check if an entry exists in the database for this file and build number
            if ExecutedSQLScript.objects.filter(file_name=file_name, build_number=build_number).exists():
                # If any file is not executed, return True (migration file should be created)
                print("NO MIGRATION FILE REQUIRED FOR DB SCIRPTS")
                return

        # Generate a unique migration file name (e.g., with timestamp)
        migration_file_name = f"{(migration_counter+1):04}_auto_run_sql_scripts.py"
        migration_file_path = os.path.join(migration_dir, migration_file_name)

        # Write migration content
        migration_file_content = f'''
# Generated migration to run SQL scripts

from django.db import migrations
from django.conf import settings
import os
import glob
from nativo_english.db_scripts_automate.models import ExecutedSQLScript

def run_sql_scripts(apps, schema_editor):

    project_root = os.path.dirname(os.path.dirname(
            os.path.dirname(__file__)
        ))
    # Path to the db_scripts folder from settings.py
    db_scripts_folder = os.path.join(project_root, 'db_scripts', settings.BUILD_VERSION, 'deploy')

    print(db_scripts_folder)
    # Get all SQL files recursively in the deploy folder
    sql_files = glob.glob(os.path.join(db_scripts_folder, '*.sql'), recursive=True)
    
    print(sql_files)
    
    for sql_file in sql_files:
        # Check if this script has already been executed
        if not ExecutedSQLScript.objects.filter(file_name=os.path.basename(sql_file), build_number=settings.BUILD_VERSION).exists():
            # Check if file exists before reading
            if not os.path.exists(sql_file):
                print("SQL file not found: " + sql_file)
                continue
            
            # Open the SQL file and read its content
            with open(sql_file, 'r') as file:
                sql_script = file.read()

            # Execute SQL script
            with schema_editor.connection.cursor() as cursor:
                cursor.execute(sql_script)

            # Mark the script as executed by adding an entry to the database
            ExecutedSQLScript.objects.create(file_name=os.path.basename(sql_file), build_number=settings.BUILD_VERSION)
            print("Executed SQL script: " + os.path.basename(sql_file))

class Migration(migrations.Migration):

    dependencies = [
        {formatted_dependencies},
    ]

    operations = [
        migrations.RunPython(run_sql_scripts),
    ]
'''

        # Create the new migration file path
        with open(migration_file_path, 'w') as f:
            f.write(migration_file_content)

        self.stdout.write(self.style.SUCCESS(f"Migration file created: {migration_file_path}"))

        # Inform the user about the created migration file and its location
        self.stdout.write(self.style.SUCCESS(f"Migration file created successfully at: {migration_file_path}"))
