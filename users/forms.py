from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'address',
            'phone_number',
            'resume',
            'skills',
            'portfolio_url',
            'company_name',
            'company_website',
            'industry',
            'company_description'
        ]

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError("Resume must be a PDF file.")
        return resume
