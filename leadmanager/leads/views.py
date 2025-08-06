from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import HospitalLead
from .models import PaymentFollowUp
from django.http import JsonResponse
from .models import Category
from .models import Product, Category
from .models import Product
from .models import Parts 
from .models import Employee
from .models import CustomerProduct
from .models import Customer
import datetime
import os

from .models import Project, Expense, ExpenseCategory
from .forms import ProjectForm, ExpenseCategoryForm,ExpenseForm
from django.core.paginator import Paginator
from django.db.models import Q, Sum

def payment_followup_form(request):
    return render(request, 'payment_followup_form.html')

def save_payment_followup(request):
    if request.method == 'POST':
        try:
            PaymentFollowUp.objects.create(
                client_name=request.POST.get('client_name'),
                amount=request.POST.get('amount'),
                mode_of_payment=request.POST.get('mode_of_payment'),
                payment_status=request.POST.get('payment_status'),
                follow_up_date=request.POST.get('follow_up_date'),
                next_follow_date=request.POST.get('next_follow_date'),
                last_payment_date=request.POST.get('last_payment_date'),
                due_days=request.POST.get('due_days'),
                present_date=request.POST.get('present_date')
            )
            messages.success(request, 'Payment follow-up details saved successfully!')
            return redirect('payment_followup_form')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')
            return redirect('payment_followup_form')
    return redirect('payment_followup_form')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
@login_required
def payment(request):
    return render(request, 'payment.html')


@login_required
def new_lead1(request):
    if request.method == 'POST':
        try:
            data = request.POST

            # List of checkbox options
            decision_maker_choices = [
                'Dialysis Technician', 'Nephrologist', 
                'Purchase Department', 'Account Department',
                'Biomedical Department'
            ]

            telecalling_response_choices = [
                'Did not receive', 'Call me later', 'Not interested',
                'Interested in product', 'No more in business', 'Other'
            ]

            # Extract selected checkboxes
            decision_maker = [
                choice for choice in decision_maker_choices
                if data.get(f'decision_maker_{choice.lower().replace(" ", "_")}')
            ]

            telecalling_response = [
                choice for choice in telecalling_response_choices
                if data.get(f'telecalling_response_{choice.lower().replace(" ", "_")}')
            ]

            # Create and save the lead
            lead = HospitalLead.objects.create(
                hospital_name=data['hospital_name'],
                hospital_type=data['hospital_type'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                email=data.get('email'),
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                country=data.get('country', 'India'),
                decision_maker=decision_maker,
                telecalling_response=telecalling_response,
                followup_date=data.get('followup_date'),
                followup_time=data.get('followup_time'),
                communication_channel=data.get('communication_channel'),
                promotional_messages=data.get('promotional_messages'),
                remarks=data.get('remarks'),
                created_by=request.user,
            )

            messages.success(request, 'Hospital lead submitted successfully!')
            return redirect('new_lead')

        except Exception as e:
            messages.error(request, f'Error submitting form: {str(e)}')
            return redirect('new_lead')

    return render(request, 'new_lead.html')




def new_lead(request):
    # ✅ Get categories grouped by ID
    category_ids = Category.objects.values_list('id', flat=True).distinct()
    categories = {}
    for id in category_ids:
        categories[id] = Category.objects.filter(id=id)

    # ✅ Get all products
    products = Product.objects.all()

    if request.method == 'POST':
        try:
            data = request.POST

            # ✅ Handle multiple selected products
            products_data = []
            for key, value in data.items():
                if key.startswith('products[') and key.endswith('][id]'):
                    index = key.split('[')[1].split(']')[0]
                    product_id = value
                    product_name = data.get(f'products[{index}][name]', '')
                    if product_id and product_name:
                        products_data.append({
                            'id': product_id,
                            'name': product_name
                        })
            print("Received products:", products_data)  # Optional: remove in production

            # ✅ Handle checkboxes
            decision_maker = data.getlist('decision_maker')
            telecalling_response = data.getlist('telecalling_response')

            # ✅ Create lead
            lead = HospitalLead.objects.create(
                hospital_name=data.get('hospital_name', '').strip(),
                hospital_type=data.get('hospital_type', '').strip(),
                first_name=data.get('first_name', '').strip(),
                last_name=data.get('last_name', '').strip(),
                phone=data.get('phone', '').strip(),
                email=data.get('email', '').strip(),
                address=data.get('address', '').strip(),
                city=data.get('city', '').strip(),
                state=data.get('state', '').strip(),
                country=data.get('country', 'India').strip(),
                decision_maker=decision_maker,
                telecalling_response=telecalling_response,
                followup_date=data.get('followup_date'),
                followup_time=data.get('followup_time'),
                communication_channel=data.get('communication_channel'),
                promotional_messages=data.get('promotional_messages'),
                remarks=data.get('remarks'),
                created_by=request.user,
            )

            # ✅ Success message
            messages.success(request, 'Hospital lead submitted successfully!')
            return redirect('new_lead')

        except Exception as e:
            messages.error(request, f'Error submitting form: {str(e)}')
            return redirect('new_lead')

    # ✅ Always pass categories and products for rendering
    return render(request, 'new_lead.html', {
        'categories': categories,
        'products': products
    })



def add_category(request):
    return render(request, 'add_categories.html')

def save_category(request):
    if request.method == 'POST':
        try:
            Category.objects.create(
                id=request.POST.get('category_id'),
                name=request.POST.get('category_name'),
                description=request.POST.get('description'),
                image=request.FILES.get('category_image')
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'update_categories.html', {'category': category})

def save_updated_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=request.POST.get('category_id_original'))
            category.id = request.POST.get('category_id')
            category.name = request.POST.get('category_name')
            category.description = request.POST.get('description')
            
            if 'category_image' in request.FILES:
                category.image = request.FILES.get('category_image')
            
            category.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        Category.objects.create(
            id=request.POST['category_id'],
            name=request.POST['category_name']
        )
        return redirect('category_list')
    return render(request, 'add_category.html')

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        try:
            category.id = request.POST['category_id']
            category.name = request.POST['category_name']
            # Save other fields as needed
            category.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

