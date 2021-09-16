import os

from django.contrib import messages
from django.forms import inlineformset_factory, TextInput, DateInput
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin, DetailView

from extraction_cv_informations.extraction_of_cv_infos import extraction_of_cv_infos
from . import forms
from .forms import CandidateForm, SearchCandidateES, EducationFormset, ExperienceFormset, SkillsFormset, \
    UploadCVForm
from .models import Candidate, Education, Skills, Experience, Score
from django.shortcuts import render, redirect, get_object_or_404
from .es_call import konekt, get_cv_by_id
from .fill_cvmodel import fill_cvmodel
from wsgiref.util import FileWrapper


def listing_cv(request):
    candidates = Candidate.objects.all()
    formated_candidates = ["<li>{}</li>".format(candidate.name) for candidate in candidates]
    message = """<ul>{}</ul>""".format("\n".join(formated_candidates))
    return HttpResponse(message)


def detail_candidate(request, candidate_id):
    # educations = Education.objects.get(pk=candidate_id)
    # candidate = " ".join([candidate.name for candidate in educations.candidate.all()])
    # experience = " ".join([experience.name for experience in candidate.experience.all()])
    candidate = Candidate.objects.get(pk=candidate_id)
    context = {'candidate': candidate}
    return render(request, 'candidate.html', context)


def search_candidate(request):
    query = request.GET.get('query')
    if not query:
        candidates = Candidate.objects.all()
    else:
        candidates = Candidate.objects.filter(name__icontains=query)

    if not candidates.exists():
        candidates = Candidate.objects.filter(education__name__icontains=query)

    if not candidates.exists():
        message = "Nous n'avons trouvé aucun résultat !"
    else:
        candidates = ["<li>{}.{}</li>".format(candidate.name, candidate.job) for candidate in candidates]
        message = """
            Nous avons trouvé les candidats correspondant à votre requête ! Les voici :
            <ul>{}</ul>
        """.format("<li></li>".join(candidates))

    return HttpResponse(message)


def search_index(request):
    job_term = request.GET['job'] if request.GET.get('job') else ""
    availability_term = request.GET['availability'] if request.GET.get('availability') else ""
    price_term = request.GET['price'] if request.GET.get('price') else ""
    mobility_term = request.GET['mobility'] if request.GET.get('mobility') else ""
    status_term = request.GET['status'] if request.GET.get('status') else ""
    experience_term = request.GET['experience'] if request.GET.get('experience') else ""
    skills_term = request.GET['skills'] if request.GET.get('skills') else ""
    search_term = job_term or availability_term or price_term or status_term or mobility_term or experience_term or skills_term
    results = konekt(job=job_term,
                     availability=availability_term,
                     price=price_term,
                     mobility=mobility_term,
                     status=status_term,
                     experience=experience_term,
                     skills=skills_term)

    form = SearchCandidateES(use_required_attribute=False)
    context = {'form': form, 'results': results, 'search_term': search_term, 'button': 'Chercher', 'title': 'Chercher un⸱e candidat⸱e'}
    return render(request, 'index.html', context)


