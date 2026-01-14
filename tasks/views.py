from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from .serializers import TaskSerializer, TaskCompleteSerializer
from accounts.permissions import IsAdminOrSuperAdmin
from .models import Task
from accounts.models import User
from django.contrib.auth.decorators import login_required



class UserTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
class TaskReportView(generics.RetrieveAPIView):
    queryset = Task.objects.filter(status='COMPLETED')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]




@login_required
def admin_create_task(request):
    if request.user.role != "ADMIN":
        return redirect("/admin-panel/")

    users = User.objects.filter(assigned_admin=request.user)

    if request.method == "POST":
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            assigned_to=User.objects.get(id=request.POST["user"]),
            due_date=request.POST["due_date"],
        )
        return redirect("/admin-panel/tasks/")

    return render(request, "admin_create_task.html", {"users": users})
