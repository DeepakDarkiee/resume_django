from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import formset_factory,modelformset_factory
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'full name', 'name': 'fname', 'id': 'fname'}),

            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email', 'name': 'email', 'id': 'email'}),
        }
        fields = ('email','username','password')
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title', 'name': 'title', 'id': 'title'}),
            'objective': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'objective', 'name': 'objective', 'id': 'objective'}),
        }
        fields = ("title", "objective")
class DateInput(forms.DateInput):
    input_type = 'date'
class ResumeUserDetailsForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "date_of_birth",
    }))
    class Meta:
        model = ResumeUserDetails
        fields = ['full_name','email', 'mobile','date_of_birth', 'address', 'photo']
        
class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ['qualification_name', 'year_of_passing',
                  'percentage_or_grade', 'university']

class ExperienceForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "start_date",
    }))
    end_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "end_date",
    }))
    class Meta:
        model = Experience
        fields = ['company_name', 'designation','start_date','end_date', 'role', 'place']
ExperienceFormSet = formset_factory(ExperienceForm,extra=1,max_num=None)
class WorkSamplesForms(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "date",
    }))
    class Meta:
        model = WorkSamples
        fields = ['project_name','project_link','technology','description','responsibilities','date']
class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your skills ', 'skills': 'Name', 'id': 'skills'}),
        }
        fields = ['skills'] 
# SkillsFormSet = formset_factory(SkillsForm,extra=1,max_num=None)
SkillsFormSet = modelformset_factory(Skills,fields=("skills",),extra=1 )
class HobbiesForm(forms.ModelForm):
    class Meta:
        model = Hobbies
        widgets = {
            'hobbies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Hobbies', 'name': 'hobbies', 'id': 'hobbies'}),
        }
        fields = ['hobbies']
HobbiesFormSet = formset_factory(HobbiesForm,extra=1,max_num=None)
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        widgets = {
            'certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificate', 'name': 'certificate', 'id': 'certificate'}),
        }
        fields = ['certificate']
CertificateFormSet = formset_factory(CertificateForm,extra=1,max_num=None)
class AchievementsForm(forms.ModelForm):
    class Meta:
        model = Achievements
        widgets = {
            'achievements': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievements', 'name': 'achievements', 'id': 'achievements'}),
        }
        fields = ['achievements']
AchievementsFormSet = formset_factory(AchievementsForm,extra=1,max_num=None)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first name', 'name': 'fname', 'id': 'fname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name', 'name': 'lname', 'id': 'lname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email', 'name': 'email', 'id': 'email'}),
        }
        fields = ('first_name', 'last_name', 'email','username','password')
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title', 'name': 'title', 'id': 'title'}),
            'objective': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'objective', 'name': 'objective', 'id': 'objective'}),
        }
        fields = ("title", "objective")
class DateInput(forms.DateInput):
    input_type = 'date'
class ResumeUserDetailsForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "date_of_birth",
    }))
    class Meta:
        model = ResumeUserDetails
        fields = ['full_name'
                  ,'email', 'mobile','date_of_birth', 'address', 'photo']

class ExperienceForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "start_date",
    }))
    end_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "end_date",
    }))
    class Meta:
        model = Experience
        fields = ['company_name', 'designation','start_date','end_date', 'role', 'place']
ExperienceFormSet = formset_factory(ExperienceForm,extra=1,max_num=None)
class WorkSamplesForms(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "date",
        'class': "form-control",
        'id': "date",
    }))
    class Meta:
        model = WorkSamples
        fields = ['project_name','project_link','technology','description','responsibilities','date']
class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your skills ', 'skills': 'Name', 'id': 'skills'}),
        }
        fields = ['skills'] 
# SkillsFormSet = formset_factory(SkillsForm,extra=1,max_num=None)
SkillsFormSet = modelformset_factory(Skills,fields=("skills",),extra=1 )
class HobbiesForm(forms.ModelForm):
    class Meta:
        model = Hobbies
        widgets = {
            'hobbies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Hobbies', 'name': 'hobbies', 'id': 'hobbies'}),
        }
        fields = ['hobbies']
HobbiesFormSet = formset_factory(HobbiesForm,extra=1,max_num=None)
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        widgets = {
            'certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificate', 'name': 'certificate', 'id': 'certificate'}),
        }
        fields = ['certificate']
CertificateFormSet = formset_factory(CertificateForm,extra=1,max_num=None)
class AchievementsForm(forms.ModelForm):
    class Meta:
        model = Achievements
        widgets = {
            'achievements': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievements', 'name': 'achievements', 'id': 'achievements'}),
        }
        fields = ['achievements']
AchievementsFormSet = formset_factory(AchievementsForm,extra=1,max_num=None)