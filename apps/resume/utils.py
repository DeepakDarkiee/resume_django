import imgkit
from django.http import HttpResponse
from django.views import View

class GenratePdf(View):

    def get(self, request):

        imgkit.from_url('127.0.0.1:8000/resume4/', 'out.jpg')
        return HttpResponse('done')