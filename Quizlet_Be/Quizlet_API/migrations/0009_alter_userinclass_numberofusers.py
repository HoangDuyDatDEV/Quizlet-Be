# Generated by Django 4.0.6 on 2022-09-13 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizlet_API', '0008_class_members_alter_userinclass_numberofusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinclass',
            name='numberOfUsers',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
