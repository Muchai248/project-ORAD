# Generated by Django 5.0.1 on 2024-02-04 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
    ]
