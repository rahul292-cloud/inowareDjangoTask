# Generated by Django 2.2 on 2020-11-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='static/UserProfileImages/'),
        ),
    ]
