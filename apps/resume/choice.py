from django.shortcuts import render
from .models import *

COMPETENCY_CHOICES = (
    ('', '-----'),
    (1, 'Below Average'),
    (2, 'Average'),
    (3, 'Good'),
    (4,'Very Good'),
    (5, 'Excellent'), )
RESUME_CHOICES = (
    ('template1', 'Template1'),
    ('template2', 'Template2'),
    ('template3', 'Template3'),
    ('template4', 'Template4'), )