def product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        # Handle multiple products
        products_data = []
        for key, value in request.POST.items():
            if key.startswith('products[') and key.endswith('][id]'):
                index = key.split('[')[1].split(']')[0]
                product_id = value
                product_name = request.POST.get(f'products[{index}][name]', '')
                if product_id and product_name:
                    products_data.append({
                        'id': product_id,
                        'name': product_name
                    })
        
        # Process your lead with products_data here
        print("Received products:", products_data)
        
    return render(request, 'new_lead.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        Product.objects.create(
            id=request.POST.get('product_id'),
            name=request.POST.get('product_name'),
            selling_price=request.POST.get('selling_price'),
            tax_percent=request.POST.get('tax_percent'),
            purchase_price=request.POST.get('purchase_price'),
            unit=request.POST.get('product_unit'),
            hsn_sac=request.POST.get('hsn_sac'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category_id'),
            product_image=request.FILES.get('product_image')
        )
        return redirect('product_list')
    
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            # Helper function to handle decimal fields
            def get_decimal_value(field_name, default_value):
                value = request.POST.get(field_name, '').strip()
                if value == '' or value is None:
                    return default_value
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default_value
            
            # Update product fields with proper validation
            product.name = request.POST.get('name', '').strip() or product.name
            
            # Handle decimal fields safely
            product.selling_price = get_decimal_value('selling_price_with_tax', product.selling_price)
            product.tax_percent = get_decimal_value('tax_percentage', product.tax_percent)
            product.purchase_price = get_decimal_value('purchase_price_with_tax', product.purchase_price)
            
            # Handle text fields
            product.unit = request.POST.get('unit', product.unit)
            product.hsn_sac = request.POST.get('hsn_sac', '').strip() or product.hsn_sac
            product.description = request.POST.get('description', '').strip() or product.description
            
            # Handle category
            category_id = request.POST.get('category')
            if category_id:
                product.category_id = category_id

            # Handle image upload (check both possible field names)
            if 'image' in request.FILES:
                if hasattr(product, 'image'):
                    product.image = request.FILES['image']
                elif hasattr(product, 'product_image'):
                    product.product_image = request.FILES['image']
            
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
            
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
            return redirect('edit_product', product_id=product_id)
    
    # Get all categories for the dropdown
    categories = Category.objects.all()
    return render(request, 'edit_product.html', {
        'product': product, 
        'categories': categories
    })

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, f'Product "{product.name}" deleted successfully!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error deleting product: {str(e)}')
            return redirect('product_list')
    
    # For GET request, show confirmation page
    return render(request, 'delete_product_confirm.html', {'product': product})
# Updated Parts-related view functions to add to your views.py

def parts_list(request):
    parts_list = Parts.objects.all()
    return render(request, 'parts_list.html', {'parts_list': parts_list})

