from django.contrib import admin
from .models import (
    Brand, ProductGroup,Product, ProductFeature, Feature, ProductGallery, FeatureValue
    )
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field

# Register your models here.

#==================BrandModelsAmin=============================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title', 'slug')
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)

#===================ProductGroupsAction==================
def de_active_product_group(modeladmin, request, queryset):  # (متدی که باید میشود سه تا از کوئری ست ها آپدیت شوند(اکشن نویسی   
    res = queryset.update(is_active=False)
    message = f'تعداد {res} گروه کالا غیر فعال شد'
    modeladmin.message_user(request, message)

#-----------------------------------------------
def active_product_group(modeladmin, request, queryset):  # (متدی که باید میشود سه تا از کوئری ست ها آپدیت شوند(اکشن نویسی   
    res = queryset.update(is_active=True)
    message = f'تعداد {res} گروه کالا فعال شد'
    modeladmin.message_user(request, message)
    
#-----------------------------------------------
def export_json(modelsadmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset, stream=response)
    return response

#-----------------------------------------------
def delete_selected_custom(modeladmin, request, queryset):
    # چک کردن مجوز های لازم برای حذف
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    res = queryset.delete()
    message = f'تعداد گروه {res} کالا حذف شد'
    modeladmin.message_user(request,message)
#-----------------------------------------------
class GroupFilter(SimpleListFilter):    # برای کاستم سازی فیلتر ها 
    title = 'گروه محصولات'
    parameter_name = 'group'  #  مشخص کردن پارامتر خط آدرس(name value url)

    def lookups(self,request, model_admin): # می توان فیلترمان را عوض کنیم با کمک این تابع و پیاده سازی این تابع اجباری است
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]

    def queryset(self, request, queryset):  # به پارامتر اول item.id توجه دارد  value
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
            return queryset
    
#-----------------------------------------------
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 3

#===================ProductGroupsModel===================
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title', 'is_active', 'group_parent', 'slug', 'register_date', 'update_date', 'count_sub_group', 'count_product_of_group')
    list_filter = (GroupFilter, 'is_active',)
    search_fields = ('group_title',)
    ordering = ('group_parent', 'group_title',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [de_active_product_group, active_product_group, export_json, delete_selected_custom]
    list_editable = ['is_active']   # برای راحتر کردن ادیت فیلد هایی از جنس بولین

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group = Count('groups'))
        qs = qs.annotate(product_of_group = Count('products_of_groups'))
        return qs
    
    @short_description('تعداد زیر گروه ها')
    @order_field('sub_group')
    def count_sub_group(self, obj):
        return obj.sub_group
    
    @short_description('تعداد کالاهای گروه')
    @order_field('product_of_group')
    def count_product_of_group(self, obj):
        return obj.product_of_group
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    de_active_product_group.short_description = 'غیر فعال کردن گروه های انتخاب شده'
    active_product_group.short_description = 'فعال کردن گروه های انتخاب شده'
    export_json.short_description = 'خروجی json از گروه های انتخاب شده'
    delete_selected_custom.short_description = 'حذف موارد انتخاب شده'
    
#=====================ProductAction============================
def de_active_product(modeladmin, request,queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

#-----------------------------
def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)

#-----------------------------
class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 3
    
    class Media:
        css = {
            'all': ('css/admin_style.css',)
        }
        
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )
#-----------------------------
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3
#=====================ProductModelAdmin============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'display_product_group', 'price', 'brand', 'is_active', 'update_date', 'slug',)
    list_filter = (('brand__brand_title', DropdownFilter), ('product_group__group_title', DropdownFilter))
    search_fields = ('product_name',)
    ordering = ('update_date', 'product_name',)
    actions = [de_active_product, active_product]
    inlines = [ProductFeatureInlineAdmin, ProductGalleryInline]
    list_editable = ['is_active']

    #-----------------------------
    def display_product_group(self, obj):
       return ', '.join([group.group_title for group in obj.product_group.all()])
   
   
    #-----------------------------
    def formfield_for_manytomany(self, db_field, request, **kwargs):
       if db_field.name ==  'product_group':
           kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
       return super().formfield_for_manytomany(db_field, request, **kwargs)

    #-----------------------------
    de_active_product.short_description = 'غیر فعال کردن کالاهای انتخاب شده'
    active_product.short_description = 'فعال کردن کالاهای انتخاب شده'
    display_product_group.short_description = 'گروه های کالا'

    #-----------------------------
    fieldsets = (
        ('اطلاعات محصول',{'fields':(
           'product_name',
           'price',
           'image_name',
           ('product_group', 'brand',),   # برای قرار دادن فیلدها در یک سطر
           'is_active',
           'summary_description',
           'description',
           'slug', 
        )}),
        ('تاریخ و زمان',{'fields':(
            'published_date',
        )}),
    )
    
    class Media:
        css = {
            'all': ('css/admin_style.css',)
        }
        
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )

#==========================FeatureModelAdmin======================================
class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3
    
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'display_groups', 'display_feature_value', )
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline, ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def display_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    def display_feature_value(self, obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_values.all()])

    display_groups.short_descriptions = 'گروه های دارای این ویژگی'
    display_feature_value.short_descriptions = 'مقادیر ممکن برای این ویژگی'

#========================================================================

    


