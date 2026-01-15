from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from .models import User


def web_login(request):
    if request.user.is_authenticated:
        return redirect("/admin-panel/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/admin-panel/")
        else:
            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "login.html")


@login_required
def admin_dashboard(request):
    if request.user.role not in ["ADMIN", "SUPERADMIN"]:
        return redirect("/login/")

    return render(request, "admin_dashboard.html")


@login_required
def admin_tasks(request):
    if request.user.role == "ADMIN":
        tasks = Task.objects.filter(assigned_to__assigned_admin=request.user)
    elif request.user.role == "SUPERADMIN":
        tasks = Task.objects.all()
    else:
        return redirect("/login/")

    return render(request, "admin_tasks.html", {"tasks": tasks})


@login_required
def task_report(request, task_id):
    if request.user.role not in ["ADMIN", "SUPERADMIN"]:
        return redirect("/login/")

    task = get_object_or_404(Task, id=task_id, status="COMPLETED")
    return render(request, "task_report.html", {"task": task})


def web_logout(request):
    logout(request)
    return redirect("/login/")

# users

@login_required
def manage_users(request):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    users = User.objects.filter(role="USER")
    return render(request, "manage_users.html", {"users": users})


@login_required
def create_user(request):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        user.role = request.POST["role"]
        user.save()
        if user.role == "ADMIN":
            return redirect("/admin-panel/admins/")
        else:
            return redirect("/admin-panel/users/")


    return render(request, "create_user.html")


@login_required
def delete_user(request, user_id):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    User.objects.filter(id=user_id).delete()
    return redirect("/admin-panel/users/")

@login_required
def assign_user_to_admin(request):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    users = User.objects.filter(role="USER")
    admins = User.objects.filter(role="ADMIN")

    if request.method == "POST":
        user = User.objects.get(id=request.POST["user"])
        admin = User.objects.get(id=request.POST["admin"])
        user.assigned_admin = admin
        user.save()
        return redirect("/admin-panel/users/")

    return render(request, "assign_user.html", {
        "users": users,
        "admins": admins
    })




# admin
@login_required
def manage_admins(request):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    admins = User.objects.filter(role="ADMIN")
    return render(request, "manage_admins.html", {"admins": admins})


@login_required
def create_admin(request):
    if request.user.role != "SUPERADMIN":
        return redirect("/admin-panel/")

    if request.method == "POST":
        admin = User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        admin.role = "ADMIN"
        admin.save()

        return redirect("/admin-panel/admins/")

    return render(request, "create_admin.html")

@login_required
def admin_assign_user(request):
    if request.user.role != "ADMIN":
        return redirect("/admin-panel/")

    # Only users with no assigned admin
    users = User.objects.filter(role="USER", assigned_admin__isnull=True)

    if request.method == "POST":
        user_id = request.POST.get("user")

        if not user_id:
            return render(request, "admin_assign_user.html", {
                "users": users,
                "error": "No user selected."
            })

        user = User.objects.get(id=user_id)
        user.assigned_admin = request.user
        user.save()

        return redirect("/admin-panel/users/")

    return render(request, "admin_assign_user.html", {"users": users})








