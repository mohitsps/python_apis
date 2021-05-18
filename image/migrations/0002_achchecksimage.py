# Generated by Django 3.1.7 on 2021-05-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchChecksImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='check_valid/')),
                ('image_type', models.CharField(choices=[('money_order', 'money_order'), ('ach_check', 'Ach Check')], max_length=15)),
            ],
        ),
    ]