# Generated by Django 4.0.6 on 2022-09-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizlet_API', '0006_alter_course_description_alter_folder_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default=False, max_length=200),
        ),
    ]