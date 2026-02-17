from django.urls import path
from . import views
from .views import apply_job, MyApplicationsView,application_success
from .views import ManageApplicantsView
from .views import update_status
from .views import withdraw_application
from .views import apply_job, MyApplicationsView,schedule_interview
from .views import NotificationListView

urlpatterns = [
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('my-applications/', MyApplicationsView.as_view(), name='my_applications'),
    path('manage/', ManageApplicantsView.as_view(), name='manage_applicants'),
    path('update/<int:app_id>/<str:status>/', update_status, name='update_status'),
    path('withdraw/<int:pk>/', withdraw_application, name='withdraw_application'),
    path('success/', views.application_success, name='application_success'),
    path('schedule/<int:app_id>/', schedule_interview, name='schedule_interview'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),

]
