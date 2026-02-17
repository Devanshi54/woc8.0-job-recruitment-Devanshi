from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from django.views.generic import ListView,DetailView
from applications.models import Application
from .models import Job
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

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

    return render(request, 'jobs/post_job.html', {'form': form})
class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 5   # 🔥 This enables pagination
    ordering = ['-date_posted']
    def get_queryset(self):
        queryset = Job.objects.all()

        # 🔍 Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        # 🟢 Job Type Filter
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        # 🟢 Location Filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        applied_job_ids = []

        if self.request.user.is_authenticated and self.request.user.user_type == "job_seeker":
            applied_job_ids = Application.objects.filter(
                seeker=self.request.user
            ).values_list('job_id', flat=True)

        context['applied_job_ids'] = applied_job_ids
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        already_applied = False
        application_status = None   # ✅ IMPORTANT: define it first

        if self.request.user.is_authenticated and self.request.user.user_type == "job_seeker":
            application = Application.objects.filter(
                job=self.object,
                seeker=self.request.user
            ).first()

            if application:
                already_applied = True
                application_status = application.status

        context['already_applied'] = already_applied
        context['application_status'] = application_status

        return context
class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobPostForm
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.user_type == 'employer'
class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobPostForm
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.employer
class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.employer

