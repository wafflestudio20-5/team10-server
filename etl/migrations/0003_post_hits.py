# Generated by Django 2.2 on 2023-01-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0002_module_modulecontent_weekly'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
