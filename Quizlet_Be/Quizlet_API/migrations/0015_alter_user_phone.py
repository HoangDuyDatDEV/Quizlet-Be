# Generated by Django 4.0.6 on 2022-09-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizlet_API', '0014_alter_userinclass_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(blank=True),
        ),
    ]
