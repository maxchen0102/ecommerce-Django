from django.contrib import admin

# Register your models here.
from core import models

admin.site.register(models.ProductModel)
admin.site.register(models.OrdersModel)
admin.site.register(models.DetailModel)
