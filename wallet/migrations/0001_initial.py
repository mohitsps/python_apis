# Generated by Django 3.1.7 on 2021-05-26 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('city', models.CharField(blank=True, max_length=15, null=True)),
                ('state', models.CharField(blank=True, max_length=15, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pay2mateUser',
            fields=[
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contact', models.CharField(blank=True, max_length=15, null=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_code/')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.address')),
                ('user_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_purpose', models.TextField()),
                ('amount', models.FloatField()),
                ('transaction_token', models.CharField(max_length=256)),
                ('transaction_type', models.CharField(choices=[('debit', 'Debit'), ('credit', 'Credit')], max_length=40)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Wallet_Transaction_Created_By', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Transaction_Receiver', to='wallet.pay2mateuser')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Transaction_Sender', to='wallet.pay2mateuser')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Wallet_Transaction_Updated_By', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserWalletTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_Transaction_Created_By', to=settings.AUTH_USER_MODEL)),
                ('pay2mate_user_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.pay2mateuser')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_Transaction_Updated_By', to=settings.AUTH_USER_MODEL)),
                ('wallet_transaction_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.wallettransaction')),
            ],
        ),
    ]
