from django import forms
from .models import Lead
from django.utils import timezone
from .models import Project, Expense, ExpenseCategory
from django.utils import timezone

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
            'followup_date': forms.DateInput(attrs={'type': 'date'}),
            'followup_time': forms.TimeInput(attrs={'type': 'time'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
        

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'amount', 'expense_date', 'category', 'vendor', 
            'description', 'notes', 'payment_type', 'is_paid'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'step': '0.01',
                'min': '0'
            }),
            'expense_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vendor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vendor name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter expense description'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
            'payment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default expense_date to today if not set
        if not self.instance.pk:
            self.fields['expense_date'].initial = timezone.now().date()
        # Optional: add empty option for category
        self.fields['category'].empty_label = "Select Category"

from django import forms
from django.utils import timezone
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'started_date']
        widgets = {
            'project_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Project ID (e.g., PRJ-001)'
            }),
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Project Name'
            }),
            'started_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default started_date to today if creating a new Project
        if not self.instance.pk:
            self.fields['started_date'].initial = timezone.now().date()
            
class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter category description (optional)'
            }),
        }