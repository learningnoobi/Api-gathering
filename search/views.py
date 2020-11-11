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
    
    # print(results[0])
    for result in results:
        news_data = {
        'img': result['image']['thumbnail']['contentUrl'],
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



# def weather(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

#     err_msg = ''
#     message = ''
#     message_class = ''

#     if request.method == 'POST':
#         form = CityForm(request.POST)

#         if form.is_valid():
#             new_city = form.cleaned_data['name']
#             existing_city_count = City.objects.filter(name=new_city).count()
            
#             if existing_city_count == 0:
#                 r = requests.get(url.format(new_city)).json()

#                 if r['cod'] == 200:
#                     form.save()
#                 else:
#                     err_msg = 'Enter Correct Name of the City'
#             else:
#                 err_msg = 'City already exists!'

#         if err_msg:
#             message = err_msg
#             message_class = 'danger'
#         else:
#             message = 'City added successfully!'
#             message_class = 'success'

#     form = CityForm()

#     cities = City.objects.all().order_by("-created")
#     weather_data = []

#     for city in cities:

#         r = requests.get(url.format(city)).json()

#         city_weather = {
#             'city' : city.name,
#             'temperature' : r['main']['temp'],
#             'description' : r['weather'][0]['description'],
#             'icon' : r['weather'][0]['icon'],
#         }

#         weather_data.append(city_weather)

#     context = {
#         'weather_data' : weather_data, 
#         'form' : form,
#         'message' : message,
#         'message_class' : message_class
#     }

#     return render(request, 'search/weather.html', context)

# def delete_city(request, city_name):
#     City.objects.get(name=city_name).delete() 
#     return redirect('weather')



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

