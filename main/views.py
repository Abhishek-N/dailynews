from random import randint
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from cat.models import Cat

from main.models import Main
from news.models import News
from subcat.models import SubCat
from trending.models import Trending

# Create your views here.


def home(request):

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')

    cat = Cat.objects.all()
    subcat = SubCat.objects.all()

    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]

    popnews = News.objects.filter(act=1).order_by('-show')

    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]

    trending = Trending.objects.all().order_by('-pk')[:3]

    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    random_object = Trending.objects.all()[randint(0, len(trending) -1)]

    return render(request, 'front/home.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2})


def login(request):

    if request.method == "POST":

        utxt = request.POST.get("username")
        ptxt = request.POST.get("password")

        if utxt != "" and ptxt != "":

            user = authenticate(username=utxt, password=ptxt)

            if user != None:
                login(request, user)
                return redirect('panel')
        
    return render(request, 'front/login.html')


def register(request):

    if request.method == "POST":

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Input your name"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if password1 != password2:
            msg = "Your Passwords didn't match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        check1 = 0
        check2 = 0
        check3 = 0
        check4 = 0


        for i in password1:
            
            if i > 0 and i < 9:
                check1 = 1

            if i > 'A' and i < 'Z':
                check2 = 1

            if i > 'a' and i < 'z':
                check3 = 1

            if i > '!' and i < '(':
                check4 = 1

        if check1 == 0 or check2 == 0 or check3 == 0 or check4 == 0:
            msg = "Your password is not strong enough"
            return render(request, 'front/msgbox.html', {'msg':msg})

        if len(password1) < 8:
            msg = "Your password must be atleast 8 charecters long"
            return render(request, 'front/msgbox.html', {'msg':msg})

        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:

            ip, is_routable = get_client_ip(request)

            if ip is None:
                ip = "0.0.0.0"

            try: 
                response = DbIpCity.get(ip, api_key='free')
                country = response.country + " | " + response.city

            except:
                country = "Unknown"

            user = User.objects.create_user(username=uname, email=email, password=password1)
            # b = Manager(name=name, utxt=uname, email=email, ip=ip, country=country)
            # b.save()
    return render(request, 'front/login.html')
