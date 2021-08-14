from django.urls import path

from .views import *

urlpatterns = [
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_remove/<int:id>", UserRemove.as_view(), name="user_remove"),
    path("team_leader/", TeamLeader.as_view(), name="team_leader"),
    path("login/", sign_in, name="sign_in"),
    path("login/<uuid:id>/", sign_in, name="sign_in"),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_up/<uuid:id>", sign_up, name="sign_up"),
]
