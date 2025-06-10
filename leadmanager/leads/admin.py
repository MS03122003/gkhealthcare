from django.contrib import admin
from .models import HospitalLead
from .models import Category
from .models import Product
from .models import Parts

admin.site.register(HospitalLead)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Parts)