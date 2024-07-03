from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from .forms import TaskForm, UserRegisterForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # Фильтруем задачи по текущему пользователю
    tasks = Task.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/index.html', {'title': 'Главная страница',
                                               'tasks': tasks})

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
            return redirect('/')
        else:
            error = 'Форма неверна'

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
    if request.method == 'POST':
        if 'save' in request.POST:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                error = 'Форма неверна'
        elif 'delete' in request.POST:
            task.delete()
            return redirect('/')

    form = TaskForm(instance=task)
    context = {
        'form': form,
        'error': error,
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
