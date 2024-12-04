
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
        ('db_scripts_automate', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(run_sql_scripts),
    ]
