from datetime import date

import pdfkit
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from resume_maker import settings
from .forms import *
from .utils import get_childs

date = date.strftime
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

User = get_user_model()


def mail(user, password):
    subject = "Greetings"
    msg = f"Congratulations for your successfull ResumeForm username {user} ,password {password}"
    to = "nisha.thoughtwin@gmail.com"
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if (res == 1):
        msg = "Mail Sent Successfully"
    else:
        msg = "Mail could not sent"
    return HttpResponse(msg)


class Home(View):
    def get(self, request):
        theme = ChooseTemplate.objects.all()
        response = HttpResponse("200 ok")
        response.set_cookie('last_work', '')
        last_work = None
        try:
            last_work = request.COOKIES['last_work']
        except KeyError as ke:
            pass
        return render(request, 'index.html', {'theme': theme, 'last_work': last_work})


class Dashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.is_superuser:
            resumes = Resume.objects.all()
        else:
            childs = get_childs(user, [])
            resumes = Resume.objects.filter(user__in=childs)
            # resume = team_resume | user_resume
        return render(request, 'resume/dashboard.html', {'resumes': resumes, })


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
                        temp_l.append(l + "1")
                        break
                    else:
                        i.university = l

                i.save()
                e = e + 1

                i.save()
                e = e + 1

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
                                            email=email, mobile=mobile, date_of_birth=date_of_birth, address=address,
                                            photo=photo)
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
                        temp_l.append(l + "1")
                        break
                    else:
                        i.university = l

                i.save()
                e = e + 1

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
                e = e + 1

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
                e = e + 1

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
        context = {'resume': resume, 'eduform': eduform, 'education': education, 'skillsform': skillsform,
                   'skills': skills, 'hobbiesform': hobbiesform,
                   'hobbies': hobbies, 'achievementsform': achievementsform, 'achievements': achievements,
                   'experienceform': experienceform, 'experience': experience,
                   'worksamplesform': worksamplesform, 'worksamples': worksamples, 'certificateform': certificateform,
                   'certificate': certificate,
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
                                   technology=technology, description=description, responsibilities=responsibilities,
                                   date=date)

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
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8,
               'form9': form9, }
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
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8,
               'form9': form9, }

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
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8,
               'form9': form9, }

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
               'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, 'form8': form8,
               'form9': form9, }

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
    def get(self, request, id, *args, **kwargs):
        resume = Resume.objects.create()
        template = ChooseTemplate.objects.get(id=id)
        resume.template = template
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
        return redirect("/update_data/" + str(resume_id))


