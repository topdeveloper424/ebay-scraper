from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import requests
from bs4 import BeautifulSoup
import json

headers = {'authority':'www.ebay.com', 'scheme':'https', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
url = "https://www.ebay.com/sch/i.htm"
search_params = "_from=R40&_trksid=m570.l1313&_nkw={}&_sacat=0&LH_TitleDesc=0&_sop=12&_odkw={}"

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def search(request):
    year_of_card = ''
    player_name = ''
    _set = ''
    variation = ''
    card = ''
    grade = ''
    include_list = []
    exclude_list = []
    post_data = request.GET
    
    search_str = ''
    
    if 'yearOfCard' in post_data:
        year_of_card = post_data['yearOfCard']
        if year_of_card.strip() != '':
            search_str += year_of_card.strip() + " "
        
    player_name = post_data['playerName']
    search_str += player_name.strip() + " "

    if 'set' in post_data:
        _set = post_data['set']
        if _set.strip() != '':
            search_str += _set.strip() + " "
        
    if 'variation' in post_data:
        variation = post_data['variation']
        if variation.strip() != '':
            search_str += variation.strip() + " "
        
    if 'card' in post_data:
        card = str(post_data['card'])
        if card.strip() != '':
            search_str += card.strip() + " "
        
    if 'grade' in post_data:
        grade = post_data['grade']
        
    if 'termsInclude' in post_data:
        terms_include = post_data['termsInclude']
        if terms_include.strip() != '':
            include_list = terms_include.split(",")
            print(include_list)
        
    if 'termsExclude' in post_data:
        terms_exclude = post_data['termsExclude']
        if terms_exclude.strip() != '':
            exclude_list = terms_exclude.split(",")
            print(exclude_list)
    
    search_str = search_str.strip()
    
    real_params = search_params.format(search_str, search_str)
    if grade != '':
        real_params += '&Professional Grader=' + grade
    print(real_params)
    source = requests.get(url+"?"+real_params, headers=headers).text
    soup = BeautifulSoup(source ,'lxml')
    container = soup.find('div',{'id':'srp-river-main'})
    ul_tag = container.find('ul',{'class':'srp-results'})
    products = ul_tag.findAll('li',{'class':'s-item'})
    results = []
    for product in products:
        title_tag = product.find('h3',{'class':'s-item__title'})
        title = title_tag.text
        title = title.strip()
        
        flag = False
        for word in include_list:
            if title.find(word) == -1:
                flag = True
        for word in exclude_list:
            if title.find(word) != -1:
                flag = True
        if flag:
            continue
        img = product.find('img',{'class':'s-item__image-img'})
        price_tag = product.find('span', {'class':'s-item__price'})
        item = {}
        item['title'] = title
        if img:
            item['img'] = img['src']
        else:
            item['img'] = ''
        if price_tag:
            item['price'] = price_tag.text
        else:
            item['price'] = ''

        results.append(item)
    
    return HttpResponse(json.dumps(results),content_type="application/json")
    
def save_search(request):
    pass