from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import signup, user_login, user_logout, task_list, task_detail, task_create, task_update, task_delete, export_tasks

urlpatterns = [
    path('export/<str:format>/', login_required(views.export_tasks),name='export_tasks'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/new/', task_create, name='task_create'),
    path('task/<int:pk>/edit/', task_update, name='task_update'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
]