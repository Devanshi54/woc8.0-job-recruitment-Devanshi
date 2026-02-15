from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only job seekers can apply
    if request.user.user_type != 'job_seeker':
        return redirect('home')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {'form': form, 'job': job})
