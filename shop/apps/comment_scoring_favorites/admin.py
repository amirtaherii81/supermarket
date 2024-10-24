from django.contrib import admin
from . import models 

# Register your models here.
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'commenting_user', 'comment_text', 'is_active']
    list_editable = ['is_active']
