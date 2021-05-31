from django.contrib import admin

# Register your models here.
from wallet.models import Address,Pay2mateUser,WalletTransaction,UserWalletTransaction,DataSetsAchMerchant

admin.site.register(Pay2mateUser)
admin.site.register(Address)
admin.site.register(WalletTransaction)
admin.site.register(UserWalletTransaction)
admin.site.register(DataSetsAchMerchant)