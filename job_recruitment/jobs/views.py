from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from django.views.generic import ListView,DetailView
from .models import Job
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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
class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'
class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobPostForm
    template_name = 'post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.user_type == 'employer'
class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobPostForm
    template_name = 'post_job.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.employer
class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.employer

