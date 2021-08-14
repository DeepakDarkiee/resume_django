import imgkit
from django.http import HttpResponse
from django.views import View


class GenratePdf(View):
    def get(self, request):

        imgkit.from_url("127.0.0.1:8000/resume4/", "out.jpg")
        return HttpResponse("done")


def get_childs(user, users):
    users.append(user)
    childs = user.children.all()
    for child in childs:
        get_childs(child, users)
    return users