def parts_detail(request, parts_id):
    parts = get_object_or_404(Parts, id=parts_id)
    return render(request, 'parts_detail.html', {'parts': parts})

def add_parts(request):
    if request.method == 'POST':
        try:
            # Get category and product objects if provided
            category = None
            product = None
            
            category_id = request.POST.get('category')
            if category_id:
                category = get_object_or_404(Category, id=category_id)
            
            product_id = request.POST.get('product')
            if product_id:
                product = get_object_or_404(Product, id=product_id)
            
            # Create the parts object
            Parts.objects.create(
                id=request.POST.get('parts_id'),
                name=request.POST.get('parts_name'),
                category=category,
                product=product,
                description=request.POST.get('description', '').strip() or None,
                parts_image=request.FILES.get('parts_image')
            )
            messages.success(request, 'Parts added successfully!')
            return redirect('parts_list')
        except Exception as e:
            messages.error(request, f'Error adding parts: {str(e)}')
    
    # Get categories and products for the form
    categories = Category.objects.all()
    products = Product.objects.all()
    
    return render(request, 'add_parts.html', {
        'categories': categories,
        'products': products
    })

def edit_parts(request, parts_id):
    parts = get_object_or_404(Parts, id=parts_id)
    
    if request.method == 'POST':
        try:
            # Update parts fields
            parts.name = request.POST.get('name', '').strip() or parts.name
            parts.description = request.POST.get('description', '').strip() or None
            
            # Handle category selection
            category_id = request.POST.get('category')
            if category_id:
                parts.category = get_object_or_404(Category, id=category_id)
            else:
                parts.category = None
            
            # Handle product selection
            product_id = request.POST.get('product')
            if product_id:
                parts.product = get_object_or_404(Product, id=product_id)
            else:
                parts.product = None
            
            # Handle image upload (check both possible field names)
            if 'image' in request.FILES:
                if hasattr(parts, 'image'):
                    parts.image = request.FILES['image']
                elif hasattr(parts, 'parts_image'):
                    parts.parts_image = request.FILES['image']
            
            parts.save()
            messages.success(request, 'Parts updated successfully!')
            return redirect('parts_list')
            
        except Exception as e:
            messages.error(request, f'Error updating parts: {str(e)}')
            return redirect('edit_parts', parts_id=parts_id)
    
    # Get categories and products for the form
    categories = Category.objects.all()
    products = Product.objects.all()
    
    return render(request, 'edit_parts.html', {
        'parts': parts,
        'categories': categories,
        'products': products
    })

def delete_parts(request, parts_id):
    parts = get_object_or_404(Parts, id=parts_id)
    
    if request.method == 'POST':
        try:
            parts.delete()
            messages.success(request, f'Parts "{parts.name}" deleted successfully!')
            return redirect('parts_list')
        except Exception as e:
            messages.error(request, f'Error deleting parts: {str(e)}')
            return redirect('parts_list')
    
    # For GET request, show parts list
    return redirect('parts_list')

@login_required
def add_customer(request):
    """Display the add customer form"""
    return render(request, 'add_customer.html')


@login_required
def save_customer(request):
    """Save customer data to database"""
    if request.method == 'POST':
        try:
            customer = Customer.objects.create(
                customer_id=request.POST.get('customer_id', '').strip() or None,
                company_name=request.POST.get('company_name', '').strip() or None,
                customer_name=request.POST.get('customer_name', '').strip(),
                phone_number=request.POST.get('phone_number', '').strip(),
                phone_number_2=request.POST.get('phone_number_2', '').strip() or None,
                email=request.POST.get('email', '').strip() or None,
                gstin=request.POST.get('gstin', '').strip() or None,
                address_line_1=request.POST.get('address_line_1', '').strip() or None,
                address_line_2=request.POST.get('address_line_2', '').strip() or None,
                city=request.POST.get('city', '').strip() or None,
                state=request.POST.get('state', '').strip() or None,
                pincode=request.POST.get('pincode', '').strip() or None,
                company_website=request.POST.get('company_website', '').strip() or None,
                created_by=request.user,
            )
            messages.success(request, f'Customer "{customer.customer_name}" added successfully!')
            return redirect('customer_list')  # or use 'total_customer' if separate view

        except Exception as e:
            messages.error(request, f'Error adding customer: {str(e)}')
            return redirect('add_customer')

    return redirect('add_customer')


