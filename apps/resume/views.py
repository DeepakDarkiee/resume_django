import datetime
# from .utils import render_to_pdf
from django.http import HttpResponse
from django.core import mail
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from resume_maker import settings
from django.http import HttpResponse
from collections import UserString
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserForm
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pdfkit
from .models import *
from apps.users.models import *
from .forms import *
import random
from datetime import date
import string
from django.contrib.auth.models import User
date = date.strftime
from django.contrib.auth import get_user_model
User = get_user_model()


def sign_up(request, id=None):
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        username = request.POST["username"]
        password = request.POST["password"]
        # print(request.POST['r_id'])
        # email = request.POST["email"]
        try:

            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, password=password)
            # resume_id = request.POST.get("r_id")
            if id is not None:
                resume = Resume.objects.get(id=id)
                resume.user = user
                resume.save()
            if user.is_active == False:
                return render(request, 'resume/sign_in.html')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                form = login(request, user)
                messages.success(request, f' welcome {username} !!')
                return redirect('dashboard')

        except IntegrityError as e:
            return render(request, "resume/sign_up.html", {"status": "Mr/Miss. {} your Account Already  Exist".format(username),'id':id})
    else:
        return render(request, "resume/sign_up.html",{'id':id})


def sign_in(request, id=None):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if id is not None:
            resume = Resume.objects.get(id=id)
            resume.user = user
            resume.save()
        if user is not None:    
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('dashboard')
        else:
            messages.info(request,f'account does not exist please sign in')
    form = AuthenticationForm()
    return render(request, 'resume/sign_in.html',{'id':id})


def mail(user, password):
    subject = "Greetings"
    msg = f"Congratulations for your successfull ResumeForm username {user} ,password {password}"
    to = "nisha.thoughtwin@gmail.com"
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if(res == 1):
        msg = "Mail Sent Successfully"
    else:
        msg = "Mail could not sent"
    return HttpResponse(msg)


class Home(View):
    def get(self, request):
        theme=ChooseTemplate.objects.all()
        response =HttpResponse("200 ok")
        response.set_cookie('last_work', '') 
        last_work=None
        try:
            last_work  = request.COOKIES['last_work']
        except KeyError as ke:
            pass
        return render(request, 'index.html',{'theme':theme,'last_work':last_work})


class Dashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        # import pdb
        # pdb.set_trace()
        user = request.user
        resume = Resume.objects.filter(user=user)
        return render(request, 'resume/dashboard.html', {'resume': resume, })


class FresherResumeInput(View):

    def post(self, request):
        if request.method == 'POST':

            print(request.POST)
            template_id = request.POST.get('template_id')
            template = ChooseTemplate.objects.get(id=template_id)

            title = request.POST.get('resume_title')
            objective = request.POST.get('resume_objective')
            resume = Resume(title=title, objective=objective)

            resume.template = template

            resume.save()

            # handel skills

            skills = request.POST.getlist("skills")
            for skill in skills:
                skill = Skills.objects.create(resume=resume, skills=skill)

             # handel hobbies:
            hobbies = request.POST.getlist("hobbies")
            for hobby in hobbies:
                hobby = Hobbies.objects.create(resume=resume, hobbies=hobby)

            # handel achievements:
            achievements = request.POST.getlist("achievements")
            for achievement in achievements:
                achievement = Achievements.objects.create(
                    resume=resume, achievements=achievement)

            # handle certifications:
            certificates = request.POST.getlist("certificate")
            for certificate in certificates:
                certificate = Certificate.objects.create(
                    resume=resume, certificate=certificate)

            # handle Education request
            education = request.POST.getlist('qualification_name')
            e = 1
            temp_j = []
            temp_k = []
            temp_l = []

            for i in education:
                i = Education(resume=resume, qualification_name=i)
                for j in request.POST.getlist('year_of_passing'):
                    if e < len(request.POST.getlist('year_of_passing')) and j not in temp_j:
                        i.year_of_passing = j
                        temp_j.append(j)
                        break
                    else:
                        i.year_of_passing = j

                for k in request.POST.getlist('percentage_or_grade'):
                    if e < len(request.POST.getlist('percentage_or_grade')) and k not in temp_k:
                        i.percentage_or_grade = k
                        temp_k.append(k)
                        break
                    else:
                        i.percentage_or_grade = k

                for l in request.POST.getlist('university'):
                    if e < len(request.POST.getlist('university')) and l not in temp_l:
                        i.university = l
                        temp_l.append(l+"1")
                        break
                    else:
                        i.university = l

                i.save()
                e = e+1

                i.save()
                e = e+1

        if request.user.is_authenticated:
            user = request.user
            resume.user = user
            resume.save()
            return redirect('dashboard')

        else:

            return render(request, 'resume/thank-you.html', {'resume': resume})


