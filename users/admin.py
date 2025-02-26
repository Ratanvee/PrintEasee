from django.contrib import admin
from .models import CustomUser, Document

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'unique_url')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')



from django.contrib import admin
from .models import PrintOrder

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ('file', 'status', 'created_at')
    list_filter = ('status',)
