from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Malzeme_category, Malzeme_birim, Malzeme)

class Malzeme_categoryAdmin(ImportExportModelAdmin):
    list_display = ("name",)

class Malzeme_birimAdmin(ImportExportModelAdmin):
    list_display = ("name",)
class MalzemeAdmin(ImportExportModelAdmin):
    list_display = ("isim", "aciklama", "miktar", "malzeme_category", "malzeme_birim" )

admin.site.register(Malzeme_category, Malzeme_categoryAdmin)
admin.site.register(Malzeme_birim, Malzeme_birimAdmin)
admin.site.register(Malzeme, MalzemeAdmin)