class ExperienceResumeInput(View):
    # def get(self, request):
    #     form1 = ResumeForm

    #     form2 = ResumeUserDetailsForm

    #     form3 = EducationForm

    #     form4 = ExperienceForm
    #     form5 = WorkSamplesForms
    #     form6 = SkillsForm
    #     form7 = HobbiesForm
    #     form8 = CertificateForm
    #     form9 = AchievementsForm
    #     context = {'form1': form1, 'form2': form2,
    #                'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, }
    #     return render(request, 'resume/experience.html', context)

    def post(self, request):
        if request.method == 'POST':

            print(request.POST)
            template_id = request.POST.get('template_id')
            template = ChooseTemplate.objects.get(id=template_id)

            title = request.POST.get('resume_title')
            objective = request.POST.get('resume_objective')
            resume = Resume(title=title, objective=objective)

            resume.template = template

            resume.save()

            # handle resume user details

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            date_of_birth = request.POST.get('date_of_birth')
            address = request.POST.get('address')
            photo = request.FILES.get('photo')
            resume_user = ResumeUserDetails(resume=resume,
                                            email=email, mobile=mobile, date_of_birth=date_of_birth, address=address, photo=photo)
            resume_user.save()

            # handel skills

            skills = request.POST.getlist("skills")
            for skill in skills:
                skill = Skills.objects.create(resume=resume, skills=skill)

             # handel hobbies:
            hobbies = request.POST.getlist("hobbies")
            for hobby in hobbies:
                hobby = Hobbies.objects.create(resume=resume, hobbies=hobby)

            # handel achievements:
            achievements = request.POST.getlist("achievements")
            for achievement in achievements:
                achievement = Achievements.objects.create(
                    resume=resume, achievements=achievement)

            # handle certifications:
            certificates = request.POST.getlist("certificate")
            for certificate in certificates:
                certificate = Certificate.objects.create(
                    resume=resume, certificate=certificate)

            # handle Education request
            education = request.POST.getlist('qualification_name')
            e = 1
            temp_j = []
            temp_k = []
            temp_l = []

            for i in education:
                i = Education(resume=resume, qualification_name=i)
                for j in request.POST.getlist('year_of_passing'):
                    if e < len(request.POST.getlist('year_of_passing')) and j not in temp_j:
                        i.year_of_passing = j
                        temp_j.append(j)
                        break
                    else:
                        i.year_of_passing = j

                for k in request.POST.getlist('percentage_or_grade'):
                    if e < len(request.POST.getlist('percentage_or_grade')) and k not in temp_k:
                        i.percentage_or_grade = k
                        temp_k.append(k)
                        break
                    else:
                        i.percentage_or_grade = k

                for l in request.POST.getlist('university'):
                    if e < len(request.POST.getlist('university')) and l not in temp_l:
                        i.university = l
                        temp_l.append(l+"1")
                        break
                    else:
                        i.university = l

                i.save()
                e = e+1

            # handle Experience request
            experience = request.POST.getlist('company_name')
            e = 1
            temp_j = []
            temp_k = []
            temp_l = []
            temp_m = []
            temp_n = []

            for i in experience:
                i = Experience(resume=resume, company_name=i)
                for j in request.POST.getlist('start_date'):
                    if e < len(request.POST.getlist('start_date')) and j not in temp_j:
                        i.start_date = j
                        temp_j.append(j)
                        break
                    else:
                        i.start_date = j
                for k in request.POST.getlist('end_date'):
                    if e < len(request.POST.getlist('end_date')) and k not in temp_k:
                        i.end_date = k
                        temp_k.append(k)
                        break
                    else:
                        i.end_date = k
                for l in request.POST.getlist('designation'):
                    if e < len(request.POST.getlist('designation')) and l not in temp_l:
                        i.designation = l
                        temp_l.append(l)
                        break
                    else:
                        i.designation = l

                for m in request.POST.getlist('role'):
                    if e < len(request.POST.getlist('role')) and m not in temp_m:
                        i.role = m
                        temp_m.append(m)
                        break
                    else:
                        i.role = m

                for n in request.POST.getlist('place'):
                    if e < len(request.POST.getlist('place')) and n not in temp_n:
                        i.place = n
                        temp_n.append(n)
                        break
                    else:
                        i.place = n
                i.save()
                e = e+1


