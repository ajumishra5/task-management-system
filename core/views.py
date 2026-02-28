from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from time import timezone
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Task, CustomUser

# Create your views here.

@login_required
def dashboard(request):
    total = Task.objects.filter(is_deleted=False).count()
    pending = Task.objects.filter(is_deleted=False, status="pending").count()
    completed = Task.objects.filter(is_deleted=False, status="completed").count()

    context = {
        "total": total,
        "pending": pending,
        "completed": completed,
    }

    return render(request, "core/dashboard.html", context)

@login_required
def task_list(request):

    tasks = Task.objects.filter(is_deleted=False).select_related("creator", "assigned_to")

    status = request.GET.get("status")
    priority = request.GET.get("priority")

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    paginator = Paginator(tasks.order_by("-created_at"), 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/task_list.html", {
        "page_obj": page_obj,
        "status": status,
        "priority": priority,
        #"now": timezone.now(),
    })

@login_required
def create_task(request):
    users = CustomUser.objects.filter(is_active=True, is_deleted=False)

    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority")
        assigned_to_id = request.POST.get("assigned_to")
        due_date = request.POST.get("due_date")

        if not title:
            messages.error(request, "Title is required.")
            return redirect("create_task")

        assigned_user = None
        if assigned_to_id:
            assigned_user = CustomUser.objects.filter(id=assigned_to_id).first()

        Task.objects.create(
            title=title,
            priority=priority,
            creator=request.user,
            assigned_to=assigned_user,
            due_date=due_date if due_date else None,
        )

        messages.success(request, "Task created successfully.")
        return redirect("task_list")

    return render(request, "core/task_form.html", {"users": users})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_deleted=False)

    if request.user != task.creator and not request.user.is_superuser:
        messages.error(request, "You are not allowed to edit this task.")
        return redirect("task_list")

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.priority = request.POST.get("priority")
        task.assigned_to_id = request.POST.get("assigned_to") or None
        task.due_date = request.POST.get("due_date") or None
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect("task_list")

    users = CustomUser.objects.filter(is_active=True, is_deleted=False)

    return render(
        request,
        "core/task_form.html",
        {
            "task": task,
            "users": users,
            "is_edit": True,
        },
    )

@login_required
def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_deleted=False)

    if request.user != task.assigned_to and not request.user.is_superuser:
        messages.error(request, "You cannot change status of this task.")
        return redirect("task_list")

    if request.method == "POST":
        task.status = request.POST.get("status")
        task.save()
        messages.success(request, "Status updated.")
        return redirect("task_list")

    return render(request, "core/change_status.html", {"task": task})


@login_required
def create_user(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to create users.")
        return redirect("task_list")

    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        role = request.POST.get("role")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect("create_user")

        CustomUser.objects.create(
            email=email,
            name=name,
            role=role,
            password=make_password(password),
            is_active=True,
        )

        messages.success(request, "User created successfully.")
        return redirect("task_list")

    return render(request, "core/create_user.html")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, is_deleted=False)

    if request.user != task.creator and not request.user.is_superuser:
        messages.error(request, "You are not allowed to delete this task.")
        return redirect("task_list")

    if task.status != "completed":
        messages.error(request, "Only completed tasks can be deleted.")
        return redirect("task_list")

    task.is_deleted = True
    task.save(update_fields=["is_deleted"])

    messages.success(request, "Task deleted successfully.")
    return redirect("task_list")

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Only superuser can delete users.")
        return redirect("task_list")

    user_obj = get_object_or_404(CustomUser, id=user_id, is_deleted=False)

    if user_obj == request.user:
        messages.error(request, "You cannot delete yourself.")
        return redirect("task_list")

    # Unassign pending tasks
    Task.objects.filter(
        assigned_to=user_obj,
        status="pending"
    ).update(assigned_to=None)

    user_obj.soft_delete()

    messages.success(request, "User deleted successfully.")
    return redirect("task_list")