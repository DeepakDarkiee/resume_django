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
    user = User.objects.filter(parent=request.user)  
    context["user"] = user
    users=User.objects.filter(parent=None)
    context["users"] = users
    return render(request,"team_list.html",context)

  def post(self, request):
    user=User.objects.get(username=request.user)
    team_member=User.objects.get(id=request.POST.get('team'))
    team_member.parent=user
    team_member.save()
    return redirect('/users/user_list')
    
class UserRemove(View):
  def get(self, request,id):
    team_member=User.objects.get(id=id)
    team_member.parent=None
    team_member.save()
    return redirect('/users/user_list')

class TeamLeader(View):
  def post(self, request):
    user=User.objects.get(id=request.POST.get('team'))
    user.is_teamleader=True
    user.save()
    return redirect('/users/user_list')