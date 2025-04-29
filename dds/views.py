from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import JsonResponse
from .models import Transaction, Status, Type, Category, Subcategory

# Create your views here.

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        
def index(request):
    transactions = Transaction.objects.all()

    if request.GET.get('date_from'):
        transactions = transactions.filter(created_at__gte=request.GET.get('date_from'))
    if request.GET.get('date_to'):
        transactions = transactions.filter(created_at__lte=request.GET.get('date_to'))
    if request.GET.get('status'):
        transactions = transactions.filter(status_id=request.GET.get('status'))
    if request.GET.get('type'):
        transactions = transactions.filter(type_id=request.GET.get('type'))
    if request.GET.get('category'):
        transactions = transactions.filter(category_id=request.GET.get('category'))
    if request.GET.get('subcategory'):
        transactions = transactions.filter(subcategory_id=request.GET.get('subcategory'))

    dataset = {
        'transactions': transactions,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }

    return render(request, 'dds/index.html', dataset)

def transaction_create(request):
    dataset = {}
    if request.method == 'POST':
        dataset['form'] = TransactionForm(request.POST)
        if dataset['form'].is_valid():
            dataset['form'].save()
            return redirect('dds:index')
    else:
        dataset['form'] = TransactionForm()
    return render(request, 'dds/transaction_form.html', dataset)

def transaction_edit(request, pk):
    dataset = {}
    dataset['transaction'] = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        dataset['form'] = TransactionForm(request.POST, instance=dataset['transaction'])
        if dataset['form'].is_valid():
            dataset['form'].save()
            return redirect('dds:index')
    else:
        dataset['form'] = TransactionForm(instance=dataset['transaction'])
    return render(request, 'dds/transaction_form.html', dataset)

def transaction_delete(request, pk):
    dataset = {}
    dataset['transaction'] = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        dataset['transaction'].delete()
        return redirect('dds:index')
    dataset['transactions'] = Transaction.objects.all()
    return render(request, 'dds/index.html', dataset)

def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def get_statuses(request):
    statuses = Status.objects.values('id', 'name')
    return JsonResponse(list(statuses), safe=False)

def create_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        form = StatusForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=405)

def get_types(request):
    types = Type.objects.values('id', 'name')
    return JsonResponse(list(types), safe=False)

def create_type(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        form = TypeForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=405)

def create_category(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        form = CategoryForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=405)

def create_subcategory(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        form = SubcategoryForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=405)

def dictionaries(request):
    dataset = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'status_form': StatusForm(),
        'type_form': TypeForm(),
        'category_form': CategoryForm(),
        'subcategory_form': SubcategoryForm(),
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_status':
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dds:dictionaries')
        elif action == 'create_type':
            form = TypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dds:dictionaries')
        elif action == 'create_category':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dds:dictionaries')
        elif action == 'create_subcategory':
            form = SubcategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dds:dictionaries')
        elif action.startswith('delete_'):
            item_type, item_id = action.split('_')[1], action.split('_')[2]
            if item_type == 'status':
                Status.objects.filter(id=item_id).delete()
            elif item_type == 'type':
                Type.objects.filter(id=item_id).delete()
            elif item_type == 'category':
                Category.objects.filter(id=item_id).delete()
            elif item_type == 'subcategory':
                Subcategory.objects.filter(id=item_id).delete()
            return redirect('dds:dictionaries')

    return render(request, 'dds/dictionaries.html', dataset)