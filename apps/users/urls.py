
from django.urls import path
from .views import *
urlpatterns = [
  
path('user_list/',UserListView.as_view(),name="user_list"),

]