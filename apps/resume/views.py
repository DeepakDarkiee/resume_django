from datetime import date

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from resume_maker import settings

from .models import *
from .utils import get_childs

date = date.strftime
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

User = get_user_model()


# def mail(user, password):
#     subject = "Greetings"
#     msg = f"Congratulations for your successfull ResumeForm username {user} ,password {password}"
#     to = "nisha.thoughtwin@gmail.com"
#     res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#     if (res == 1):
#         msg = "Mail Sent Successfully"
#     else:
#         msg = "Mail could not sent"
#     return HttpResponse(msg)


def logout_request(request):
    logout(request)
    return redirect("/")


def choose(request):
    return render(request, "resume/choose-template.html")


class Home(View):
    def get(self, request):
        theme = ChooseTemplate.objects.all()
        response = HttpResponse("200 ok")
        response.set_cookie("last_work", "")
        last_work = None
        try:
            last_work = request.COOKIES["last_work"]
        except KeyError as ke:
            pass
        return render(request, "index.html", {"theme": theme, "last_work": last_work})


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
        return render(
            request,
            "resume/dashboard.html",
            {
                "resumes": resumes,
            },
        )


# Add template
class AddAnother(View):
    def post(self, request, id):
        resume = Resume.objects.get(id=id)
        element = request.POST.get("element")
        if element == "education":
            education = Education.objects.create()
            education.resume = resume
            education.save()

        if element == "skills":
            skills = Skills.objects.create()
            skills.resume = resume
            skills.save()

        if element == "experience":
            experience = Experience.objects.create()
            experience.resume = resume
            experience.save()

        if element == "worksamples":
            worksamples = WorkSamples.objects.create()
            worksamples.resume = resume
            worksamples.save()

        if element == "achievements":
            achievements = Achievements.objects.create()
            achievements.resume = resume
            achievements.save()

        if element == "certificate":
            certificate = Certificate.objects.create()
            certificate.resume = resume
            certificate.save()

        if element == "hobbies":
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
        return redirect(f"/update_data/{resume.id}")


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
        return JsonResponse({"status": True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteEducation(View):
    def get(self, request, id):
        education = Education.objects.get(id=id)
        resume_id = education.resume.id
        education.delete()
        return JsonResponse({"status": True})
        # return redirect("/update_data/"+str(resume_id))


class DeleteWorkSamples(View):
    def get(self, request, id):
        deleteworksamples = WorkSamples.objects.get(id=id)
        resume_id = deleteworksamples.resume.id
        deleteworksamples.delete()
        return JsonResponse({"status": True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteAchievements(View):
    def get(self, request, id):
        deleteachievements = Achievements.objects.get(id=id)
        resume_id = deleteachievements.resume.id
        deleteachievements.delete()
        return JsonResponse({"status": True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteCertificate(View):
    def get(self, request, id):
        certificate = Certificate.objects.get(id=id)
        resume_id = certificate.resume.id
        certificate.delete()
        return JsonResponse({"status": True})
        # print(hobbies.resume.id)
        # return redirect("/update_data/"+str(resume_id))


class DeleteSkills(View):
    def get(self, request, id):
        skills = Skills.objects.get(id=id)
        resume_id = skills.resume.id
        skills.delete()
        # print(skills.resume.id)
        return JsonResponse({"status": True})
        # return redirect("/update_data/"+str(resume_id))


class DeleteHobbies(View):
    def get(self, request, id):
        hobbies = Hobbies.objects.get(id=id)
        resume_id = hobbies.resume.id
        hobbies.delete()
        return JsonResponse({"status": True})


# ImageUpload for template
class ImageUpload(View):
    def post(self, request, id):
        user_data = ResumeUserDetails.objects.get(resume__id=id)
        photo = request.FILES.get("photo")
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
        if request.method == "POST":
            objective = request.POST.get("objective", "")
            title = request.POST.get("title", "")
            resume.objective = objective
            resume.title = title
            resume.save()

            experience_data_list = resume.experience_set.all()
            company_names = request.POST.getlist("company_name[]")
            res = max(idx for idx, val in enumerate(company_names) if val == "")
            company_names.pop(res)
            designations = request.POST.getlist("designation[]")
            res = max(idx for idx, val in enumerate(designations) if val == "")
            designations.pop(res)
            roles = request.POST.getlist("role[]")
            res = max(idx for idx, val in enumerate(roles) if val == "")
            roles.pop(res)
            places = request.POST.getlist("place[]")
            res = max(idx for idx, val in enumerate(places) if val == "")
            places.pop(res)
            for count, experience in enumerate(experience_data_list):
                experience.company_name = company_names[count]
                experience.designation = designations[count]
                experience.role = roles[count]
                experience.place = places[count]
                experience.save()

            worksamples_data_list = resume.worksamples_set.all()
            project_names = request.POST.getlist("project_name[]")
            res = max(idx for idx, val in enumerate(project_names) if val == "")
            project_names.pop(res)
            project_links = request.POST.getlist("project_link[]")
            res = max(idx for idx, val in enumerate(project_links) if val == "")
            project_links.pop(res)
            technologies = request.POST.getlist("technology[]")
            res = max(idx for idx, val in enumerate(technologies) if val == "")
            technologies.pop(res)
            descriptions = request.POST.getlist("description[]")
            res = max(idx for idx, val in enumerate(descriptions) if val == "")
            descriptions.pop(res)
            responsibilities = request.POST.getlist("responsibilities[]")
            res = max(idx for idx, val in enumerate(responsibilities) if val == "")
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
            res = max(idx for idx, val in enumerate(achievements) if val == "")
            achievements.pop(res)
            for count, achievements_data in enumerate(achievements_data_list):
                achievements_data.achievements = achievements[count]
                achievements_data.save()

            certificate_data_list = resume.certificate_set.all()
            certificate = request.POST.getlist("certificate[]")
            res = max(idx for idx, val in enumerate(certificate) if val == "")
            certificate.pop(res)
            for count, certificate_data in enumerate(certificate_data_list):
                certificate_data.certificate = certificate[count]
                certificate_data.save()

            education_data_list = resume.education_set.all()
            qualification_names = request.POST.getlist("qualification_name[]")
            res = max(idx for idx, val in enumerate(qualification_names) if val == "")
            qualification_names.pop(res)
            universitys = request.POST.getlist("university[]")
            res = max(idx for idx, val in enumerate(universitys) if val == "")
            universitys.pop(res)
            year_of_passings = request.POST.getlist("year_of_passing[]")
            res = max(idx for idx, val in enumerate(year_of_passings) if val == "")
            year_of_passings.pop(res)
            percentage_or_grades = request.POST.getlist("percentage_or_grade[]")
            res = max(idx for idx, val in enumerate(percentage_or_grades) if val == "")
            percentage_or_grades.pop(res)
            for count, education_data in enumerate(education_data_list):
                education_data.qualification_name = qualification_names[count]
                education_data.university = universitys[count]
                education_data.year_of_passing = year_of_passings[count]
                education_data.percentage_or_grade = percentage_or_grades[count]
                education_data.save()

            skills_data_list = resume.skills_set.all()
            skills = request.POST.getlist("skills[]")
            res = max(idx for idx, val in enumerate(skills) if val == "")
            skills.pop(res)
            for count, skills_data in enumerate(skills_data_list):
                skills_data.skills = skills[count]
                skills_data.save()

            hobbies_data_list = resume.hobbies_set.all()
            hobbies = request.POST.getlist("hobbies[]")
            res = max(idx for idx, val in enumerate(hobbies) if val == "")
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
            response.set_cookie("last_work", f"http://127.0.0.1:8000/update_data/{id}")
            return response

    def get(self, request, id, *args, **kwargs):
        """
        Get template selected by user.
        """
        resume = Resume.objects.get(id=id)
        experiences = Experience.objects.filter(resume=resume)
        workSamples = WorkSamples.objects.filter(resume=resume)
        certificates = Certificate.objects.filter(resume=resume)
        achievements = Achievements.objects.filter(resume=resume)
        educations = Education.objects.filter(resume=resume)
        skills = Skills.objects.filter(resume=resume)
        hobbies = Hobbies.objects.filter(resume=resume)

        context = {
            "resume": resume,
            "experiences": experiences,
            "achievements": achievements,
            "worksamples": workSamples,
            "certificates": certificates,
            "educations": educations,
            "skills": skills,
            "hobbies": hobbies,
        }
        if resume.template.name == "template":
            return render(request, "resume/template.html", context)
        if resume.template.name == "template2":
            return render(request, "resume/template2.html", context)
        if resume.template.name == "template3":
            return render(request, "resume/template3.html", context)
        if resume.template.name == "template4":
            return render(request, "resume/template4.html", context)
        if resume.template.name == "template5":
            return render(request, "resume/template5.html", context)
        if resume.template.name == "template6":
            return render(request, "resume/template6.html", context)


class TemplatePreviews(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews.html", context)


class TemplatePreviews2(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews2.html", context)


class TemplatePreviews3(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews3.html", context)


class TemplatePreviews4(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews4.html", context)


class TemplatePreviews5(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews5.html", context)


class TemplatePreviews6(View):
    def get(self, request, id):
        context = {}
        user = request.user
        resume = Resume.objects.filter(id=id).last()
        context["resume"] = resume
        return render(request, "resume/template_previews6.html", context)
