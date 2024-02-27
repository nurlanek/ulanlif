from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Kroy_detail, Kroy, Masterdata, Colors, City, Operations, Product_type
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import json
from django.core.management import call_command
from django.http import HttpResponse
import xlrd
import json

class MasterdataAdmin(ImportExportModelAdmin):
    list_display = ("kroy_no", "edinitsa", "created", "user", "confirmation","status",)
    list_editable = ("confirmation",)

class KroyAdmin(ImportExportModelAdmin):
    list_display = ("id", "kroy_no", "name", "ras_tkani", "ras_dublerin", "edinitsa", "description", "created", "is_active",)
    search_fields = ("kroy_no",)
    list_editable = ("is_active",)

class ColorsAdmin(ImportExportModelAdmin):
    list_display = ("name",)

class Product_typeAdmin(ImportExportModelAdmin):
    list_display = ("name",)

class CityAdmin(ImportExportModelAdmin):
    list_display = ("name",)

class Kroy_detailAdmin(ImportExportModelAdmin):
    list_display = ("kroy", "pachka", "razmer", "rost", "stuk", "user", )
    search_fields = ("kroy",)

class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    actions = ['export_selected', 'import_data']

class OperationsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("kroy","product_type", "name", "price", )
    search_fields = ("name",)




# Отменить предыдущую регистрацию модели UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Masterdata, MasterdataAdmin)
admin.site.register(Kroy, KroyAdmin)
admin.site.register(Kroy_detail, Kroy_detailAdmin)
admin.site.register(Colors, ColorsAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Operations, OperationsAdmin)
admin.site.register(Product_type, Product_typeAdmin)
