from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'admin_photo', 'price', 'is_published', 'is_active', 'created_date', 'updated_date')
    readonly_fields = ('admin_photo',)
    
    class Meta:
        model = Product
        
admin.site.register(Product, ProductAdmin) 