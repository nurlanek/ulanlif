from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Order, OrderItem)
# Register your models here.

class OrderAdmin(ImportExportModelAdmin):
    list_display = ("orderno", "description", "client", "created_at", "updated_at",)
    search_fields = ("orderno",)

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(ImportExportModelAdmin):
    list_display = ("order", "product", "quantity", "price",)
    search_fields = ("order",)

admin.site.register(OrderItem, OrderItemAdmin)