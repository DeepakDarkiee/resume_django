# Generated by Django 3.2.5 on 2021-07-31 07:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
