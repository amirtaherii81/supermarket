from django.contrib import admin
from .models import Order, OrderDetails, OrderState
# Register your models here.

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 3

#----------------------------------------------------------------
@admin.register(Order)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_state', 'register_date', 'is_finaly', 'discount']
    inlines = [OrderDetailsInline]

#----------------------------------------------------------------
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_state_title']
    