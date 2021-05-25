# Generated by Django 3.1.7 on 2021-05-24 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0009_auto_20210523_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyorder',
            name='account_number',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='moneyorder',
            name='check_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='moneyorder',
            name='number',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='moneyorder',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='money_order_qr/'),
        ),
        migrations.AddField(
            model_name='moneyorder',
            name='routing_number',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
