# Generated by Django 3.1.7 on 2021-05-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_auto_20210520_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneyorder',
            name='receiver_mail',
        ),
        migrations.RemoveField(
            model_name='moneyorder',
            name='receiver_name',
        ),
        migrations.RemoveField(
            model_name='moneyorder',
            name='sender_email',
        ),
        migrations.RemoveField(
            model_name='moneyorder',
            name='sender_name',
        ),
        migrations.AddField(
            model_name='moneyorder',
            name='purchaser',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
