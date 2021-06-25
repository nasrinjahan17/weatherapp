import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9295a7ce8caae310c2c6c86f0279aeb1"

    errmsg = ''
    emsg  = ''
    msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    errmsg = "Sorry! Can't find the city"
            else:
                errmsg = "The city is already exists"
        if errmsg:
            emsg = errmsg
           
        else:
            msg = "The city is successfully added in database"
            
    form = CityForm()

    weather = []
    city = City.objects.all()
    for p in city:
        r = requests.get(url.format(p)).json()
        print(r)
        city_weather = {
            'city': p,
            'temparature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        
        }
        weather.append(city_weather)
        print(weather)

    context = {
        'weather': weather, 'form': form, 'msg': msg, 'emsg': emsg,}
    return render(request, 'weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('wether:home')


'''def delete_city(request, city_name):
    city = get_object_or_404(City, name=city_name)
    city.delete()
    return redirect('wether:city_weather')'''
    
    
''' <div class="notification">
                          
</div>'''