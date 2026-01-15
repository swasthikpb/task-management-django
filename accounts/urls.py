from django.urls import path
from .views import (
    web_login,
    admin_dashboard,
    admin_tasks,
    task_report,
    web_logout,
    manage_admins,
    manage_users, 
    create_user, 
    delete_user,
    assign_user_to_admin,
    admin_assign_user
)

urlpatterns = [
    path("", web_login),
    path("login/", web_login),
    path("logout/", web_logout),

    path("admin-panel/", admin_dashboard),
    path("admin-panel/tasks/", admin_tasks),
    path("admin-panel/tasks/<int:task_id>/report/", task_report),

    path("admin-panel/users/", manage_users),
    path("admin-panel/users/create/", create_user),
    path("admin-panel/users/delete/<int:user_id>/", delete_user),
    path("admin-panel/users/assign/", assign_user_to_admin),
    path("admin-panel/users/assign-self/", admin_assign_user),



    path("admin-panel/admins/", manage_admins),
    

   

]


