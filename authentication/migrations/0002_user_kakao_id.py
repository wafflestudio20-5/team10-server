# Generated by Django 2.2 on 2023-02-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kakao_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]