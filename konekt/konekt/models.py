from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Candidate(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    link_cv = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'odf', 'odt'])
    ], blank=True, default='', upload_to='uploads/%Y/%m/%d/')
    status = models.CharField(max_length=200, blank=True, default='')
    availability = models.CharField(max_length=200, blank=True, default='')
    mobility = models.CharField(max_length=200, blank=True, default='')
    price = models.CharField(max_length=100, blank=True, default='')
    salary = models.CharField(max_length=100, blank=True, default='')
    job = models.CharField(max_length=100, blank=True, default='')
    scrapping_id = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('konekt:candidate_detail', kwargs={'pk': self.pk})


class Education(models.Model):
    date = models.CharField(max_length=200, blank=True, default='')
    name = models.CharField(max_length=4000, blank=True, default='')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations',)

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.name


class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    job_location = models.CharField(max_length=200, blank=True, default='')
    duration = models.CharField(max_length=200, blank=True, default='')
    description = models.CharField(max_length=4000, blank=True, default='')
    tools = models.CharField(max_length=400, blank=True, default='')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return self.job_title


class Score(models.Model):
    score = models.SmallIntegerField()
    comment = models.CharField(max_length=200, blank=True, default='')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return self.score

