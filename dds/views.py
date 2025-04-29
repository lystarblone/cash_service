from django.shortcuts import render, redirect, get_object_or_404
from django import forms
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