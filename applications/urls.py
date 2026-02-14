from django.urls import path
from .views import apply_job

urlpatterns = [
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
]
