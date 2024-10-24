from django.db import models
import utils
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum, Avg
from middlewares.middleware import RequestMiddleware
#from ckeditor.fields import RichTextField
# Create your models here.

class Brand(models.Model):
    brand_title = models.CharField(max_length=100, verbose_name='نام برند')
    file_upload = utils.FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    slug = models.SlugField(max_length = 200, null=True)

    def __str__(self):
        return self.brand_title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        
# --------------------------------------------------------------------------   
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    file_upload = utils.FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات گروه کالا')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیر فعال')
    group_parent = models.ForeignKey('ProductGroup', on_delete=models.CASCADE, verbose_name='والد گروه کالا', blank=True, null=True, related_name='groups')   # نکته
    register_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین بروز رسانی')
    slug = models.SlugField(max_length = 200, null=True)
    
    def __str__(self):
        return self.group_title

    class Meta:
        verbose_name = 'گروه کالا'
        verbose_name_plural = 'گروه کالاها'
        
# --------------------------------------------------------------------------   
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='features_of_groups')
    
    def __str__(self):
        return self.feature_name

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
        
# --------------------------------------------------------------------------   
class Product(models.Model):    # این کلاس می تواند ارتباط چند به چند با ویژگی ها داشته باشد
    product_name = models.CharField(max_length=500, verbose_name='نام کالاها')
    description = RichTextUploadingField(config_name='special',blank=True, null=True, verbose_name='توضیحات کامل')
    summary_description = models.TextField(default="", blank=True, null=True, verbose_name='توضیح مختصر')

    file_upload = utils.FileUpload('images', 'product')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت کالا')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='products_of_groups')
    features = models.ManyToManyField(Feature, through='ProductFeature')
    brand = models.ForeignKey(Brand, verbose_name='برند کالا', on_delete=models.CASCADE, null=True, blank=True, related_name='product_of_brands')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیر فعال')
    register_date = models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ درج')
    published_date = models.DateField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروز رسانی')
    slug = models.SlugField(max_length = 200, null=True)
        
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})
    
    # قیمت ها با تخفیف کالا
    def get_price_by_discount(self):
        list1 = []
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and 
                dbd.discount_basket.start_date <= datetime.now() and
                dbd.discount_basket.end_date >= datetime.now()):
                list1.append(dbd.discount_basket.discount)
        
        discount = 0
        if (len(list1)>0):
           discount = max(list1)
        return int(self.price - (self.price*discount/100))
            
    # تعدادموجودی کالا در انبار
    def get_number_in_warehouse(self):
        sum1 = self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        sum2 = self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))

        input = 0
        if sum1['qty__sum']!=None:
            input = sum1['qty__sum']
        output = 0
        if sum2['qty__sum']!=None:
            output = sum2['qty__sum']
        return (input-output)
    
    # میزان امتیازی که کاربر جاری به این کالا داده
    def get_user_score(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score = user_score[0].score
        return score
    
    # میانگین امتیازی که این کالا کسب کرده
    def get_average_score(self):
        avgScore = self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore == None:
            avgScore=0
        return '%2.1f'%avgScore
    
    # آیا این کالا مورد علاقه کاربر جاری بوده یا خیر
    def get_user_favorite(self):
        request = RequestMiddleware(get_response=None).thread_local.current_request
        flag = self.favorite_product.filter(favorite_user=request.user).exists()
        return flag
    
    # تابعی برای برگرداندن گروه اصلی کالا
    def get_main_product_group(self):
        return self.product_group.all()[0].id
    
    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'
        
# --------------------------------------------------------------------------   
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100, verbose_name='عنوان مقدار')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, blank=True, null=True, verbose_name='ویژگی', related_name='feature_values')
        
    def __str__(self):
        return f"{self.id}  {self.value_title}"
        
    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی ها'
        
        
# --------------------------------------------------------------------------   
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name = 'product_feature')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')
    filter_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, blank=True, null=True, verbose_name='مقدار ویژگی برای فیلتر')
    
    def __str__(self):
        return f"{self.product} - {self.feature} : {self.value}"

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'

# --------------------------------------------------------------------------   
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='gallery_images') 
    file_upload = utils.FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    
    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
        
# --------------------------------------------------------------------------   
# from django.db.models.signals import post_delete
# from django.dispatch import receiver


# def delete_product_image(sender, **kwargs):
#     print('*'*50)
#     print('delete product image ...')
#     print('*'*50)
# post_delete.connect(receiver=delete_product_image, sender=Product)
        
        
        

# @receiver(post_delete, sender=Product)
# def delete_product_image(sender, **kwargs):
#     print('*'*50)
#     print('delete product image ...')
#     print('*'*50)