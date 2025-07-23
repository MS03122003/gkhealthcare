from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-lead/', views.new_lead, name='new_lead'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('payment-followup/', views.payment_followup_form, name='payment_followup_form'),
    path('save-payment-followup/', views.save_payment_followup, name='save_payment_followup'),
     path('add-category/', views.add_category, name='add_category'),
    #  path('update-category/<str:category_id>/', views.update_category, name='update_category'),
    path('delete-category/<str:category_id>/', views.delete_category, name='delete_category'),
     path('categories/', views.category_list, name='category_list'),
    
    # path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<str:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<str:category_id>/', views.delete_category, name='delete_category'),
    path('save-category/', views.save_category, name='save_category'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('products/<str:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<str:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/add/', views.add_product, name='save_product'),  
    path('parts/', views.parts_list, name='parts_list'),
    path('parts/add/', views.add_parts, name='add_parts'),
    path('parts/<str:parts_id>/', views.parts_detail, name='parts_detail'),
    path('parts/<str:parts_id>/edit/', views.edit_parts, name='edit_parts'),
    path('parts/<str:parts_id>/delete/', views.delete_parts, name='delete_parts'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/save/', views.save_customer, name='save_customer'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('add-employee/<int:customer_id>/', views.add_employee, name='add_employee'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
   path('customers/<int:customer_id>/add-product/', views.add_customer_product, name='add_customer_product'),
   path('customers/product/edit/<int:product_id>/', views.edit_customer_product, name='edit_customer_product'),
   path('customers/product/delete/<int:product_id>/', views.delete_customer_product, name='delete_customer_product'),

    path('add_vendor/', views.add_vendor, name='add_vendor'),
    path('save_vendor/', views.save_vendor, name='save_vendor'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('vendor_detail/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('vendors/delete/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),

    # Vendor Employee URLs
    path('add_vendor_employee/<int:vendor_id>/', views.add_vendor_employee, name='add_vendor_employee'),
    path('edit_vendor_employee/<int:employee_id>/', views.edit_vendor_employee, name='edit_vendor_employee'),
    path('delete_vendor_employee/<int:employee_id>/', views.delete_vendor_employee, name='delete_vendor_employee'),
    
  
# With these updated lines:
    path('vendors/<int:vendor_id>/add-product/', views.add_vendor_product, name='add_vendor_product'),
    path('vendors/product/edit/<int:product_id>/', views.edit_vendor_product, name='edit_vendor_product'),
    path('vendors/product/delete/<int:product_id>/', views.delete_vendor_product, name='delete_vendor_product'),
        

]