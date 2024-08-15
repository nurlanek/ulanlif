from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Client)
# Register your models here.

class ClientAdmin(ImportExportModelAdmin):
    list_display = ("name", "email", "phone", "address", "created_at", "updated_at", )
    search_fields = ("name",)

admin.site.register(Client, ClientAdmin)