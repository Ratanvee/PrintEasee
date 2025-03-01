from django.urls import path
from .views import register, user_login, user_logout, dashboard, upload_document, home
from django.urls import path
# from .views import get_pending_orders, update_order_status
# from .views import dashboard, redirect_to_owner_dashboard
# from .views import get_print_jobs, complete_print_job
# from .views import get_pending_print_jobs, update_print_status, login_owner



from django.conf.urls import handler404
from users.views import custom_404_view  # Import the custom view

handler404 = custom_404_view


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/<int:user_id>/', dashboard, name='dashboard'),
    path('upload/<slug:unique_url>/', upload_document, name='upload_document'),
    # path("api/print-jobs/", get_pending_print_jobs, name="print-jobs"),
    # path("api/update-status/", update_print_status, name="update-status"),
    # path("api/login/", login_owner, name="login"),
]
