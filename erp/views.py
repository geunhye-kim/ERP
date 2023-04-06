from django.shortcuts import render, redirect
from .models import Product, Inbound, Outbound
from django.http import HttpResponse
from django.contrib import auth  # 사용자 auth 기능(비밀번호 체크, 로그인 기능 해결)
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user.is_authenticated # 로그인 여부 검증
    if user:
        return redirect('/inventory')
    else:
        return redirect('/login')


@login_required
def product_create(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code', '') # 값이 비어있을 때 빈 문자열을 반환해 에러를 표시
        product_name = request.POST.get('product_name', '')
        product_size = request.POST.get('product_size', '')
        product_price = request.POST.get('product_price', '')
        product_desc = request.POST.get('product_desc', '')
        product_quantity = request.POST.get('product_quantity', 0)

        if product_code == '' or product_name == '' or product_size == '' or product_price == '' or product_desc == '':
            return render(request, 'erp/product_create.html', {'error': '빈칸을 입력해 주세요.'})
        else:
            Product.objects.create(product_code=product_code, product_name=product_name, product_size=product_size,
                                   product_price=product_price, product_desc=product_desc, product_quantity=product_quantity)
            product_list = Product.objects.all()
            return render(request, 'erp/inventory.html', {'product_list': product_list})
    else:
        return render(request, 'erp/product_create.html')


@login_required
def inbound_create(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        return render(request, 'erp/inbound_create.html', {'product_list': product_list})

    elif request.method == 'POST':
        product_code = request.POST.get('product_code', '')  # code 값을 먼저 가져온 뒤
        inbound_quantity = request.POST.get('product_quantity', '')

        if product_code == '' or inbound_quantity == '':
            return render(request, 'erp/inbound_create.html', {'error': '빈칸을 입력해 주세요.'})
        else:
            product = Product.objects.get(product_code=product_code)
            product.product_quantity += int(inbound_quantity)
            product.save()
            product_list = Product.objects.all()
            inbound_date = Inbound.objects.inbound_date
            # inbound_date = inbound.inbound_date

            return render(request, 'erp/inventory.html', {'product_list': product_list, 'inbound_date': inbound_date})


def inventory_show(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            product_list = Product.objects.all()
            # inbound_quantity = Inbound.objects.get(product_code=product_list.product_code)
            # Product.product_quantity = Inbound.inbound_quantity
            return render(request, 'erp/inventory.html', {'product_list': product_list})
        else:
            return redirect('/login')
