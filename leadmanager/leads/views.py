from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import HospitalLead
from .models import PaymentFollowUp
from django.http import JsonResponse
from .models import Category
from .models import Product, Category
from .models import Product

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
        product.name = request.POST['product_name']
        product.selling_price = request.POST['selling_price']
        product.tax_percent = request.POST['tax_percent']
        product.purchase_price = request.POST['purchase_price']
        product.unit = request.POST['product_unit']
        product.hsn_sac = request.POST.get('hsn_sac')
        product.description = request.POST.get('description')
        product.category_id = request.POST.get('category_id')

        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']
        product.save()
        return redirect('product_detail', product_id=product.id)
    
    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')