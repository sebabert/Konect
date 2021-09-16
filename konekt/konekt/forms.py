from django.forms import ModelForm, TextInput, EmailInput, DateInput, Textarea, Select, FileInput
from django import forms

from .models import Candidate, Experience, Skills, Education
from django.forms.models import inlineformset_factory


EducationFormset = inlineformset_factory(
    Candidate,
    Education,
    fields=('date', 'name',),
    extra=1,
    widgets={
        'date': DateInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Date', 'type': 'month'}),
        'name': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Nom du diplôme'}),
    },
    can_delete=True,
    labels={
        "date": "Date",
        "name": "Nom du diplôme"
    },
)


ExperienceFormset = inlineformset_factory(
    Candidate,
    Experience,
    fields=('job_title', 'company_name', 'job_location', 'duration', 'description', 'tools'),
    extra=1,
    widgets={
        'job_title': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Poste*'}),
        'company_name': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Entreprise*'}),
        'job_location': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Lieu'}),
        'duration': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Durée'}),
        'description': Textarea(attrs={'class': 'form-input', 'placeholder': 'Description', 'cols': '80', 'row': '80'}),
        'tools': TextInput(attrs={'class': 'form-input', 'placeholder': 'Outils'}),
    },
    can_delete=True,
    labels={
        "job_title": "Poste",
        "company_name": "Entreprise",
        "job_location": "Lieu",
        "duration": "Durée",
        "tools": "Outils"
    },
)


SkillsFormset = inlineformset_factory(
    Candidate,
    Skills,
    fields=('name',),
    extra=1,
    widgets={
        'name': TextInput(attrs={'class': 'form-input form-input-element', 'placeholder': 'Nom'}),
    },
    can_delete=True,
    labels={
        "name": "Nom"
    },
)


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'job', 'address', 'phone', 'email', 'status', 'availability', 'mobility', 'price', 'salary']
        STATUS_CHOICES = [
            ('', 'Statut'),
            ('Freelance', 'Freelance'),
            ('Salarié·e', 'Salarié·e'),
            ('Stagiaire', 'Stagiaire'),
            ('Autre', 'Autre')
        ]
        labels = {
            'name': 'Nom',
            'job': 'Poste',
            'address': 'Adresse',
            'phone': 'Téléphone',
            'email': 'Email',
            'status': 'Statut',
            'availability': 'Disponibilité',
            'mobility': 'Mobilité',
            'price': 'Tarif',
            'salary': 'Salaire',
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Nom'}),
            'job': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Poste'}),
            'address': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Adresse'}),
            'phone': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Téléphone'}),
            'email': EmailInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Email'}),
            'status': Select(choices=STATUS_CHOICES, attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Status'}),
            'availability': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Disponibilité'}),
            'mobility': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Mobilité'}),
            'price': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Tarif'}),
            'salary': TextInput(attrs={'class': 'form-input form-input-element--half', 'placeholder': 'Salaire'}),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        labels = {
            "job_title": "Poste",
            "company_name": "Entreprise",
            "job_location": "Lieu",
            "duration": "Durée",
            "tools": "Outils",
        }
        widgets = {
            'job_title': TextInput(attrs={'class': 'form-input', 'placeholder': 'Poste'}),
            'company_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Entreprise'}),
            'job_location': TextInput(attrs={'class': 'form-input', 'placeholder': 'Lieu'}),
            'duration': TextInput(attrs={'class': 'form-input', 'placeholder': 'Description'}),
            'description': TextInput(attrs={'class': 'form-input', 'placeholder': 'Description'}),
            'tools': TextInput(attrs={'class': 'form-input', 'placeholder': 'Description'}),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'class': 'form-input', 'placeholder': 'Date', 'type': 'date'}),
            'name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom'}),
        }


class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-input form-input-element', 'placeholder': 'Compétence'}),
        }


class UploadCVForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['link_cv']
        labels = {'link_cv': 'Importer un CV'}
        widgets = {
            'link_cv': FileInput,
        }


class SearchCandidateES(forms.Form):
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all())
    job = forms.CharField(
        label='Poste',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input',
                                                        'placeholder': 'Chercher par job'}))
    availability = forms.CharField(max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                                 'placeholder': 'Chercher par disponibilité'}))
    price = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                          'placeholder': 'Chercher par prix'}))
    mobility = forms.CharField(max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                             'placeholder': 'Chercher par mobilité'}))
    status = forms.CharField(max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                           'placeholder': 'Chercher par statut'}))
    experience = forms.CharField(max_length=200,
                                 widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                               'placeholder': "Chercher par années d'expérience"}))
    skills = forms.CharField(max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-input form-input-element--half',
                                                           'placeholder': 'Chercher par compétences'}))
