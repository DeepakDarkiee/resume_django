from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("dashboard", Dashboard.as_view(), name="dashboard"),
    path("logout", logout_request, name="logout"),
    path("update_data/<uuid:id>", UpdateDataView.as_view(), name="update_data"),
    path("add_another/<uuid:id>", AddAnother.as_view(), name="add_another"),
    #     path('delete_block/<int:id>', DeleteBlock.as_view(), name='delete_block'),
    #     path('create_data_template/', CreateTemplateData.as_view(), name='create_data_template'),
    path("create_resume/<int:id>", CreateResumeView.as_view(), name="create_resume"),
    path("image_upload/<uuid:id>", ImageUpload.as_view(), name="image_upload"),
    path(
        "deleteeducation/<uuid:id>/",
        views.DeleteEducation.as_view(),
        name="deleteeducation",
    ),
    path(
        "deleteexperience/<uuid:id>/",
        views.DeleteExperience.as_view(),
        name="deleteexperience",
    ),
    path(
        "deleteworksamples/<uuid:id>/",
        views.DeleteWorkSamples.as_view(),
        name="deleteworksamples",
    ),
    path(
        "deleteachievements/<uuid:id>/",
        views.DeleteAchievements.as_view(),
        name="deleteachievements",
    ),
    path(
        "deletecertificate/<uuid:id>/",
        views.DeleteCertificate.as_view(),
        name="deletecertificate",
    ),
    path("deleteskill/<uuid:id>/", views.DeleteSkills.as_view(), name="deleteskill"),
    path("deletehobbie/<uuid:id>/", views.DeleteHobbies.as_view(), name="deletehobbie"),
    #######################################################################################
    path(
        "template_preview/<uuid:id>",
        TemplatePreviews.as_view(),
        name="template_preview",
    ),
    path(
        "template_preview2/<uuid:id>",
        TemplatePreviews2.as_view(),
        name="template_preview2",
    ),
    path(
        "template_preview3/<uuid:id>",
        TemplatePreviews3.as_view(),
        name="template_preview3",
    ),
    path(
        "template_preview4/<uuid:id>",
        TemplatePreviews4.as_view(),
        name="template_preview4",
    ),
    path(
        "template_preview5/<uuid:id>",
        TemplatePreviews5.as_view(),
        name="template_preview5",
    ),
    path(
        "template_preview6/<uuid:id>",
        TemplatePreviews6.as_view(),
        name="template_preview6",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
