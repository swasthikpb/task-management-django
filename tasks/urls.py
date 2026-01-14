from django.urls import path
from .views import  UserTaskListView,TaskUpdateView, TaskReportView, admin_create_task


urlpatterns = [
    path('tasks/', UserTaskListView.as_view()),
    path('tasks/<int:pk>/', TaskUpdateView.as_view()),
    path('tasks/<int:pk>/report/', TaskReportView.as_view()),

    path("admin-panel/tasks/create/", admin_create_task),

]