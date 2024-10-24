from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
# Create your models here.

class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50, verbose_name='نوع انبار')

    def __str__(self):
        return f"{self.warehouse_type_title}"
    
    class Meta:
        verbose_name = 'نوع انبار'
        verbose_name_plural = 'انواع روش انبار'

#----------------------------------------------------------------
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE, related_name='warehouses', verbose_name='انبار')
    user_registered = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='warehouseuser_registered', verbose_name='ادمین')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouse_products', verbose_name='کالا')
    qty = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت واحد', null=True, blank=True)
    register_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"{self.warehouse_type}"
    
    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'
    
    