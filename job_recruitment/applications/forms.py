from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter','resume']
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if resume:
            # 2MB limit
            if resume.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Resume must be under 2MB.")

            # Only allow PDF
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Resume must be a PDF file.")

        return resume

class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['interview_date']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
