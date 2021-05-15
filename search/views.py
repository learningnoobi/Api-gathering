from django.shortcuts import render, redirect
from django.conf import settings
import requests
from isodate import parse_duration

from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    bing = []
    url = "https://bing-news-search1.p.rapidapi.com/news"

    querystring = {"safeSearch":"Off","textFormat":"Raw"}

    headers = {
        'x-bingapis-sdk': "true",
        'x-rapidapi-key': "c84814a9d4msh0adba8fb76f6854p13b21ejsnef8f35136c16",
        'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    results=response.json()['value']


    for result in results:
        
        news_data = {
           
            'news': result['name'],
            'url': result['url'],
            'description': result['description'],
            

            
 
        }
        bing.append(news_data)
    
    context = {

        'bing':bing
     }

    return render (request,'search/index.html',context)


def youtube(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    
    return render(request, 'search/home.html', context)



def corona(request):
    data = []
    url = "https://covid-193.p.rapidapi.com/statistics"
    search = request.POST.get('search')
    

    if request.method =='POST':
        querystring = {"country":search}
    else:
        querystring = {"country":"usa"}
    print(search)
    headers = {
    
        'x-rapidapi-key': "c84814a9d4msh0adba8fb76f6854p13b21ejsnef8f35136c16",
        'x-rapidapi-host': "covid-193.p.rapidapi.com",

        }
    try:

          
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        d = response['response']
        s = d[0]
        print(response)
    except:
        messages.success(request, 'country name not found !')
        return redirect("corona")
    context = {
        'country':s['country'],
        'population':s['population'],
        'all': s['cases']['total'],
        'recovered': s['cases']['recovered'],
        'deaths': s['deaths']['total'],
        'new': s['cases']['new'],
        'serioz': s['cases']['critical'],
        'active': s['cases']['active'],
        'tests': s['tests']['total'],

    }
    
   

    return render(request, 'search/corona.html', context)

