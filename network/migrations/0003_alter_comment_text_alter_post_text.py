# Generated by Django 4.1.1 on 2022-12-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
