# Generated by Django 5.1.3 on 2024-11-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='description',
        ),
        migrations.AddField(
            model_name='subrole',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]