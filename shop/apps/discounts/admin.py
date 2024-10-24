from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'start_date', 'end_date', 'discount', 'is_active',)
    ordering = ('is_active',)

#----------------------------------------------------------------
class DiscountBasketDetailsInline(admin.TabularInline):
    model = models.DiscountBasketDetails
    extra = 3

@admin.register(models.DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ('discount_title', 'start_date', 'end_date', 'discount', 'is_active',)
    ordering = ('is_active',)
    inlines = [DiscountBasketDetailsInline,]