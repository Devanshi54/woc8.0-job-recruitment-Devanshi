from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from jobs.models import Job
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from django.contrib import messages


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only job seekers can apply
    if request.user.user_type != 'job_seeker':
        return redirect('home')

    # 🔥 Prevent duplicate application
    if Application.objects.filter(job=job, seeker=request.user).exists():
        return redirect('job_detail', pk=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})
class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(seeker=self.request.user)

class ManageApplicantsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/manage_applicants.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(job__employer=self.request.user)

@login_required
def update_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.job.employer:
        return redirect('job_list')

    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        messages.success(request, f"Application {status} successfully.")
    return redirect('manage_applicants')

@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.user == application.seeker and application.status == "Pending":
        application.delete()
        messages.success(request, "Application withdrawn successfully.")

    return redirect('my_applications')