@login_required
def customer_list(request):
    """Display list of all customers with search and filter functionality"""
    customers = Customer.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(customer_id__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    # Filters
    state_filter = request.GET.get('state', '')
    if state_filter:
        customers = customers.filter(state__icontains=state_filter)

    city_filter = request.GET.get('city', '')
    if city_filter:
        customers = customers.filter(city__icontains=city_filter)

    states = Customer.objects.exclude(state__isnull=True).exclude(state='').values_list('state', flat=True).distinct().order_by('state')
    cities = Customer.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct().order_by('city')

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer_list.html', {
        'customers': page_obj,
        'search_query': search_query,
        'state_filter': state_filter,
        'city_filter': city_filter,
        'states': states,
        'cities': cities,
        'total_customers': Customer.objects.count(),
    })


@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    employees = customer.employees.all()  # Uses related_name='employees' from Employee model
    customer_products = customer.products.all()  # Assuming you have a CustomerProduct model

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'employees': employees,
        'customer_products': customer_products
    })


@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            customer.company_name = request.POST.get('company_name', '').strip() or None
            customer.customer_name = request.POST.get('customer_name', '').strip()
            customer.phone_number = request.POST.get('phone_number', '').strip()
            customer.phone_number_2 = request.POST.get('phone_number_2', '').strip() or None
            customer.email = request.POST.get('email', '').strip() or None
            customer.gstin = request.POST.get('gstin', '').strip() or None
            customer.address_line_1 = request.POST.get('address_line_1', '').strip() or None
            customer.address_line_2 = request.POST.get('address_line_2', '').strip() or None
            customer.city = request.POST.get('city', '').strip() or None
            customer.state = request.POST.get('state', '').strip() or None
            customer.pincode = request.POST.get('pincode', '').strip() or None
            customer.company_website = request.POST.get('company_website', '').strip() or None

            customer.save()
            messages.success(request, f'Customer "{customer.customer_name}" updated successfully!')
            return redirect('customer_detail', customer_id=customer.id)

        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
            return redirect('edit_customer', customer_id=customer_id)

    return render(request, 'edit_customer.html', {'customer': customer})


@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            customer_name = customer.customer_name
            customer.delete()
            messages.success(request, f'Customer "{customer_name}" deleted successfully!')
            return redirect('customer_list')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
            return redirect('customer_list')

    return render(request, 'delete_customer.html', {'customer': customer})



def add_employee(request, customer_id):
    """Add new employee linked to a customer"""
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            position = request.POST.get('position')
            name = request.POST.get('employee_name')  # match with form field
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            date_of_birth = request.POST.get('date_of_birth')

            if not all([position, name, phone_number, email, date_of_birth]):
                messages.error(request, 'All fields are required!')
                return render(request, 'add_employee.html', {'customer': customer})

            Employee.objects.create(
                customer=customer,  # Assuming you have a ForeignKey to Customer in Employee model
                position=position,
                name=name,
                phone_number=phone_number,
                email=email,
                date_of_birth=date_of_birth
            )

            messages.success(request, f'Employee {name} added successfully!')
            return redirect('customer_detail', customer_id=customer.id)

        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
            return render(request, 'add_employee.html', {'customer': customer})

    return render(request, 'add_employee.html', {'customer': customer})

def edit_employee(request, employee_id):
    """Edit existing employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    customer_id = employee.customer.id  # Assuming Employee has a ForeignKey to Customer

    if request.method == 'POST':
        try:
            employee.position = request.POST.get('position')
            employee.name = request.POST.get('employee_name')
            employee.phone_number = request.POST.get('phone_number')
            employee.email = request.POST.get('email')
            employee.date_of_birth = request.POST.get('date_of_birth')
            employee.save()

            messages.success(request, f'Employee {employee.name} updated successfully!')
            return redirect('customer_detail', customer_id=customer_id)

        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')

    return render(request, 'edit_employee.html', {
        'employee': employee,
        'customer': employee.customer,
        'is_edit': True
    })


def delete_employee(request, employee_id):
    """Delete employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    customer_id = employee.customer.id

    if request.method == 'POST':
        try:
            employee_name = employee.name
            employee.delete()
            messages.success(request, f'Employee {employee_name} deleted successfully!')
            return redirect('customer_detail', customer_id=customer_id)
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
            return redirect('customer_detail', customer_id=customer_id)

    return render(request, 'delete_employee.html', {'employee': employee})


