from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, register,profile
from .views import edit_profile, delete_account
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-account/', delete_account, name='delete_account'),

    path('password-reset/',
     auth_views.PasswordResetView.as_view(
         template_name='password_reset.html'
     ),
     name='password_reset'),

    path('password-reset/done/',
     auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
     ),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html'
     ),
     name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
    template_name='password_reset_complete.html'),
     name='password_reset_complete'),


]
