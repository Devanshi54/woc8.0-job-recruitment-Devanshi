from django.urls import path
from .views import post_job, JobListView,JobDetailView, JobCreateView, JobUpdateView, JobDeleteView


urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('post-job/', post_job, name='post_job'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='edit_job'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='delete_job'),
   


]
