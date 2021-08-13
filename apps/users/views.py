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