from django.db import models
from django.contrib.auth.models import User

class HospitalLead(models.Model):
    # Hospital Information
    hospital_name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=50, choices=[
        ('Direct Hospital', 'Direct Hospital'),
        ('Distributed', 'Distributed'),
        ('Other', 'Other'),
    ])
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')

    # Telecalling and Decision Data
    telecalling_response = models.JSONField(default=list)
    decision_maker = models.JSONField(default=list)

    # Follow-up Information
    followup_date = models.DateField(null=True, blank=True)
    followup_time = models.TimeField(null=True, blank=True)

    # Communication Preferences
    communication_channel = models.CharField(
        max_length=20,
        choices=[
            ('SMS', 'SMS'),
            ('Email', 'Email'),
            ('WhatsApp', 'WhatsApp'),
            ('Phone', 'Phone')
        ],
        null=True,
        blank=True
    )
    
    promotional_messages = models.CharField(
        max_length=3,
        choices=[('Yes', 'Yes'), ('No', 'No')],
        null=True,
        blank=True
    )
    
    remarks = models.TextField(null=True, blank=True)

    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital_name} - {self.first_name} {self.last_name}"
    

class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class Product(models.Model):
    PRODUCT_UNITS = [
        ('kg', 'Kilogram'),
        ('ltr', 'Liter'),
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('nos', 'Numbers'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=PRODUCT_UNITS, default='pcs')
    hsn_sac = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class PaymentFollowUp(models.Model):
    PAYMENT_MODES = [
        ('Mail Done', 'Mail Done'),
        ('Online Transfer', 'Online Transfer'),
        ('Cheque', 'Cheque'),
        ('Cash', 'Cash'),
        ('DD', 'Demand Draft'),
    ]
    
    PAYMENT_STATUSES = [
        ('Pending', 'Pending'),
        ('Partial', 'Partial Payment'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]
    
    client_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    mode_of_payment = models.CharField(max_length=50, choices=PAYMENT_MODES)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUSES)
    follow_up_date = models.DateField(null=True, blank=True)
    next_follow_date = models.DateField(null=True, blank=True)
    last_payment_date = models.DateField()
    due_days = models.IntegerField()
    present_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.client_name} - {self.amount}"
    
    class Meta:
        verbose_name = "Payment Follow-up"
        verbose_name_plural = "Payment Follow-ups"

class Parts(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    
    # New optional fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    parts_image = models.ImageField(upload_to='parts_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Parts"
        verbose_name_plural = "Parts"
        ordering = ['-created_at']

