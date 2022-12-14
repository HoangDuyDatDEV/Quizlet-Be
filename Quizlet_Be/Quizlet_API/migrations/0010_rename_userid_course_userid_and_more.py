# Generated by Django 4.0.6 on 2022-09-15 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quizlet_API', '0009_alter_userinclass_numberofusers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='UserID',
            new_name='userID',
        ),
        migrations.RenameField(
            model_name='flashcard',
            old_name='CourseID',
            new_name='courseID',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='UserID',
            new_name='userID',
        ),
        migrations.RenameField(
            model_name='folderinclass',
            old_name='ClassID',
            new_name='classID',
        ),
        migrations.RenameField(
            model_name='folderinclass',
            old_name='FolderID',
            new_name='folderID',
        ),
        migrations.RenameField(
            model_name='userinclass',
            old_name='ClassID',
            new_name='classID',
        ),
        migrations.RenameField(
            model_name='userinclass',
            old_name='UserID',
            new_name='userID',
        ),
    ]