# handle worksample request
            worksamples = request.POST.getlist('project_name')
            e = 1
            temp_j = []
            temp_k = []
            temp_l = []
            temp_m = []
            temp_n = []
            temp_o = []
            for i in worksamples:
                i = WorkSamples(resume=resume, project_name=i)
                for j in request.POST.getlist('project_link'):
                    if e < len(request.POST.getlist('project_link')) and j not in temp_j:
                        i.project_link = j
                        temp_j.append(j)
                        break
                    else:
                        i.project_link = j
                for k in request.POST.getlist('technology'):
                    if e < len(request.POST.getlist('technology')) and k not in temp_k:
                        i.technology = k
                        temp_k.append(k)
                        break
                    else:
                        i.technology = k
                for l in request.POST.getlist('description'):
                    if e < len(request.POST.getlist('description')) and l not in temp_l:
                        i.description = l
                        temp_l.append(l)
                        break
                    else:
                        i.description = l
                for m in request.POST.getlist('responsibilities'):
                    if e < len(request.POST.getlist('responsibilities')) and m not in temp_m:
                        i.responsibilities = m
                        temp_m.append(m)
                        break
                    else:
                        i.responsibilities = m

                for n in request.POST.getlist('date'):
                    if e < len(request.POST.getlist('date')) and n not in temp_n:
                        i.date = n
                        temp_n.append(n)
                        break
                    else:
                        i.date = n

                i.save()
                e = e+1

            print(request.POST)
            if request.user.is_authenticated:
                user = request.user
                resume.user = user
                resume.save()
                return redirect('dashboard')

            else:

                return render(request, 'resume/thank-you.html', {'resume': resume})


@method_decorator(login_required, name='dispatch')
class GenratePdf(View):
    def post(self, request):
        if request.method == 'POST':
            url = request.POST.get('temp_url')
            pdf = pdfkit.from_url(url, 'file1.pdf')
            # resume = Resume.objects.create(resume=pdf)
            return HttpResponse('download success')


class Template(View):
    def get(self, request):
        context = {}
        user = request.user
        resume = Resume.objects.filter(user=user).last()
        context['resume'] = resume

        return render(request, 'resume/template.html', context)


@method_decorator(login_required, name='dispatch')
class Template1(View):
    def get(self, request):
        context = {}
        skillsform = SkillsForm
        educationform = EducationForm
        experienceform = ExperienceForm
        user = request.user
        resume = Resume.objects.filter(user=user).last()
        context['resume'] = resume
        context['educationform'] = educationform
        context['experienceform'] = experienceform
        context['skillsform'] = skillsform

        return render(request, 'resume/template1.html', context)

# @method_decorator(login_required, name='dispatch')
# class Template1(View):
#     def get(self, request):
#         context = {}
#         user = request.user
#         resume = Resume.objects.get(user=user)
#         context['resume'] = resume

#         return render(request, 'resume/template1.html', context)


@method_decorator(login_required, name='dispatch')
class Template2(View):
    def get(self, request):
        return render(request, 'resume/template2.html')


def logout_request(request):
    logout(request)
    return redirect("/")


class Template3(View):
    def get(self, request):
        context = {}
        user = request.user
        resume = Resume.objects.get(user=user)
        context['resume'] = resume

        return render(request, 'resume/template3.html', context)


