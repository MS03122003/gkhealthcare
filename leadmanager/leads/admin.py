from django.contrib import admin
from .models import HospitalLead
from .models import Category
from .models import Product

admin.site.register(HospitalLead)
admin.site.register(Category)
admin.site.register(Product)