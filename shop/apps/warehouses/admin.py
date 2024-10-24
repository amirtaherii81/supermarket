from django.contrib import admin
from .models import WarehouseType, Warehouse
# Register your models here.

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ['id','warehouse_type_title',]
    
#----------------------------------------------------------------   
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['product','warehouse_type', 'qty', 'price', 'user_registered', 'register_date']
