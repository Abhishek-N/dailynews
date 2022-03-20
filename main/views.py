from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity

from main.models import Main

# Create your views here.


def home(request):

    pass


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
