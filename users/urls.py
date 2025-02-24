from django.urls import path
from .views import register, user_login, user_logout, dashboard, upload_document, home

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/<int:user_id>/', dashboard, name='dashboard'),
    path('upload/<slug:unique_url>/', upload_document, name='upload_document'),
]
