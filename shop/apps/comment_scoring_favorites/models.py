from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser 
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments_product', verbose_name='کالا')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments_user1', verbose_name='کاربر نظر دهنده') 
    approving_user = models.ForeignKey(CustomUser,blank=True, null=True , on_delete=models.CASCADE, related_name='comments_user2', verbose_name='کاربر تایید کننده نظر') 
    comment_text = models.TextField(verbose_name='متن نظر')
    register_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت نظر')
    comment_parent = models.ForeignKey('Comment',on_delete=models.CASCADE, null=True, blank=True ,related_name='comments_child', verbose_name='والد نظر')

    def __str__(self):
        return f"{self.product} {self.commenting_user}"
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
     
#----------------------------------------------------------------
class Scoring(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='scoring_product', verbose_name='کالا')
    scoring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scoring_user', verbose_name='امتیاز دهی')
    register_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ درج')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])   


    def __str__(self):
        return f"{self.product} - {self.scoring_user}"
    
    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'

#----------------------------------------------------------------
class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite_product', verbose_name='کالا')
    favorite_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_user', verbose_name='کاربر علاقه مند')
    register_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ افزودن')
    
    
    def __str__(self):
        return f"{self.product} - {self.favorite_user}"

    class Meta:
        verbose_name = 'علاقه'
        verbose_name_plural = 'علایق'
    
    
