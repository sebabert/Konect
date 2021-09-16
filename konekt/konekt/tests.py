from http import HTTPStatus

from django.test import TestCase
from konekt.forms import CandidateForm, EducationFormset, ExperienceFormset, SkillsFormset


class TestForms(TestCase):

    def test_candidate_form(self):
        form = CandidateForm({
            'name': 'Pierre Dupont',
            'job': 'DevOps',
            'address': 'Paris',
            'phone': '0123465789',
            'email': 'pierre@bti.com',
            'status': 'Freelance',
            'availability': 'Sous 3 mois',
            'mobility': 'Paris',
            'price': '600',
            'salary': ''
        })
        self.assertTrue(form.is_valid())

    def instantiate_formset(self, formset_class, data, instance=None, initial=None):
        prefix = formset_class().prefix
        formset_data = {}
        for i, form_data in enumerate(data):
            for name, value in form_data.items():
                if isinstance(value, list):
                    for j, inner in enumerate(value):
                        formset_data['{}-{}-{}_{}'.format(prefix, i, name, j)] = inner
                else:
                    formset_data['{}-{}-{}'.format(prefix, i, name)] = value
        formset_data['{}-TOTAL_FORMS'.format(prefix)] = len(data)
        formset_data['{}-INITIAL_FORMS'.format(prefix)] = 0

        if instance:
            return formset_class(formset_data, instance=instance, initial=initial)
        else:
            return formset_class(formset_data, initial=initial)

    def test_education_formset(self):
        formset = self.instantiate_formset(EducationFormset, [
            {
                'date': '01/01/2021',
                'name': 'Xxx',
            },
        ])
        self.assertTrue(formset.is_valid())

    def test_experiences_formset(self):
        formset = self.instantiate_formset(ExperienceFormset, [
            {
                'job_title': 'DevOps',
                'company_name': 'BTI',
                'job_location': 'Levallois',
                'duration': '12 mois',
                'description': 'cicd, cloud',
                'tools': 'azure, aws, jenkins',
            },
        ])
        self.assertTrue(formset.is_valid())

    def test_skills_formset(self):
        formset = self.instantiate_formset(SkillsFormset, [
            {
                'name': 'aws',
            },
        ])
        self.assertTrue(formset.is_valid())


class AddCandidateViewTests(TestCase):
    def test_get(self):
        response = self.client.get("/add_candidate/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<h1 class="title-huge">BTI Konekt - Ajouter un&middot;e candidat&middot;e</h1>', html=True)
