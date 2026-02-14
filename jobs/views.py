from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job
@login_required
def post_job(request):
    if request.user.user_type != 'employer':
        return redirect('home')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('home')
    else:
        form = JobPostForm()

    return render(request, 'post_job.html', {'form': form})
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})
