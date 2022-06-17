from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    discount = models.IntegerField(default=0, null=True)
    price_discount = models.DecimalField(decimal_places=2,max_digits=10, default=0, null=True)
    description = RichTextUploadingField()
    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    admin_photo.short_description = 'Product Image'
    admin_photo.allow_tags = True
    
    def save(self, *args, **kwargs):
        count = (self.price / 100) * int(self.discount)
        self.price_discount = self.price - count

        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.title)
    
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        

class Contact(models.Model):
    username = models.CharField(max_length=50)
    gmail = models.EmailField(max_length=50)
    message = models.TextField()
    
    def __str__(self):
        return self.username + " " + self.gmail + " " + self.message