class Template4(View):
    def get(self, request):
        context = {}
        user = request.user
        resume = Resume.objects.filter(user=user).last()
        context['resume'] = resume

        return render(request, 'resume_templates/template4.html', context)


# poornima....................................................................
class Template5(View):
    def get(self, request):
        context = {}
        user = request.user
        resume = Resume.objects.get(user=user)
        context['resume'] = resume
        print(resume.education_set.all())
        # mail(resume)
        return render(request, 'resume/template5.html', context)


class ViewResumeDetail(View):
    @method_decorator(login_required)
    def get(self, request, id):
        resume = Resume.objects.get(pk=id)
        print('...........', resume)
        eduform = EducationForm()
        education = Education.objects.filter(resume=resume)
        skillsform = SkillsForm()
        skills = Skills.objects.filter(resume=resume)
        hobbiesform = HobbiesForm()
        hobbies = Hobbies.objects.filter(resume=resume)
        achievementsform = AchievementsForm()
        achievements = Achievements.objects.filter(resume=resume)
        experienceform = ExperienceForm()
        experience = Experience.objects.filter(resume=resume)
        worksamplesform = WorkSamplesForms()
        worksamples = WorkSamples.objects.filter(resume=resume)
        certificateform = CertificateForm()
        certificate = Certificate.objects.filter(resume=resume)
        # languageform = LanguageForm()
        # language = Language.objects.filter(resume=resume)
        context = {'resume': resume, 'eduform': eduform, 'education': education, 'skillsform': skillsform, 'skills': skills, 'hobbiesform': hobbiesform,
                   'hobbies': hobbies, 'achievementsform': achievementsform, 'achievements': achievements, 'experienceform': experienceform, 'experience': experience,
                   'worksamplesform': worksamplesform, 'worksamples': worksamples, 'certificateform': certificateform, 'certificate': certificate,
                   }
        return render(request, 'resume/updatedata.html', context)


# poornima...........................................................

class AddEducation(View):
    @method_decorator(login_required)
    def post(self, request, id):

        resume = Resume.objects.get(pk=request.POST.get('id'))
        qualification = request.POST.get("qualification_name")
        year = request.POST.get("year_of_passing")
        percentage = request.POST.get("percentage_or_grade")
        university = request.POST.get("university")
        addeducation = Education(resume=resume, qualification_name=qualification,
                                 year_of_passing=year, percentage_or_grade=percentage, university=university)

        addeducation.save()
        print(request.POST)

        return redirect("template1")


class UpdateEducation(View):

    @method_decorator(login_required)
    def post(self, request):

        degree = request.POST.get("qualification_name")
        year = request.POST.get("year_of_passing")
        percentage = request.POST.get("percentage_or_grade")
        university = request.POST.get("university")

        upd_education = Education.objects.get(id=request.POST.get('id'))
        upd_education.qualification_name = degree
        upd_education.year_of_passing = year
        upd_education.percentage_or_grade = percentage
        upd_education.university = university
        upd_education.save()

        print(request.POST)
        resume_id = request.POST.get("r_id")
        return redirect("template1")


class DeleteEducation(View):

    def post(self, request):
        edu = Education.objects.get(id=request.POST.get("e_id"))
        edu.delete()
        resume_id = request.POST.get("r_id")
        return redirect("updateresume", id=resume_id)


# poornima...........................................................

class AddSkillsData(View):
    @method_decorator(login_required)
    @method_decorator(login_required)
    def post(self, request, *args):
        resume_id = request.POST.get("id")

        resume = Resume.objects.get(id=resume_id)
        skills = request.POST.get("skills")
        addskills = Skills(resume=resume)
        addskills.skills = skills
        addskills.save()

        return redirect("updateresume", id=resume.id)


class UpdateSkills(View):

    @method_decorator(login_required)
    def post(self, request):
        skill = Skills.objects.get(id=request.POST.get("id"))
        skill.skills = request.POST.get("skills")
        skill.save()

        resume_id = request.POST.get("r_id")
        return redirect("resume", id=resume_id)


