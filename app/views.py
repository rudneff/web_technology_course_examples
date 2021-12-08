from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from app.forms import LoginForm, UserForm


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


def login(request):
    print(request.POST)
    if request.method == 'GET':
        form = UserForm()
    elif request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            print(user)
            if not user:
                form.add_error(None, "User not found.")
            else:
                auth.login(request, user)
                return redirect(reverse('new'))
    return render(request, "login.html", {'form': form})


@login_required
def settings(request):
    if request.method == 'GET':
        user_form = UserForm(data={'username': request.user.username})
    elif request.method == 'POST':
        user = User.objects.get(request.user.id)
        user.set_password()


def logout(request):
    auth.logout(request)
