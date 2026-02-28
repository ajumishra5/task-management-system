from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  
    path("tasks/", views.task_list, name="task_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/status/", views.change_status, name="change_status"),
    path("users/create/", views.create_user, name="create_user"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("users/<int:user_id>/delete/", views.delete_user, name="delete_user"),
]
