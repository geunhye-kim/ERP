from django.contrib.auth.forms import UserModel
from django.shortcuts import render, redirect
from .models import Product, Inbound, Outbound
from accounts.models import UserModel
from django.http import HttpResponse
from django.contrib import auth  # 사용자 auth 기능(비밀번호 체크, 로그인 기능 해결)
from django.contrib.auth.decorators import login_required
from datetime import datetime


def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 여부 검증
        if user:
            return redirect('/inventory')
        else:
            return redirect('/login')

@login_required()
def inventory_show(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            product_list = Product.objects.all()
            user_name = request.user
            return render(request, 'erp/inventory.html', {'product_list': product_list, 'user_name': user_name})
        else:
            return redirect('/login')


def product_create(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code', '')  # 값이 비어있을 때 빈 문자열을 반환해 에러를 표시
        product_name = request.POST.get('product_name', '')
        product_size = request.POST.get('product_size', '')
        product_price = request.POST.get('product_price', '')
        product_desc = request.POST.get('product_desc', '')
        product_quantity = request.POST.get('product_quantity', 0)

        exist_product = Product.objects.filter(product_code=product_code)
        if exist_product.exists():
            return render(request, 'erp/product_create.html', {'error': '이미 등록되어 있는 상품 코드입니다.'})
        elif product_code == '' or product_name == '' or product_size == '상품 사이즈' or product_price == '' or product_desc == '':
            return render(request, 'erp/product_create.html', {'error': '빈칸을 입력해 주세요.'})
        else:
            Product.objects.create(product_code=product_code, product_name=product_name, product_size=product_size,
                                   product_price=product_price, product_desc=product_desc,
                                   product_quantity=product_quantity)
            product_list = Product.objects.all()
            return render(request, 'erp/inventory.html', {'product_list': product_list})
    else:
        return render(request, 'erp/product_create.html')


def inbound_create(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        return render(request, 'erp/inbound_create.html', {'product_list': product_list})

    elif request.method == 'POST':
        product_code = request.POST.get('product_code', '')
        inbound_quantity = request.POST.get('product_quantity', '')

        if product_code == '상품 코드':
            product_list = Product.objects.all()
            return render(request, 'erp/inbound_create.html', {'product_list': product_list, 'error': '상품 코드를 입력해 주세요.'})
        elif inbound_quantity == '':
            product_list = Product.objects.all()
            return render(request, 'erp/inbound_create.html', {'product_list': product_list, 'error': '수량을 입력해 주세요.'})
        else:
            product = Product.objects.get(product_code=product_code)
            product.product_quantity += int(inbound_quantity)
            product.save()

            Inbound.objects.create(product_id=product,
                                   inbound_quantity=int(inbound_quantity),
                                   inbound_date=datetime.now().date())

            product_list = Product.objects.all()
            return render(request, 'erp/inventory.html', {'product_list': product_list})

def outbound_create(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        return render(request, 'erp/outbound_create.html', {'product_list': product_list})

    elif request.method == 'POST':
        product_code = request.POST.get('product_code', '')
        outbound_quantity = request.POST.get('product_quantity', '')

        if product_code == '상품 코드':
            product_list = Product.objects.all()
            return render(request, 'erp/outbound_create.html', {'product_list': product_list, 'error': '상품 코드를 입력해 주세요.'})
        elif outbound_quantity == '':
            product_list = Product.objects.all()
            return render(request, 'erp/outbound_create.html', {'product_list': product_list, 'error': '수량을 입력해 주세요.'})

        product_quantity = Product.objects.get(product_code=product_code).product_quantity
        if int(outbound_quantity) > int(product_quantity):
            product_list = Product.objects.all()
            return render(request, 'erp/outbound_create.html', {'product_list': product_list, 'error': '출고량이 재고량보다 높을 수 없습니다.'})
        else:
            product = Product.objects.get(product_code=product_code)
            product.product_quantity -= int(outbound_quantity)
            product.save()

            Outbound.objects.create(product_id=product,
                                   outbound_quantity=int(outbound_quantity),
                                   outbound_date=datetime.now().date())

            product_list = Product.objects.all()
            return render(request, 'erp/inventory.html', {'product_list': product_list})

def inbound_list(request, id):
    if request.method == 'GET':
        product_id = Product.objects.get(id=id)
        product_name = Product.objects.get(id=id).product_name
        inbound_list = Inbound.objects.filter(product_id=product_id)
        return render(request, 'erp/inbound_list.html', {'product_name': product_name, 'inbound_list': inbound_list})

def outbound_list(request, id):
    if request.method == 'GET':
        product_id = Product.objects.get(id=id)
        product_name = Product.objects.get(id=id).product_name
        outbound_list = Outbound.objects.filter(product_id=product_id)
        return render(request, 'erp/outbound_list.html', {'product_name': product_name, 'outbound_list': outbound_list})
