# Generated by Django 4.1.5 on 2023-01-16 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_user_is_qualified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
