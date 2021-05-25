from django.contrib import admin

# Register your models here.
from image.models import AchChecksImage,TestedCheck,CashierCheckDetail,MoneyOrder

admin.site.register(AchChecksImage)
admin.site.register(TestedCheck)
admin.site.register(CashierCheckDetail)
admin.site.register(MoneyOrder)