from django.urls import path
from .views import apply_job, MyApplicationsView
from .views import ManageApplicantsView
from .views import update_status
urlpatterns = [
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('my-applications/', MyApplicationsView.as_view(), name='my_applications'),
    path('manage/', ManageApplicantsView.as_view(), name='manage_applicants'),
    path('update/<int:app_id>/<str:status>/', update_status, name='update_status'),
]
