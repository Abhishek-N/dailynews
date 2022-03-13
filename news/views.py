from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

# Create your views here.


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