def add_customer_product(request, customer_id):
   customer = get_object_or_404(Customer, id=customer_id)
   categories = Category.objects.all()  # Assuming you have a Category model
   
   if request.method == 'POST':
       # Create the product
       product = CustomerProduct.objects.create(
           customer=customer,
           product_id=request.POST.get('product_id'),
           product_name=request.POST.get('product_name'),
           manufacturer=request.POST.get('manufacturer') or None,
           serial_number=request.POST.get('serial_number') or None,
           selling_price=request.POST.get('selling_price'),
           purchase_price=request.POST.get('purchase_price') or None,
           installation_date=request.POST.get('installation_date') or None,
           warranty_period_date=request.POST.get('warranty_period_date') or None,
           tax_percent=request.POST.get('tax_percent') or None,
           product_unit=request.POST.get('product_unit'),
           hsn_sac=request.POST.get('hsn_sac'),
           category_id=request.POST.get('category_id') or None,
           description=request.POST.get('description'),
       )
       
       # Handle image upload
       if request.FILES.get('product_image'):
           product.product_image = request.FILES['product_image']
           product.save()
       
       messages.success(request, f'Product "{product.product_name}" added successfully!')
       return redirect('customer_detail', customer_id=customer.id)
   
   context = {
       'customer': customer,
       'categories': categories,
   }
   return render(request, 'add_customer_product.html', context)

def edit_customer_product(request, product_id):
   product = get_object_or_404(CustomerProduct, id=product_id)
   customer = product.customer
   categories = Category.objects.all()
   
   if request.method == 'POST':
       # Update product fields
       product.product_id = request.POST.get('product_id')
       product.product_name = request.POST.get('product_name')
       product.manufacturer = request.POST.get('manufacturer') or None
       product.serial_number = request.POST.get('serial_number') or None
       product.installation_date = request.POST.get('installation_date') or None
       product.warranty_period_date = request.POST.get('warranty_period_date') or None
       product.selling_price = request.POST.get('selling_price')
       product.purchase_price = request.POST.get('purchase_price') or None
       product.tax_percent = request.POST.get('tax_percent') or None
       product.product_unit = request.POST.get('product_unit')
       product.hsn_sac = request.POST.get('hsn_sac')
       product.category_id = request.POST.get('category_id') or None
       product.description = request.POST.get('description')
       
       # Handle image upload
       if request.FILES.get('product_image'):
           product.product_image = request.FILES['product_image']
       
       product.save()
       messages.success(request, f'Product "{product.product_name}" updated successfully!')
       return redirect('customer_detail', customer_id=customer.id)
   
   context = {
       'customer': customer,
       'product': product,
       'categories': categories,
   }
   return render(request, 'edit_customer_product.html', context)

def delete_customer_product(request, product_id):
   product = get_object_or_404(CustomerProduct, id=product_id)
   customer_id = product.customer.id
   product_name = product.product_name
   
   # Delete the product image file if it exists
   if product.product_image:
       if os.path.isfile(product.product_image.path):
           os.remove(product.product_image.path)
   
   product.delete()
   messages.success(request, f'Product "{product_name}" deleted successfully!')
   return redirect('customer_detail', customer_id=customer_id)

# Add these imports to your existing views.py file
from .models import Vendor, VendorEmployee, VendorProduct

# Vendor Views
@login_required
def add_vendor(request):
    """Display the add vendor form"""
    return render(request, 'add_vendor.html')

@login_required
def save_vendor(request):
    """Save vendor data to database"""
    if request.method == 'POST':
        try:
            vendor = Vendor.objects.create(
                vendor_id=request.POST.get('vendor_id', '').strip(),
                company_name=request.POST.get('company_name', '').strip() or None,
                vendor_name=request.POST.get('vendor_name', '').strip(),
                phone_number=request.POST.get('phone_number', '').strip(),
                phone_number_2=request.POST.get('phone_number_2', '').strip() or None,
                email=request.POST.get('email', '').strip() or None,
                gstin=request.POST.get('gstin', '').strip() or None,
                address_line_1=request.POST.get('address_line_1', '').strip() or None,
                address_line_2=request.POST.get('address_line_2', '').strip() or None,
                city=request.POST.get('city', '').strip() or None,
                state=request.POST.get('state', '').strip() or None,
                pincode=request.POST.get('pincode', '').strip() or None,
                company_website=request.POST.get('company_website', '').strip() or None,
                created_by=request.user,
            )
            messages.success(request, f'Vendor "{vendor.vendor_name}" added successfully!')
            return redirect('vendor_list')

        except Exception as e:
            messages.error(request, f'Error adding vendor: {str(e)}')
            return redirect('add_vendor')

    return redirect('add_vendor')