class DeleteSkills(View):
    @method_decorator(login_required)
    def get(self, request, id):

        skills = Skills.objects.get(id=id)

        skills.delete()

        return HttpResponseRedirect("/dashboard/")
# ..................................................................


class AddHobbiesData(View):

    @method_decorator(login_required)
    def post(self, request):
        resume = Resume.objects.get(id=request.POST.get("id"))
        print(resume.id)
        hobbies = request.POST.get("hobbies")
        addhobbies = Hobbies(resume=resume)
        addhobbies.hobbies = hobbies
        addhobbies.save()
        print(request.POST)
        print(resume)
        resume_id = request.POST.get("r_id")
        return redirect("updateresume", id=resume.id)


class UpdateHobbies(View):

    @method_decorator(login_required)
    def post(self, request):
        hobbies = Hobbies.objects.get(id=request.POST.get("id"))
        hobbies.hobbies = request.POST.get("hobbies")
        hobbies.save()

        resume_id = request.POST.get("r_id")
        return redirect("updateresume", id=resume_id)


class DeleteHobbies(View):

    def get(self, request, id):
        hobbies = Hobbies.objects.get(id=id)
        hobbies.delete()
        return redirect("dashboard")

# .................................................................


class AddAchievementsData(View):

    @method_decorator(login_required)
    def post(self, request):
        resume = Resume.objects.get(id=request.POST.get("id"))
        print(resume.id)
        achievements = request.POST.get("achievements")
        addachievements = Achievements(resume=resume)
        addachievements.achievements = achievements
        addachievements.save()
        print(request.POST)
        print(resume)

        return redirect("updateresume", id=resume.id)


class UpdateAchievements(View):

    @method_decorator(login_required)
    def post(self, request):
        achievement = Achievements.objects.get(id=request.POST.get("id"))
        achievement.achievements = request.POST.get("achievements")
        achievement.save()

        resume_id = request.POST.get("r_id")
        return redirect("updateresume", id=resume_id)


class DeleteAchievements(View):
    @method_decorator(login_required)
    def get(self, request, id):
        achievements = Achievements.objects.get(id=id)
        achievements.delete()
        return HttpResponseRedirect("/dashboard")
# ..................................................................


class AddExperienceData(View):
    @method_decorator(login_required)
    def post(self, request):

        resume = Resume.objects.get(pk=request.POST.get('id'))
        company_name = request.POST.get("company_name")
        designation = request.POST.get("designation")
        role = request.POST.get("role")
        place = request.POST.get("place")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        addexperience = Experience(resume=resume, company_name=company_name, designation=designation,
                                   start_date=start_date, end_date=end_date, role=role, place=place)

        addexperience.save()
        print(request.POST)

        return redirect("template1")


class UpdateExperience(View):

    @method_decorator(login_required)
    def post(self, request):
        experience = Experience.objects.get(id=request.POST.get("id"))
        experience.company_name = request.POST.get("company_name")
        experience.designation = request.POST.get("designation")
        experience.role = request.POST.get("role")
        experience.place = request.POST.get("place")
        experience.start_date = request.POST.get("start_date")
        experience.end_date = request.POST.get("end_date")

        experience.save()

        resume_id = request.POST.get("r_id")
        return redirect("template1")


class DeleteExperience(View):
    @method_decorator(login_required)
    def post(self, request):
        experience = Experience.objects.get(id=request.POST.get("ex_id"))
        experience.delete()
        resume_id = request.POST.get("r_id")
        return redirect("template1")

# ..............................................................................


class AddWorkSamples(View):
    @method_decorator(login_required)
    def post(self, request):

        resume = Resume.objects.get(pk=request.POST.get('id'))
        project_name = request.POST.get("project_name")
        project_link = request.POST.get("project_link")
        technology = request.POST.get("technology")
        description = request.POST.get("description")
        responsibilities = request.POST.get("responsibilities")
        date = request.POST.get("date")

        addworksample = Experience(resume=resume, project_name=project_name, project_link=project_link,
                                   technology=technology, description=description, responsibilities=responsibilities, date=date)

        addworksample.save()
        print(request.POST)

        return redirect("template1")


