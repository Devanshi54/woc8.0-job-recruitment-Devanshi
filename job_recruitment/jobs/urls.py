from django.urls import path
from .views import post_job, job_list

urlpatterns = [
    path('post-job/', post_job, name='post_job'),
    path('', job_list, name='job_list'),


]
