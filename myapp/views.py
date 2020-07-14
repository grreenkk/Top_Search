from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.utils import timezone
from bs4 import BeautifulSoup
# This strings phrases in the url with +, So that it makes sense for the url
from urllib.parse import quote_plus
import requests

BASE_TOP_SEARCH_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL= 'https://images.craigslist.org/{}_300x300.jpg'


def index(request):
    return render(request, 'base.html', )


def new_search(request):
    search = request.POST.get('search')
    created_objects = models.Search.objects.create(text=search)
    # This strings searches inputted phrases in the url with an +, So that it makes sense for the url
    print(quote_plus(search))
    # This links the input in search bar to whatever base url we use
    final_url = BASE_TOP_SEARCH_URL.format(quote_plus(search))
    # print(final_url)
    # Getting the webpage, creating a Response object
    response = requests.get(final_url)
    # Extracting thhe source code of the page
    data = response.text
    #  Passing the source code to beautiful soup to create a beautiful soup object
    soup = BeautifulSoup(data, features='html.parser')
    # This is used to target the info the html collected by beautiful soup, so the one bellow prints out all the a tags with and it class of result-title
    post_listings = soup.find_all('li', {'class':'result-row'})


    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price ='N/A'

        #this gets the image ids
        if post.find(class_='result-image').get('data-ids'):
            #This splits the image ids into a list
            image_urls= post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image = 'https://images.craigslist.org/{}_300x300.jpg'.format(image_urls)
        else:
            post_image = 'https://craigslist.org/images/peace.jpg'


        print(image_urls)
        print(post_image)

        final_postings.append((post_title, post_url, post_price, post_image))



    # print(data)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/index.html', stuff_for_frontend)