class UpdateWorkSamples(View):

    @method_decorator(login_required)
    def post(self, request):
        worksamples = WorkSamples.objects.get(id=request.POST.get("id"))
        worksamples.project_name = request.POST.get("project_name")
        worksamples.project_link = request.POST.get("project_link")
        worksamples.technology = request.POST.get("technology")
        worksamples.description = request.POST.get("description")
        worksamples.responsibilities = request.POST.get("responsibilities")

        worksamples.save()

        resume_id = request.POST.get("r_id")
        return redirect("template1")


class DeleteWorkSamples(View):
    @method_decorator(login_required)
    def post(self, request):
        worksamples = WorkSamples.objects.get(id=request.POST.get("w_id"))
        worksamples.delete()
        resume_id = request.POST.get("r_id")
        return redirect("template1")

# ..............................................................................


def choose_template1(request):

    form1 = ResumeForm

    form2 = ResumeUserDetailsForm

    form3 = EducationForm

    form4 = ExperienceForm
    form5 = WorkSamplesForms
    form6 = SkillsForm
    form7 = HobbiesForm
    form8 = CertificateForm
    form9 = AchievementsForm
    template1 = "resume_templates/template1.html"
    choose_template = ChooseTemplate.objects.create(name=template1)
    context = {'form1': form1, 'form2': form2, 'template': choose_template,
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, }
    return render(request, 'resume/template.html', context)


def choose_template2(request):

    form1 = ResumeForm
    form2 = ResumeUserDetailsForm
    form3 = EducationFormSet(queryset=Education.objects.none())
    form4 = ExperienceForm
    form5 = WorkSamplesForms
    form6 = SkillsFormSet(queryset=Skills.objects.none())
    form7 = HobbiesForm
    form8 = CertificateForm
    form9 = AchievementsForm

    template2 = "resume_templates/template2.html"
    choose_template = ChooseTemplate.objects.create(name=template2)
    context = {'form1': form1, 'form2': form2, 'template': choose_template,
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, }

    return render(request, 'resume/fresher.html', context)


def choose_template3(request):

    form1 = ResumeForm
    form2 = ResumeUserDetailsForm
    form3 = EducationFormSet(queryset=Education.objects.none())
    form4 = ExperienceForm
    form5 = WorkSamplesForms
    form6 = SkillsFormSet(queryset=Skills.objects.none())
    form7 = HobbiesForm
    form8 = CertificateForm
    form9 = AchievementsForm

    template3 = "resume_templates/template3.html"
    choose_template = ChooseTemplate.objects.create(name=template3)
    context = {'form1': form1, 'form2': form2, 'template': choose_template,
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, }

    return render(request, 'resume/fresher.html', context)


def choose_template4(request):

    form1 = ResumeForm
    form2 = ResumeUserDetailsForm
    form3 = EducationFormSet(queryset=Education.objects.none())
    form4 = ExperienceForm
    form5 = WorkSamplesForms
    form6 = SkillsFormSet(queryset=Skills.objects.none())
    form7 = HobbiesForm
    form8 = CertificateForm
    form9 = AchievementsForm

    template4 = "resume_templates/template4.html"
    choose_template = ChooseTemplate.objects.create(name=template4)
    context = {'form1': form1, 'form2': form2, 'template': choose_template,
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, }

    return render(request, 'resume/fresher.html', context)


def choose(request):
    return render(request, 'resume/choose-template.html')


@method_decorator(login_required, name='dispatch')
class Resume_Update(View):
    def get(self, request):
        return render(request, 'resume/Update-resume.html')


@method_decorator(login_required, name='dispatch')
class Resume_Update(View):
    def get(self, request):
        return render(request, 'resume/Update-resume.html')


