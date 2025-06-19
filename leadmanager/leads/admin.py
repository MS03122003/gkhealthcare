from django.contrib import admin
from .models import HospitalLead
from .models import Category
from .models import Product
from .models import Parts
from .models import Customer
from .models import Employee

admin.site.register(HospitalLead)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Parts)
admin.site.register(Customer)
admin.site.register(Employee)
