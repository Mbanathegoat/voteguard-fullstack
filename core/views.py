from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import *
from voteguard import settings

"""
For each bug and feature I either solve or create, I'll drop a dad joke.

1. What do you call a cow with no legs???
    Ground Beef(solved user auth bug)

2. Why are educated so hot???
    Cause they have more degress(Fixed mailing list bugs)

3. Why did the programmer need new glasses?
    Becaue he couldn't C# *ba dum tsss (Fixed Looping Issue With Maps API)

4. Why was 6 afraid of 7?
    Because 7, 8, 9(Fixed styling issue with maps)

5. What do you call a cow with no legs?
    Ground BEEF!!!!!!
"""


def index(request):
    return render(request, "index.html")

# Create your views here.
