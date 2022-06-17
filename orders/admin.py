from django.contrib import admin
from .models import Order, ProductInOrder


class ProductInOrderInline(admin.TabularInline):
    list_display = ('id', 'product', 'admin_photo')
    readonly_fields = ('admin_photo',)
    model = ProductInOrder
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone',  'total_price', 'is_active', 'created_date', 'updated_date')
    inlines = [ProductInOrderInline]
    
    class Meta:
        model = Order
    
admin.site.register(Order, OrderAdmin)

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order','product', 'admin_photo', 'nmb', 'price_per_item', 'total_price', 'is_active', 'created_date', 'updated_date')
    readonly_fields = ('admin_photo',)
    class Meta:
        model = ProductInOrder
            
admin.site.register(ProductInOrder, ProductInOrderAdmin)
