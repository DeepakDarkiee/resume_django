# Generated by Django 3.2.4 on 2021-08-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_team_member_user_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_teamleader',
            field=models.BooleanField(default=False),
        ),
    ]
