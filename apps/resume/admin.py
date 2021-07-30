from django.contrib import admin

from apps.resume.models import *

from django.contrib.auth.admin import UserAdmin




class UserAdmin(admin.ModelAdmin):
    list_display = ['username','account_approved']



class EducationAdmin(admin.ModelAdmin):
   
    search_fields = ['qualification_name', ]
    list_filter = ['percentage_or_grade', ]
    list_display = ['resume','qualification_name', 'percentage_or_grade', 'university', ]


class ExperienceAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'designation', ]
    list_filter = ['designation', ]
    list_display = ['resume','company_name', 'start_date','end_date', 'designation','role','place' ]


class WorkSamplesAdmin(admin.ModelAdmin):
    search_fields = ['project_name', ]
    list_display = ['project_name', 'project_link', ]

class HobbiesAdmin(admin.ModelAdmin):
    search_fields = ['resume', ]
    list_display = ['resume', 'hobbies', ]


class SkillAdmin(admin.ModelAdmin):
    search_fields = ['resume', ]
    list_display = ['resume', 'skills', ]


class CertificateAdmin(admin.ModelAdmin):
    search_fields = ['resume', ]
    list_display = ['resume', 'certificate', ]



class AchievementsAdmin(admin.ModelAdmin):
    search_fields = ['resume', ]
    list_display = ['resume', 'achievements', ]

class LanguageAdmin(admin.ModelAdmin):
    search_fields = ['resume', ]
    list_display = ['resume', 'language_name', 'competency']



admin.site.register(Resume)
admin.site.register(ResumeUserDetails)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(WorkSamples, WorkSamplesAdmin)
admin.site.register(Hobbies, HobbiesAdmin)
admin.site.register(Skills, SkillAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Achievements, AchievementsAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(ChooseTemplate)
admin.site.register(User, UserAdmin)




