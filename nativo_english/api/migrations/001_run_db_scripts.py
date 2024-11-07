from django.db import migrations
import os

def run_sql_scripts(apps, schema_editor):
    # Define the path to your db_scripts directory
    script_directory = os.path.join(os.path.dirname(__file__), '../../db_scripts')

    # Loop through your SQL scripts and execute them
    for script_name in os.listdir(script_directory):
        if script_name.endswith('.sql'):
            script_path = os.path.join(script_directory, script_name)
            
            with open(script_path, 'r') as script_file:
                sql_query = script_file.read()

            # Run the SQL command
            schema_editor.execute(sql_query)

class Migration(migrations.Migration):

    dependencies = [
        # Define dependencies, like previous migration files
    ]

    operations = [
        migrations.RunPython(run_sql_scripts),
    ]