# Generated by Django 5.0.1 on 2024-02-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0022_remove_customuser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
