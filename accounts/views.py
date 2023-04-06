from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 있는지 검사하는 함수
from django.contrib import auth  # 사용자 auth 기능(비밀번호 체크, 로그인 기능 해결)
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated # 로그인 여부 검증
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')

        if password != password2:
            return render(request, 'accounts/signup.html', {'error': '패스워드를 다시 입력해 주세요.'})
        else:
            if username == '' or password == '':
                return render(request, 'accounts/signup.html', {'error': '이름과 비밀번호는 필수입니다.'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'accounts/signup.html', {'error': '이미 등록된 이름입니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
                return redirect('/login') # 회원가입 완료시 로그인 페이지로 이동

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return render(request, 'accounts/login.html', {'error': '빈칸을 입력해 주세요.'})
        else:
            me = auth.authenticate(request, username=username, password=password)
            if me is not None: # 저장된 패스워드와 입력받은 패스워드 비교
                auth.login(request, me)
                return redirect('/')
            else: # 로그인 실패시
                return render(request, 'accounts/login.html', {'error': '이름 혹은 패스워드가 틀렸습니다.'})
    elif request.method == 'GET':
        user = request.user.is_authenticated # 로그인 여부 검증
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/login.html')

@login_required() #로그인한 사용자만 접근할 수 있게 해주는 기능
def logout_view(request):
    auth.logout(request)
    return redirect('/')

