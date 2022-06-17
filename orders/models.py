from django.db import models
from product.models import Product
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save


class Order(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True, default=None)
    email = models.EmailField(blank=True,null=True,default=None)
    phone = models.CharField(max_length=12, blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True, default=None)
    total_price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name) + " -- " + str(self.phone) + " -- " + str(self.address)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    nmb = models.IntegerField(default=1)
    price_per_item = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.product.category) + ": " + self.product.title
    
    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.product.image.url))
    admin_photo.short_description = 'Product Image'
    admin_photo.allow_tags = True
    
    
    class Meta:
        verbose_name = 'Product_in_Order'
        verbose_name_plural = 'Product_in_Orders'
    
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = self.nmb * self.price_per_item
        
        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
        print(order_total_price)

    instance.order.total_price = order_total_price

    
    instance.order.save(force_update=True)
    
post_save.connect(product_in_order_post_save, sender=ProductInOrder)
    
    