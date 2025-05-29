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
    path('products/add/', views.add_product, name='save_product')


    
]