@login_required
def vendor_list(request):
    """Display list of all vendors with search and filter functionality"""
    vendors = Vendor.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        vendors = vendors.filter(
            Q(vendor_id__icontains=search_query) |
            Q(vendor_name__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    # Filters
    state_filter = request.GET.get('state', '')
    if state_filter:
        vendors = vendors.filter(state__icontains=state_filter)

    city_filter = request.GET.get('city', '')
    if city_filter:
        vendors = vendors.filter(city__icontains=city_filter)

    states = Vendor.objects.exclude(state__isnull=True).exclude(state='').values_list('state', flat=True).distinct().order_by('state')
    cities = Vendor.objects.exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct().order_by('city')

    paginator = Paginator(vendors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendor_list.html', {
        'vendors': page_obj,
        'search_query': search_query,
        'state_filter': state_filter,
        'city_filter': city_filter,
        'states': states,
        'cities': cities,
        'total_vendors': Vendor.objects.count(),
    })

@login_required
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    employees = vendor.employees.all()
    vendor_products = vendor.products.all()

    return render(request, 'vendor_detail.html', {
        'vendor': vendor,
        'employees': employees,
        'vendor_products': vendor_products
    })

@login_required
def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        try:
            vendor.company_name = request.POST.get('company_name', '').strip() or None
            vendor.vendor_name = request.POST.get('vendor_name', '').strip()
            vendor.phone_number = request.POST.get('phone_number', '').strip()
            vendor.phone_number_2 = request.POST.get('phone_number_2', '').strip() or None
            vendor.email = request.POST.get('email', '').strip() or None
            vendor.gstin = request.POST.get('gstin', '').strip() or None
            vendor.address_line_1 = request.POST.get('address_line_1', '').strip() or None
            vendor.address_line_2 = request.POST.get('address_line_2', '').strip() or None
            vendor.city = request.POST.get('city', '').strip() or None
            vendor.state = request.POST.get('state', '').strip() or None
            vendor.pincode = request.POST.get('pincode', '').strip() or None
            vendor.company_website = request.POST.get('company_website', '').strip() or None

            vendor.save()
            messages.success(request, f'Vendor "{vendor.vendor_name}" updated successfully!')
            return redirect('vendor_detail', vendor_id=vendor.id)

        except Exception as e:
            messages.error(request, f'Error updating vendor: {str(e)}')
            return redirect('edit_vendor', vendor_id=vendor_id)

    return render(request, 'edit_vendor.html', {'vendor': vendor})

@login_required
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        try:
            vendor_name = vendor.vendor_name
            vendor.delete()
            messages.success(request, f'Vendor "{vendor_name}" deleted successfully!')
            return redirect('vendor_list')
        except Exception as e:
            messages.error(request, f'Error deleting vendor: {str(e)}')
            return redirect('vendor_list')

    return render(request, 'delete_vendor.html', {'vendor': vendor})

# Vendor Employee Views
def add_vendor_employee(request, vendor_id):
    """Add new employee linked to a vendor"""
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        try:
            position = request.POST.get('position')
            name = request.POST.get('employee_name')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            date_of_birth = request.POST.get('date_of_birth')

            if not all([position, name, phone_number, email, date_of_birth]):
                messages.error(request, 'All fields are required!')
                return render(request, 'add_vendor_employee.html', {'vendor': vendor})

            VendorEmployee.objects.create(
                vendor=vendor,
                position=position,
                name=name,
                phone_number=phone_number,
                email=email,
                date_of_birth=date_of_birth
            )

            messages.success(request, f'Employee {name} added successfully!')
            return redirect('vendor_detail', vendor_id=vendor.id)

        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
            return render(request, 'add_vendor_employee.html', {'vendor': vendor})

    return render(request, 'add_vendor_employee.html', {'vendor': vendor})

def edit_vendor_employee(request, employee_id):
    """Edit existing vendor employee"""
    employee = get_object_or_404(VendorEmployee, id=employee_id)
    vendor_id = employee.vendor.id

    if request.method == 'POST':
        try:
            employee.position = request.POST.get('position')
            employee.name = request.POST.get('employee_name')
            employee.phone_number = request.POST.get('phone_number')
            employee.email = request.POST.get('email')
            employee.date_of_birth = request.POST.get('date_of_birth')
            employee.save()

            messages.success(request, f'Employee {employee.name} updated successfully!')
            return redirect('vendor_detail', vendor_id=vendor_id)

        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')

    return render(request, 'edit_vendor_employee.html', {
        'employee': employee,
        'vendor': employee.vendor,
        'is_edit': True
    })

def delete_vendor_employee(request, employee_id):
    """Delete vendor employee"""
    employee = get_object_or_404(VendorEmployee, id=employee_id)
    vendor_id = employee.vendor.id

    if request.method == 'POST':
        try:
            employee_name = employee.name
            employee.delete()
            messages.success(request, f'Employee {employee_name} deleted successfully!')
            return redirect('vendor_detail', vendor_id=vendor_id)
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
            return redirect('vendor_detail', vendor_id=vendor_id)

    return render(request, 'delete_vendor_employee.html', {'employee': employee})

# Vendor Product Views

def add_vendor_product(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        try:
            product = VendorProduct.objects.create(
                vendor=vendor,
                product_id=request.POST.get('product_id'),
                product_name=request.POST.get('product_name'),
                selling_price=request.POST.get('selling_price'),
                purchase_price=request.POST.get('purchase_price') or None,
                tax_percent=request.POST.get('tax_percent') or None,
                product_unit=request.POST.get('product_unit'),
                warranty_period_date=request.POST.get('warranty_period_date') or None,
                installation_date=request.POST.get('installation_date') or None,
                hsn_sac=request.POST.get('hsn_sac'),
                category_id=request.POST.get('category_id') or None,
                description=request.POST.get('description'),
                manufacturer=request.POST.get('manufacturer'),
                serial_number=request.POST.get('serial_number'),
            )
            
            if request.FILES.get('product_image'):
                product.product_image = request.FILES['product_image']
                product.save()
            
            messages.success(request, f'Product "{product.product_name}" added successfully!')
            return redirect('vendor_detail', vendor_id=vendor.id)
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'add_vendor_product.html', context)

def edit_vendor_product(request, product_id):
    product = get_object_or_404(VendorProduct, id=product_id)
    vendor = product.vendor
    categories = Category.objects.all()
    
    if request.method == 'POST':
        try:
            product.product_id = request.POST.get('product_id')
            product.product_name = request.POST.get('product_name')
            product.selling_price = request.POST.get('selling_price')
            product.installation_date = request.POST.get('installation_date') or None
            product.warranty_period_date = request.POST.get('warranty_period_date') or None
            product.purchase_price = request.POST.get('purchase_price') or None
            product.tax_percent = request.POST.get('tax_percent') or None
            product.product_unit = request.POST.get('product_unit')
            product.hsn_sac = request.POST.get('hsn_sac')
            product.category_id = request.POST.get('category_id') or None
            product.description = request.POST.get('description')
            product.manufacturer = request.POST.get('manufacturer')
            product.serial_number = request.POST.get('serial_number')
            
            if request.FILES.get('product_image'):
                product.product_image = request.FILES['product_image']
            
            product.save()
            messages.success(request, f'Product "{product.product_name}" updated successfully!')
            return redirect('vendor_detail', vendor_id=vendor.id)
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    context = {
        'vendor': vendor,
        'product': product,
        'categories': categories,
    }
    return render(request, 'edit_vendor_product.html', context)

def delete_vendor_product(request, product_id):
    product = get_object_or_404(VendorProduct, id=product_id)
    vendor_id = product.vendor.id
    product_name = product.product_name
    
    if product.product_image:
        if os.path.isfile(product.product_image.path):
            os.remove(product.product_image.path)
    
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully!')
    return redirect('vendor_detail', vendor_id=vendor_id)

#
@login_required
def generate_report(request):
    """Main reports dashboard view"""
    return render(request, 'generate_report.html')

@login_required
def installation_report(request):
    """Installation reports view"""
    # Add your installation report logic here
    context = {
        'report_type': 'Installation',
        'title': 'Installation Reports'
    }
    return render(request, 'installation_report.html', context)

@login_required
def service_report(request):
    """Service reports view"""
    # Add your service report logic here
    context = {
        'report_type': 'Service',
        'title': 'Service Reports'
    }
    return render(request, 'service_report.html', context)

@login_required
def inspection_report(request):
    """Inspection reports view"""
    # Add your inspection report logic here
    context = {
        'report_type': 'Inspection',
        'title': 'Inspection Reports'
    }
    return render(request, 'inspection_report.html', context)

@login_required
def incident_report(request):
    """Incident reports view"""
    # Add your incident report logic here
    context = {
        'report_type': 'Incident',
        'title': 'Incident Reports'
    }
    return render(request, 'incident_report.html', context)

@login_required
def quotation_report(request):
    """Quotation reports view"""
    # Add your quotation report logic here
    context = {
        'report_type': 'Quotation',
        'title': 'Quotation Reports'
    }
    return render(request, 'quotation_report.html', context)

@login_required
def purchase_order_report(request):
    """Purchase order reports view"""
    # Add your purchase order report logic here
    context = {
        'report_type': 'Purchase Order',
        'title': 'Purchase Order Reports'
    }
    return render(request, 'purchase_order_report.html', context)

@login_required
def delivery_challan_report(request):
    """Delivery challan reports view"""
    # Add your delivery challan report logic here
    context = {
        'report_type': 'Delivery Challan',
        'title': 'Delivery Challan Reports'
    }
    return render(request, 'delivery_challan_report.html', context)


@login_required
def expense_dashboard(request):
    """Main expense dashboard showing all projects"""
    try:
        # Filter projects by current user and active status
        projects = Project.objects.filter(
            created_by=request.user, 
            is_active=True
        ).order_by('-created_at')
        
        # Calculate statistics for each project
        projects_with_stats = []
        for project in projects:
            project.calculated_total = project.total_expense_amount
            project.calculated_paid = project.paid_expenses
            project.calculated_pending = project.pending_expenses
            project.calculated_count = project.expense_count
            projects_with_stats.append(project)
        
        # Overall statistics
        total_projects = projects.count()
        total_expenses = sum(p.calculated_total for p in projects_with_stats)
        total_paid = sum(p.calculated_paid for p in projects_with_stats)
        total_pending = sum(p.calculated_pending for p in projects_with_stats)
        
        context = {
            'projects': projects_with_stats,
            'total_projects': total_projects,
            'total_expenses': total_expenses,
            'total_paid': total_paid,
            'total_pending': total_pending,
        }
        
        return render(request, 'expenses/expense_dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return render(request, 'expenses/expense_dashboard.html', {'projects': []})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('expense_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()

    return render(request, 'expenses/add_project.html', {'form': form})




@login_required
def project_detail(request, project_id):
    """Project detail page showing expenses"""
    try:
        project = get_object_or_404(Project, id=project_id, created_by=request.user)
        expenses = project.expenses.all()
        
        # Filter expenses
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        
        if search_query:
            expenses = expenses.filter(
                Q(description__icontains=search_query) |
                Q(vendor__icontains=search_query) |
                Q(expense_number__icontains=search_query)
            )
        
        if status_filter:
            expenses = expenses.filter(status=status_filter)
        
        # Pagination
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        expenses = paginator.get_page(page_number)
        
        # Calculate totals
        total_expenses = project.expenses.aggregate(
            total=Sum('amount'),
            paid=Sum('amount', filter=Q(status='paid')),
            pending=Sum('amount', filter=Q(status='pending'))
        )
        
        # Handle None values
        for key, value in total_expenses.items():
            if value is None:
                total_expenses[key] = 0
        
        context = {
            'project': project,
            'expenses': expenses,
            'search_query': search_query,
            'status_filter': status_filter,
            'total_expenses': total_expenses,
        }
        
        return render(request, 'expenses/project_details.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading project details: {str(e)}')
        return redirect('expense_dashboard')


@login_required
def add_expense(request, project_id):
    """Add expense to a project"""
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.project = project
                expense.created_by = request.user
                expense.save()
                messages.success(request, f'Expense "{expense.description[:30]}..." added successfully!')
                return redirect('project_detail', project_id=project.id)
            except Exception as e:
                messages.error(request, f'Error adding expense: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm()
    
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'expenses/add_expense.html', context)


@login_required
def edit_expense(request, expense_id):
    """Edit an expense"""
    expense = get_object_or_404(Expense, id=expense_id, created_by=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Expense updated successfully!')
                return redirect('project_detail', project_id=expense.project.id)
            except Exception as e:
                messages.error(request, f'Error updating expense: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'expense': expense,
        'project': expense.project
    }
    return render(request, 'expenses/edit_expense.html', context)


@login_required
def view_expense(request, expense_id):
    """View expense details"""
    expense = get_object_or_404(Expense, id=expense_id, created_by=request.user)
    
    context = {
        'expense': expense,
        'project': expense.project
    }
    return render(request, 'expenses/view_expense.html', context)


@login_required
def delete_expense(request, expense_id):
    """Delete an expense"""
    expense = get_object_or_404(Expense, id=expense_id, created_by=request.user)
    project_id = expense.project.id
    
    if request.method == 'POST':
        try:
            expense.delete()
            messages.success(request, 'Expense deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting expense: {str(e)}')
    
    return redirect('project_detail', project_id=project_id)