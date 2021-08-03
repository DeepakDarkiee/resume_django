from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
from .models import User

class UserListView(View):
  def get(self, request):
    context={}
    # user=User.objects.get(id=request.user.id)
    user = User.objects.get(pk=request.user.pk)  
    for child in user.children.all():
        print(child.username)
    context["user"]=user
    users = User.objects.all()
    context["users"]=users
    
    return render(request,"team_list.html",context)
  
  def post(self, request):
    team_member=User.objects.get(id=request.POST.get('team'))
    user=User.objects.get(id=request.user.id)
    print(user)
    user.team_member.id=team_member
    user.save()
    return redirect('/users/user_list')
    
    

  