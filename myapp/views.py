from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . models import Search
from django.utils import timezone
from bs4 import BeautifulSoup
import requests



def index(request):

    return render(request, 'base.html', )


def new_search(request):
   search = request.POST.get('search')
   stuff_for_frontend = {
       'search': search
   }
   return render(request, 'my_app/index.html', stuff_for_frontend )