def test(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse("Done")
    else:
        print("none")
        return HttpResponse("None")





# Add template
class AddAnother(View):
    def post(self, request, id):
        resume = Resume.objects.get(id=id)
        element = request.POST.get('element')
        if element == 'education':
            education = Education.objects.create()
            education.resume = resume
            education.save()

        if element == 'skills':
            skills = Skills.objects.create()
            skills.resume = resume
            skills.save()

        if element == 'experience':
            experience = Experience.objects.create()
            experience.resume = resume
            experience.save()

        if element == 'worksamples':
            worksamples = WorkSamples.objects.create()
            worksamples.resume = resume
            worksamples.save()

        if element == 'achievements':
            achievements = Achievements.objects.create()
            achievements.resume = resume
            achievements.save()

        if element == 'certificate':
            certificate = Certificate.objects.create()
            certificate.resume = resume
            certificate.save()

        if element == 'hobbies':
            hobbies = Hobbies.objects.create()
            hobbies.resume = resume
            hobbies.save()

        return HttpResponse("200 ok")


# Create for template
class CreateResumeView(View):
    def get(self, request,id, *args, **kwargs):
        resume = Resume.objects.create()
        template=ChooseTemplate.objects.get(id=id)
        resume.template=template
        resume.save()
        experience = Experience.objects.create(resume=resume)
        work_samples = WorkSamples.objects.create(resume=resume)
        achievement = Achievements.objects.create(resume=resume)
        certificate = Certificate.objects.create(resume=resume)
        education = Education.objects.create(resume=resume)
        skills = Skills.objects.create(resume=resume)
        hobbies = Hobbies.objects.create(resume=resume)
        resume_user_data = ResumeUserDetails.objects.create(resume=resume)
        return redirect(f'/update_data/{resume.id}')



# Delete for template


class DeleteExperience(View):

    def get(self, request, id):
        experience = Experience.objects.get(id=id)
        experience.delete()

        resume_id = experience.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteExperience(View):

    def get(self, request, id):
        experience = Experience.objects.get(id=id)
        experience.delete()

        resume_id = experience.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))




class DeleteEducation(View):

    def get(self, request, id):
        education = Education.objects.get(id=id)
        education.delete()

        resume_id = education.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteWorkSamples(View):

    def get(self, request, id):
        deleteworksamples = WorkSamples.objects.get(id=id)
        deleteworksamples.delete()

        resume_id = deleteworksamples.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteAchievements(View):

    def get(self, request, id):
        deleteachievements = Achievements.objects.get(id=id)
        deleteachievements.delete()

        resume_id = deleteachievements.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteCertificate(View):

    def get(self, request, id):
        certificate = Certificate.objects.get(id=id)
        certificate.delete()

        resume_id = certificate.resume.id
        # print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteSkills(View):

    def get(self, request, id):
        skills = Skills.objects.get(id=id)

        skills.delete()
        resume_id = skills.resume.id
        print(skills.resume.id)
        return redirect("/update_data/"+str(resume_id))


class DeleteHobbies(View):

    def get(self, request, id):
        hobbies = Hobbies.objects.get(id=id)
        hobbies.delete()

        resume_id = hobbies.resume.id
        print(hobbies.resume.id)
        return redirect("/update_data/"+str(resume_id))

# ImageUpload for template
class ImageUpload(View):
    def post(self, request, id):
        user_data = ResumeUserDetails.objects.get(resume__id=id)
        photo = request.FILES.get('photo')
        print(photo)
        user_data.photo = photo
        user_data.save()
        return redirect("/update_data/"+str(id))

          



########################################################################################


