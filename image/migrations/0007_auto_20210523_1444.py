# Generated by Django 3.1.7 on 2021-05-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0006_auto_20210522_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashiercheckdetail',
            name='sender_email',
        ),
        migrations.AddField(
            model_name='cashiercheckdetail',
            name='address',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
