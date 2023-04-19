from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app.forms import LoginForm, RegistrationForm


@login_required(login_url='login/', redirect_field_name='continue')
def index(request):
    return render(request, "index.html", {})


questions = [
    {
        "title": f"Title {i}",
        "text": f"This is text for {i} question.",
        "number": i,
    } for i in range(100)
]


def hot(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "hot.html", {'questions': content})


def question(request, number):
    return render(request, "question.html", {question[number]})


# @login_required()
# def ask(request):
#     if request.method == 'POST':
#         q_form = QuestionForm(data=request.POST)
#         if q_form.is_valid():
#             q=Question(**q_form.cleaned_data)
#             q.save()


@login_required
def settings(request):
    if request.method == 'GET':
        user_form = UserForm(data={'username': request.user.username})
    elif request.method == 'POST':
        user = User.objects.get(request.user.id)
        user.set_password()


@csrf_protect
def log_in(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                print('success!')
                return redirect(request.GET.get('continue'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, "login.html", context={'form': login_form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def signup(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "signup.html", {'form': user_form})
