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

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'employees': employees
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

    return render(request, 'add_employee.html', {
        'employee': employee,
        'customer': employee.customer,
        'is_edit': True
    })

def delete_employee(request, employee_id):
    """Delete employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    customer_id = employee.customer.id

    employee_name = employee.name
    employee.delete()

    messages.success(request, f'Employee {employee_name} deleted successfully!')
    return redirect('customer_detail', customer_id=customer_id)