import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import CustomUserCreationForm, CustomAuthenticationForm,TaskForm
from django.http import HttpResponse
from tablib import Dataset
from .resources import TaskResource
import json
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import messages
from django.db import transaction

# Create your views here.

logger = logging.getLogger(__name__)

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks' : tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task' : task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form' : form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form' : form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task' : task})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def export_tasks(request, format):
    """Export with versioning"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_resource = TaskResource()
    dataset = task_resource.export(request.user.task_set.filter(is_active=True))
    
    # Generate filename with username and timestamp
    filename = f"tasks_{request.user.username}_{timestamp}"
    
    if format == 'csv':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    elif format == 'json':
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
    elif format == 'pdf':
        # PDF generation code with version info
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Task Export - {filename}")
        y = 750
        for task in request.user.task_set.filter(is_active=True):
            y -= 20
            p.drawString(100, y, f"{task.title} - {'Completed' if task.completed else 'Pending'}")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    
    return response

