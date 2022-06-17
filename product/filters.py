from dataclasses import fields
from pyexpat import model
import django_filters
from matplotlib.pyplot import cla
from numpy import product

from .models import Category

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['category',]