
from django.urls import path
from .views import *
urlpatterns = [
  
path('user_list/',UserListView.as_view(),name="user_list"),
path('user_remove/<int:id>',UserRemove.as_view(),name="user_remove"),
path('team_leader/',TeamLeader.as_view(),name="team_leader"),

]