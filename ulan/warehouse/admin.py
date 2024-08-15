from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Product)
# Register your models here.

class ProductAdmin(ImportExportModelAdmin):
    list_display = ("name", "description", "quantity", "price", "created_at", "updated_at",)
    search_fields = ("name",)

admin.site.register(Product, ProductAdmin)
