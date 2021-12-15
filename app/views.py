from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST

from app.forms import LoginForm, SettingsForm


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
    return render(request, "question.html", {'question': questions[number]})


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
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
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
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = SettingsForm(initial=initial_data)
    elif request.method == 'POST':
        form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            redirect(reverse('settings'))
    return render(request, "settings.html", {'form': form})


def logout(request):
    auth.logout(request)


@login_required
@require_POST
def vote(request):
    question_id = request.POST['id']
    q = Question.objects.get(question_id)
    like = Like.objects.create(user=request.user, question=q)
    q.rating += 1
    q.save()
    return JsonResponse({})
