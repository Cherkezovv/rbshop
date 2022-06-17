from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=150)
    phone = models.IntegerField()
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    