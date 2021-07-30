from .models import *
from .forms import *
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# ----University
class ResumeTemplateEducationUnversityUpdate(View):
    @method_decorator(login_required)
    def post(self, request):
        education_id = request.POST.get("education_id")
        educations = Education.objects.get(id=education_id)
        university = request.POST.get("university")
        educations.university = university
        educations.save()
        return HttpResponseRedirect("/resume1")

# ----Qualification Name
class ResumeTemplateEducationQualificationNameUpdate(View):
    @method_decorator(login_required)
    def post(self, request):
        education_id = request.POST.get("education_id")
        educations = Education.objects.get(id=education_id)
        qualification_name = request.POST.get("qualification_name")
        educations.qualification_name = qualification_name
        educations.save()
        return HttpResponseRedirect("/resume1")        

# ---- Year Of Passing
# class ResumeTemplateEducationYearOfPassingUpdate(View):
#     @method_decorator(login_required)
#     def post(self, request):
#         education_id = request.POST.get("education_id")
#         educations = Education.objects.get(id=education_id)
#         year_of_passing = request.POST.get("year_of_passing")
#         educations.year_of_passing = year_of_passing
#         educations.save()
#         return HttpResponseRedirect("/resume1")            

# ---- percentage or grade
class ResumeTemplateEducationPercentageOrGradeUpdate(View):
    @method_decorator(login_required)
    def post(self, request):
        education_id = request.POST.get("education_id")
        educations = Education.objects.get(id=education_id)
        percentage_or_grade = request.POST.get("percentage_or_grade")
        educations.percentage_or_grade = percentage_or_grade
        educations.save()
        return HttpResponseRedirect("/resume1")        
      



class ResumeTemplateEducationUnversityDelete(View):
    def get(self, request, id):
        education = Education.objects.get(id=id)
        education.delete()
        return redirect("resume1")
