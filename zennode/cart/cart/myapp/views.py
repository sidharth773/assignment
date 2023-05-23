from functools import total_ordering
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render
from .forms import UserForm
from .models import Mycart
from decimal import Decimal
from .forms import *

# Create your views here.
def home(request):
    return render(request,'myapp/home.html')

def signup(request):
    if request.method=='GET':
        context={
            'form1': UserForm(),
            'form2': MyCart()
        }
        return render(request,'myapp/signup.html', context=context)
    elif request.method=='POST':
        form1=UserForm(request.POST)
        form2=MyCart(request.POST)

        if form1.is_valid() and form2.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            obj1=form1.save(commit=False)
            obj2=form2.save(commit=False)
            obj1.set_password(form1.cleaned_data['password'])
            obj2.costm=obj1
            obj1.save()
            obj2.save()
            return render(request,'myapp/home.html')
        else:
                return render(request,'myapp/signup.html',context={'form1':form1,'form2':form2})
    return render(request,'myapp/home.html')
def login(request):
    if request.method=='GET':
        return render(request,'myapp/login.html')
    elif request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        user=authenticate(request, username=uname, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Failed")
        
def logout(request):
    logout(request)
    return redirect('signin')


def calculate_discount(subtotal, quantities):
    discount = Decimal(0)

    if subtotal > 200:
        discount = Decimal(10)

    for quantity in quantities:
        if quantity > 10:
            discount = max(discount, Decimal(0.05) * quantities[quantity])

    total_quantity = sum(quantities.values())
    if total_quantity > 20:
        discount = max(discount, Decimal(0.1) * subtotal)

    if total_quantity > 30 and any(quantity > 15 for quantity in quantities.values()):
        tiered_discount = Decimal(0.5) * sum(max(quantity - 15, 0) for quantity in quantities.values())
        discount = max(discount, tiered_discount)

    return discount

def calculate_total(subtotal, discount, quantities):
    gift_wrap_fee = sum(quantity for quantity in quantities.values())
    shipping_fee = (total_ordering// 10) * 5
    total = subtotal - discount + gift_wrap_fee + shipping_fee
    return total

def catalog(request):
    products = Mycart.objects.all()
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            quantities = {}
            subtotal = 0
            for product in products:
                quantity = form.cleaned_data.get(f'quantity_{product.id}')
                gift_wrap = form.cleaned_data.get(f'gift_wrap_{product.id}')
                if quantity:
                    quantities[product.id] = quantity
                    subtotal += product.price * quantity
                    if gift_wrap:
                        subtotal += quantity
            discount = calculate_discount(subtotal, quantities)
            total = calculate_total(subtotal, discount, quantities)
            return render(request, 'myapp/checkout.html', {
                'products': products,
                'quantities': quantities,
                'subtotal': subtotal,
                'discount': discount,
                'total': total,
            })
    return render(request, 'myapp/catalog.html', {'products': products, 'form': form})