def format_cv(request):
    formats = ['bti', 'yellow']
    sources = ['es', 'db']
    formatcv = request.GET['format'] if request.GET.get('format') in formats else ""
    cvid = request.GET['id'] if request.GET.get('id') else ""
    source = request.GET['source'] if request.GET.get('source') in sources else ""
    if source == 'es':
        results = get_cv_by_id(cvid=cvid)
    elif source == 'db':
        candidate = Candidate.objects.get(pk=cvid)
        educations = candidate.educations.all()
        experiences = candidate.experiences.all()
        skills = candidate.skills.all()
        results = {
            'candidate': candidate,
            'educations': educations,
            'experiences': experiences,
            'skills': skills
        }
    else:
        results = ""

    formatted_cv = fill_cvmodel(source, formatcv, results, cvid)
    print(formatted_cv)

    file = open(formatted_cv, 'rb')
    response = StreamingHttpResponse(FileWrapper(file), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+formatted_cv
    return response


def edit_candidate(request, candidate_id):
    if request.method == 'POST':
        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidateform = CandidateForm(request.POST or None, instance=candidate)
        educationformset = EducationFormset(request.POST or None, request.FILES, instance=candidate, prefix='education')
        experienceformset = ExperienceFormset(request.POST or None, request.FILES, instance=candidate, prefix='experience')
        skillsformset = SkillsFormset(request.POST or None, request.FILES, instance=candidate, prefix='skills')

        if candidateform.is_valid() and educationformset.is_valid() and experienceformset.is_valid() and skillsformset.is_valid():
            candidateform.save()
            educationformset.save()
            experienceformset.save()
            skillsformset.save()

            return redirect('/candidates/' + str(candidate.id))
    else:
        candidate = get_object_or_404(Candidate, id=candidate_id)

        if candidate.name == "":
            cv_infos = extraction_of_cv_infos(candidate.link_cv.path)

            candidate.name = cv_infos['name'].strip() if cv_infos['name'] else ""
            candidate.job = cv_infos['job'].strip() if cv_infos['job'] else ""
            candidate.phone = cv_infos['phone'].strip() if cv_infos['phone'] else ""
            candidate.email = cv_infos['email'].strip() if cv_infos['email'] else ""
            candidate.status = cv_infos['status'].strip() if cv_infos['status'] else ""
            candidate.availability = cv_infos['availability'].strip() if cv_infos['availability'] else ""
            candidate.price = cv_infos['price'].strip() if cv_infos['price'] else ""
            candidate.salary = cv_infos['salary'].strip() if cv_infos['salary'] else ""
            candidate.address = cv_infos['address'].strip() if cv_infos['address'] else ""
            candidate.mobility = cv_infos['mobility'].strip() if cv_infos['mobility'] else ""

            print("___________ before check_email ____________")
            print("___________ candidate.email ____________")
            print(candidate.email)
            check_email = Candidate.objects.filter(email=candidate.email).count()
            print("___________ after check_email ____________")
            print(check_email)
            if check_email:
                print("delete")
                candidate.delete()
                message = "Le candidat existe déjà."
                return HttpResponse(message)
            else:
                print("save")
                candidate.save()
                print("saved")

            # print("save")
            # candidate.save()
            # print("saved")

            education = Education(date=cv_infos['formations']['date'], name=str(cv_infos['formations']['name_of_diploma']))
            candidate.educations.add(education, bulk=False)

            i = 1
            print("__________________________CV EXP_____________________________")
            print(cv_infos['experience'])
            for e in cv_infos['experience']:
                exp = "exp"+str(i)
                duration = "duration"
                description = "description"
                job_title = "job_title"
                job_location = "job_location"
                tools = "tools"
                company_name = "company_name"
                experience = Experience(duration=cv_infos['experience'][i-1][exp][duration],
                                        description=cv_infos['experience'][i-1][exp][description],
                                        job_title=cv_infos['experience'][i-1][exp][job_title],
                                        job_location=cv_infos['experience'][i-1][exp][job_location],
                                        tools=cv_infos['experience'][i-1][exp][tools],
                                        company_name=cv_infos['experience'][i-1][exp][company_name])
                candidate.experiences.add(experience, bulk=False)
                i += 1

        candidateform = CandidateForm(instance=candidate)
        print("___________ candidateform ____________")
        print(candidateform)

        educationformset = EducationFormset(instance=candidate, prefix='education')
        experienceformset = ExperienceFormset(instance=candidate, prefix='experience')
        skillsformset = SkillsFormset(instance=candidate, prefix='skills')

    context = {
        'can_form': candidateform,
        'edu_formset': educationformset,
        'exp_formset': experienceformset,
        'skills_formset': skillsformset,
        'title': 'Modifier un⸱e candidat⸱e',
        'button': 'Mettre à jour',
        'action_form': 'konekt:edit_candidate',
        'edit': True,
        'candidate_id': candidate.id
    }
    return render(request, 'fullform.html', context)


def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()
    context = {}
    return render(request, 'delete.html', context)


def add_candidate(request, candidate_id=None):
    if candidate_id is None:
        candidate = Candidate()
    else:
        candidate = Candidate.objects.get(id=candidate_id)

    if request.method == 'POST':
        if request.FILES.get('link_cv'):
            cvform = UploadCVForm(request.POST, request.FILES)
            if cvform.is_valid():

                saved = cvform.save()
                return redirect('konekt:edit_candidate', candidate_id=saved.id)
            else:
                pass
        else:
            cvform = UploadCVForm()
            candidateform = CandidateForm(request.POST, instance=candidate)
            educationformset = EducationFormset(request.POST, request.FILES, instance=candidate, prefix='education')
            experienceformset = ExperienceFormset(request.POST, request.FILES, instance=candidate, prefix='experience')
            skillsformset = SkillsFormset(request.POST, request.FILES, instance=candidate, prefix='skills')
            if candidateform.is_valid() and educationformset.is_valid() and experienceformset.is_valid() and skillsformset.is_valid():
                if not Candidate.objects.filter(email=candidate.email).exists():
                    candidateform.save()
                    educationformset.save()
                    experienceformset.save()
                    skillsformset.save()
                else:
                    message = "Le candidat existe déjà."
                    return HttpResponse(message)

                if '_save' in request.POST:
                    return redirect('/cv/' + str(candidateform.id))
                if '_addanother' in request.POST:
                    return redirect('/add_candidate/')
    else:
        cvform = UploadCVForm()
        candidateform = CandidateForm(instance=candidate)
        educationformset = EducationFormset(instance=candidate, prefix='education')
        experienceformset = ExperienceFormset(instance=candidate, prefix='experience')
        skillsformset = SkillsFormset(instance=candidate, prefix='skills')

    context = {
        'cv_form': cvform,
        'can_form': candidateform,
        'edu_formset': educationformset,
        'exp_formset': experienceformset,
        'skills_formset': skillsformset,
        'title': 'Ajouter un⸱e candidat⸱e',
        'button': 'Enregistrer',
        'action_form': 'konekt:add_candidate'
    }
    return render(request, 'fullform.html', context)


class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidate_list.html'


class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidate_detail.html'


class CandidateCreateView(CreateView):
    """
    Only for creating a new candidate. Adding experiences to it is done in the
    CandidateExperiencesUpdateView().
    """
    form_class = CandidateForm
    model = Candidate
    template_name = 'candidate_create.html'
    # fields = '__all__'

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Le candidat a été créé.'
        )
        return super().form_valid(form)