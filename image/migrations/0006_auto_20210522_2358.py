# Generated by Django 3.1.7 on 2021-05-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0005_auto_20210522_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achchecksimage',
            name='image_type',
            field=models.CharField(choices=[('money_order', 'money_order'), ('ach_check', 'Ach Check'), ('cashier_mask', 'Cashier Mask')], max_length=15),
        ),
    ]