# Update for template
class UpdateDataView(View):
    def post(self, request, id):
        resume = Resume.objects.get(id=id)
        if request.method == 'POST':
            # import pdb; pdb.set_trace()
            objective = request.POST.get('objective', '')
            title = request.POST.get('title', '')
            resume.objective = objective
            resume.title = title
            resume.save()

            experience = Experience.objects.filter(resume__id=id)
            for count in range(experience.count()):

                experience = Experience.objects.filter(resume__id=id)[count]
                company_name = request.POST.getlist("company_name[]")[count]
                designation = request.POST.getlist("designation[]")[count]
                role = request.POST.getlist("role[]")[count]
                place = request.POST.getlist("place[]")[count]
                company_name = company_name
                experience.company_name = company_name
                experience.designation = designation
                experience.role = role
                experience.place = place
                experience.save()

            worksamples_data = WorkSamples.objects.filter(resume__id=id)
            for count in range(worksamples_data.count()):

                worksamples_data = WorkSamples.objects.filter(resume__id=id)[
                    count]
                project_name = request.POST.getlist("project_name[]")[count]
                project_link = request.POST.getlist("project_link[]")[count]
                technology = request.POST.getlist("technology[]")[count]
                description = request.POST.getlist("description[]")[count]
                responsibilities = request.POST.getlist(
                    "responsibilities[]")[count]
                worksamples_data.project_name = project_name
                worksamples_data.project_link = project_link
                worksamples_data.technology = technology
                worksamples_data.description = description
                worksamples_data.responsibilities = responsibilities
                worksamples_data.save()

            achievements_data = Achievements.objects.filter(resume__id=id)
            for count in range(achievements_data.count()):

                achievements_data = Achievements.objects.filter(resume__id=id)[
                    count]
                achievements = request.POST.getlist("achievements[]")[count]
                achievements_data.achievements = achievements
                achievements_data.save()

            certificate_data = Certificate.objects.filter(resume__id=id)
            for count in range(certificate_data.count()):

                certificate_data = Certificate.objects.filter(resume__id=id)[
                    count]
                certificate = request.POST.getlist("certificate[]")[count]
                certificate_data.certificate = certificate
                certificate_data.save()

            education_data = Education.objects.filter(resume__id=id)

            for count in range(education_data.count()):
                education_data = Education.objects.filter(resume__id=id)[count]
                qualification_name = request.POST.getlist(
                    "qualification_name[]")[count]
                university = request.POST.getlist("university[]")[count]
                year_of_passing = request.POST.getlist(
                    "year_of_passing[]")[count]
                percentage_or_grade = request.POST.getlist(
                    "percentage_or_grade[]")[count]

                education_data.qualification_name = qualification_name
                education_data.university = university
                education_data.year_of_passing = year_of_passing
                education_data.percentage_or_grade = percentage_or_grade
                education_data.save()

            # print(request.POST)
            skills_data = Skills.objects.filter(resume__id=id)
            for count in range(skills_data.count()):
                skills_data = Skills.objects.filter(resume__id=id)[count]
                skills = request.POST.getlist("skills[]")[count]
                skills_data.skills = skills
                skills_data.save()
                

            hobbies_data = Hobbies.objects.filter(resume__id=id)
            for count in range(hobbies_data.count()):

                hobbies_data = Hobbies.objects.filter(resume__id=id)[count]
                hobbies = request.POST.getlist("hobbies[]")[count]
                hobbies_data.hobbies = hobbies
                hobbies_data.save()
               

            user_data = ResumeUserDetails.objects.get(resume__id=id)
            full_name = request.POST.get("full_name")
            address = request.POST.get("address")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            date_of_birth = request.POST.get("date_of_birth")
            # photo=request.POST.get('photo')
            print(full_name)
            user_data.full_name = full_name
            user_data.address = address
            user_data.email = email
            user_data.mobile = mobile
            user_data.date_of_birth = date_of_birth
            # user_data.photo = photo
            user_data.resume = resume
            user_data.save()
            response =HttpResponse("200 ok")
            response.set_cookie('last_work', f'http://127.0.0.1:8000/update_data/{id}') 
            return response
            # return JsonResponse(experience)
    def get(self, request, id):
        resume = Resume.objects.get(id=id)
        if resume.template.name == "template":
            return render(request, 'resume/template.html', {'resume': resume})
        if resume.template.name == "template2":
            return render(request, 'resume/template2.html', {'resume': resume})
        if resume.template.name == "template3":   
            return render(request, 'resume/template3.html', {'resume': resume}) 
        if resume.template.name == "template4":
            return render(request, 'resume/template4.html', {'resume': resume})  
        if resume.template.name == "template5":
            return render(request, 'resume/template5.html', {'resume': resume})      
            


class TemplatePreviews(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews.html', context)




class TemplatePreviews2(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews2.html', context)  



class TemplatePreviews3(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews3.html', context)        



class TemplatePreviews4(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews4.html', context)  
