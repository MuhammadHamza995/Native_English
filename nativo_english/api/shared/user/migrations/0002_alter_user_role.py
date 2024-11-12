# Generated by Django 5.1.2 on 2024-11-14 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')], max_length=100, null=True),
        ),
    ]
