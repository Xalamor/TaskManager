from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from .models import Task, Chapter
from .forms import TaskForm, UserRegisterForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    tasks = Task.objects.filter(
        models.Q(visibility='everyone') |
        models.Q(visibility='only_me', user=request.user) |
        models.Q(visibility='selected', user_can_read=request.user)
    ).distinct()

    context = {
        'tasks': tasks,
    }
    return render(request, 'main/index.html', context)


@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Связываем задачу с текущим пользователем перед сохранением
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect('/')
        else:
            error = 'Форма неверна'
    else:
        form = TaskForm()

    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'main/create.html', context)


@login_required
def about(request):
    return render(request, 'main/about.html')


@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    error = ''

    if task.user != request.user:
        messages.error(request, 'Вы не имеете права редактировать эту задачу.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        if 'save' in request.POST:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                form.save_m2m()  # save the many-to-many field after saving the task
                messages.success(request, 'Задача успешно обновлена.')
                return redirect('/')
            else:
                error = 'Форма неверна'
        elif 'delete' in request.POST:
            task.delete()
            messages.success(request, 'Задача успешно удалена.')
            return redirect('/')
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'error': error,
        'task': task,
    }
    return render(request, 'main/edit.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to home page or any desired page
            else:
                return HttpResponse("Authentication failed")
        else:
            # Handle form errors
            return render(request, 'registration/register.html', {'form': form, 'error': 'Form is not valid'})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def search(requset):
    query = requset.GET.get('query', '')
    chapter_id = requset.GET.get('chapter', '')

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(task__icontains=query)
    if chapter_id:
        tasks = tasks.filter(chapter_id=chapter_id)

    chapters = Chapter.objects.all()

    context = {
        'tasks': tasks,
        'chapters': chapters,
        'query': query,
        'chapter_id': chapter_id,
    }

    return render(requset, 'main/search_results.html', context)

# ДИМА ПИДОРАС