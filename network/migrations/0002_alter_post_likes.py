# Generated by Django 4.1.1 on 2022-12-14 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=9, null=True),
        ),
    ]
