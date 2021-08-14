import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.users.models import *


class ChooseTemplate(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    theme = models.ImageField(upload_to="theme/", blank=True)

    def __str__(self):
        return str(self.name)


class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(
        ChooseTemplate, on_delete=models.CASCADE, blank=True, null=True
    )  # change
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )  # change
    title = models.CharField(max_length=50)
    objective = models.TextField(max_length=200)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["id"]


class ResumeUserDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    photo = models.ImageField(default="../static/images/default_avatar.png", blank=True)
    # photo = models.ImageField(upload_to='images/' ,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.resume)


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    qualification_name = models.CharField(max_length=100)
    year_of_passing = models.CharField(max_length=100)
    percentage_or_grade = models.CharField(max_length=100)
    university = models.CharField(max_length=100)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100)
    role = models.CharField(max_length=1000)
    place = models.CharField(max_length=100)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class WorkSamples(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    project_name = models.CharField(max_length=100)
    project_link = models.CharField(max_length=100)
    technology = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    responsibilities = models.TextField(max_length=1000)
    logo = models.ImageField(upload_to="images/logos/")
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class Hobbies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    hobbies = models.CharField(max_length=100)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class Skills(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    skills = models.CharField(max_length=300)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    certificate = models.CharField(max_length=300)
    date_obtained = models.DateField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]


class Achievements(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)
    achievements = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resume)

    class Meta:
        ordering = ["date"]
