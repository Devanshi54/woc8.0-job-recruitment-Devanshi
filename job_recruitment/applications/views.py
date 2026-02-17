from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from jobs.models import Job
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django import forms
from .models import Notification
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only job seekers can apply
    if request.user.user_type != 'job_seeker':
        return redirect('home')

    # 🔥 Prevent duplicate application
    if Application.objects.filter(job=job, seeker=request.user).exists():
        return redirect('job_detail', pk=job.id)
    if Application.objects.filter(job=job, seeker=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('application_success')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employer_jobs = Job.objects.filter(employer=self.request.user)
        applications = Application.objects.filter(job__employer=self.request.user)

        context['total_jobs'] = employer_jobs.count()
        context['total_applications'] = applications.count()
        context['accepted_count'] = applications.filter(status="Accepted").count()

        return context


@login_required
def update_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.job.employer:
        return redirect('job_list')

    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        if status == "Rejected":
            Notification.objects.create(
                user=application.seeker,
                message=f"Application rejected for {application.job.title}"
            )

        messages.success(request, f"Application {status} successfully!")

        # 🔥 Prepare Email Context
        context = {
            'seeker_name': application.seeker.username,
            'job_title': application.job.title,
            'company_name': application.job.employer.username,
            'status': status,
        }

        # If accepted → add interview message
        if status == "Accepted":
            context['interview_message'] = "Our team will contact you soon regarding interview scheduling."

        # Render HTML template
        html_content = render_to_string(
            f'applications/emails/{status.lower()}_email.html',
            context
        )

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=f"Application {status} - {application.job.title}",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[application.seeker.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)

    return redirect('manage_applicants')


@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.user == application.seeker and application.status == "Pending":
        application.delete()
        messages.success(request, "Application withdrawn successfully.")

    return redirect('my_applications')
@login_required
def application_success(request):
    return render(request, 'applications/application_success.html')


class InterviewForm(forms.Form):
    interview_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )


@login_required
def schedule_interview(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Only employer can schedule
    if request.user != application.job.employer:
        return redirect('manage_applicants')

    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            application.interview_date = form.cleaned_data['interview_date']
            application.status = "Accepted"
            application.save()
            Notification.objects.create(
            user=application.seeker,
            message=f"Interview scheduled for {application.job.title}"
            )

            messages.success(request, "Interview scheduled successfully!")
            return redirect('manage_applicants')
    else:
        form = InterviewForm()

    return render(request, 'applications/schedule_interview.html', {
        'form': form,
        'application': application
    })
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'applications/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

