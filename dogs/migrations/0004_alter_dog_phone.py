# Generated by Django 3.2.5 on 2021-09-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0003_dog_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='phone',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
