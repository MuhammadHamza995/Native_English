# Generated by Django 5.1.2 on 2024-11-19 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutedSQLScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('executed_at', models.DateTimeField(auto_now_add=True)),
                ('build_number', models.CharField()),
            ],
        ),
    ]
