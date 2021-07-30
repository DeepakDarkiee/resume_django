from django.core.management.base import BaseCommand
import pdfkit

class Command(BaseCommand):

    def handle(self,*args, **kwargs):

        pdfkit.from_url('/home/chandu/Desktop/pythoncode/resumemaker_project/resume_maker/templates/resume/resume_template.html','shaurya.pdf')  