class DeleteExperience(View):
    def get(self, request, id):
        experience = Experience.objects.get(id=id)
        resume_id = experience.resume.id
        experience.delete()
        return JsonResponse({'status': True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteEducation(View):
    def get(self, request, id):
        education = Education.objects.get(id=id)
        resume_id = education.resume.id
        education.delete()
        return JsonResponse({'status': True})
        # return redirect("/update_data/"+str(resume_id))


class DeleteWorkSamples(View):
    def get(self, request, id):
        deleteworksamples = WorkSamples.objects.get(id=id)
        resume_id = deleteworksamples.resume.id
        deleteworksamples.delete()
        return JsonResponse({'status': True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteAchievements(View):
    def get(self, request, id):
        deleteachievements = Achievements.objects.get(id=id)
        resume_id = deleteachievements.resume.id
        deleteachievements.delete()
        return JsonResponse({'status': True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteCertificate(View):
    def get(self, request, id):
        certificate = Certificate.objects.get(id=id)
        resume_id = certificate.resume.id
        certificate.delete()
        return JsonResponse({'status': True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteSkills(View):
    def get(self, request, id):
        skills = Skills.objects.get(id=id)
        resume_id = skills.resume.id
        skills.delete()
        # print(skills.resume.id)
        return JsonResponse({'status': True})
        # return redirect("/update_data/"+str(resume_id))


class DeleteHobbies(View):
    def get(self, request, id):
        hobbies = Hobbies.objects.get(id=id)
        resume_id = hobbies.resume.id
        hobbies.delete()
        return JsonResponse({'status': True})


# ImageUpload for template
class ImageUpload(View):
    def post(self, request, id):
        user_data = ResumeUserDetails.objects.get(resume__id=id)
        photo = request.FILES.get('photo')
        print(photo)
        user_data.photo = photo
        user_data.save()
        return redirect("/update_data/" + str(id))


class UpdateDataView(View):

    def post(self, request, id, *args, **kwargs):
        """
            Method to update template content.
        """
        resume = Resume.objects.get(id=id)
        if request.method == 'POST':
            objective = request.POST.get('objective', '')
            title = request.POST.get('title', '')
            resume.objective = objective
            resume.title = title
            resume.save()

            experience_data_list = resume.experience_set.all()
            company_names = request.POST.getlist("company_name[]")
            res = max(idx for idx, val in enumerate(company_names) if val == '')
            company_names.pop(res)
            designations = request.POST.getlist("designation[]")
            res = max(idx for idx, val in enumerate(designations) if val == '')
            designations.pop(res)
            roles = request.POST.getlist("role[]")
            res = max(idx for idx, val in enumerate(roles) if val == '')
            roles.pop(res)
            places = request.POST.getlist("place[]")
            res = max(idx for idx, val in enumerate(places) if val == '')
            places.pop(res)
            for count, experience in enumerate(experience_data_list):
                experience.company_name = company_names[count]
                experience.designation = designations[count]
                experience.role = roles[count]
                experience.place = places[count]
                experience.save()

            worksamples_data_list = resume.worksamples_set.all()
            project_names = request.POST.getlist("project_name[]")
            res = max(idx for idx, val in enumerate(project_names) if val == '')
            project_names.pop(res)
            project_links = request.POST.getlist("project_link[]")
            res = max(idx for idx, val in enumerate(project_links) if val == '')
            project_links.pop(res)
            technologies = request.POST.getlist("technology[]")
            res = max(idx for idx, val in enumerate(technologies) if val == '')
            technologies.pop(res)
            descriptions = request.POST.getlist("description[]")
            res = max(idx for idx, val in enumerate(descriptions) if val == '')
            descriptions.pop(res)
            responsibilities = request.POST.getlist("responsibilities[]")
            res = max(idx for idx, val in enumerate(responsibilities) if val == '')
            responsibilities.pop(res)
            for count, worksamples_data in enumerate(worksamples_data_list):
                worksamples_data.project_name = project_names[count]
                worksamples_data.project_link = project_links[count]
                worksamples_data.technology = technologies[count]
                worksamples_data.description = descriptions[count]
                worksamples_data.responsibilities = responsibilities[count]
                worksamples_data.save()

            achievements_data_list = resume.achievements_set.all()
            achievements = request.POST.getlist("achievements[]")
            res = max(idx for idx, val in enumerate(achievements) if val == '')
            achievements.pop(res)
            for count, achievements_data in enumerate(achievements_data_list):
                achievements_data.achievements = achievements[count]
                achievements_data.save()

            certificate_data_list = resume.certificate_set.all()
            certificate = request.POST.getlist("certificate[]")
            res = max(idx for idx, val in enumerate(certificate) if val == '')
            certificate.pop(res)
            for count, certificate_data in enumerate(certificate_data_list):
                certificate_data.certificate = certificate[count]
                certificate_data.save()

            education_data_list = resume.education_set.all()
            qualification_names = request.POST.getlist("qualification_name[]")
            res = max(idx for idx, val in enumerate(qualification_names) if val == '')
            qualification_names.pop(res)
            universitys = request.POST.getlist("university[]")
            res = max(idx for idx, val in enumerate(universitys) if val == '')
            universitys.pop(res)
            year_of_passings = request.POST.getlist("year_of_passing[]")
            res = max(idx for idx, val in enumerate(year_of_passings) if val == '')
            year_of_passings.pop(res)
            percentage_or_grades = request.POST.getlist("percentage_or_grade[]")
            res = max(idx for idx, val in enumerate(percentage_or_grades) if val == '')
            percentage_or_grades.pop(res)
            for count, education_data in enumerate(education_data_list):
                education_data.qualification_name = qualification_names[count]
                education_data.university = universitys[count]
                education_data.year_of_passing = year_of_passings[count]
                education_data.percentage_or_grade = percentage_or_grades[count]
                education_data.save()

            skills_data_list = resume.skills_set.all()
            skills = request.POST.getlist("skills[]")
            res = max(idx for idx, val in enumerate(skills) if val == '')
            skills.pop(res)
            for count, skills_data in enumerate(skills_data_list):
                skills_data.skills = skills[count]
                skills_data.save()

            hobbies_data_list = resume.hobbies_set.all()
            hobbies = request.POST.getlist("hobbies[]")
            res = max(idx for idx, val in enumerate(hobbies) if val == '')
            hobbies.pop(res)
            for count, hobbies_data in enumerate(hobbies_data_list):
                hobbies_data.hobbies = hobbies[count]
                hobbies_data.save()

            user_data = ResumeUserDetails.objects.get(resume__id=id)
            user_data.full_name = request.POST.get("full_name")
            user_data.address = request.POST.get("address")
            user_data.email = request.POST.get("email")
            user_data.mobile = request.POST.get("mobile")
            user_data.date_of_birth = request.POST.get("date_of_birth")
            user_data.resume = resume
            user_data.save()
            response = HttpResponse("200 ok")
            response.set_cookie('last_work', f'http://127.0.0.1:8000/update_data/{id}')
            return response

    def get(self, request, id, *args, **kwargs):
        """
            Get template selected by user.
        """
        resume = Resume.objects.get(id=id)

        if resume.template.name == "template":
            return render(request, 'resume/template6.html', {'resume': resume})
        if resume.template.name == "template2":
            return render(request, 'resume/template2.html', {'resume': resume})
        if resume.template.name == "template3":
            return render(request, 'resume/template3.html', {'resume': resume})
        if resume.template.name == "template4":
            return render(request, 'resume/template4.html', {'resume': resume})
        if resume.template.name == "template5":
            return render(request, 'resume/template5.html', {'resume': resume})
        if resume.template.name == "template6":
            return render(request, 'resume/template.html', {'resume': resume})


class TemplatePreviews6(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews6.html', context)


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


class TemplatePreviews5(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews5.html', context)


class TemplatePreviews(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context['resume'] = resume
        return render(request, 'resume/template_previews.html', context)
