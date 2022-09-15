from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from base.forms import RegisterForm
from base.models import Profile

@login_required(login_url='/login/')
def Home(request):
    return render(request,"base/index.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect("lobby")


    if request.method=="POST":
        username1 = request.POST.get('username')
        if len(User.objects.filter(username=username1))>0:
            username1 = request.POST.get('username')
        else:
            if len(User.objects.all().filter(email=username1)) > 0:
                username1 = User.objects.get(email=username1).username
        password = request.POST.get('password')
        

        person = authenticate(
            request,username=username1, password=password)

        if person is not None:
            login(request, person)
            messages.success(request, 'Başarıyla giriş yapıldı.')
            return redirect("home")

    return render(request,"base/login.html")


@login_required(login_url='/login/')
def Lobby(request,room_name):
    return render(request,"base/lobby.html")


@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect("home")


def Register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm()
    if request.method == 'POST': 
        dizi=[]
        for i in User.objects.all():
            dizi.append(i.email)
        if request.POST['email'] in dizi:
            messages.error(request, 'Girdiğiniz email kullanımda.')
            return redirect('register')

    if request.method == 'POST': 
        dizi1=[]
        for i in User.objects.all():
            dizi1.append(i.username.lower())
        if request.POST['username'].lower() in dizi1:
            messages.error(request, 'Girdiğiniz kullanıcı adı kullanımda.')
            return redirect('register')
        
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Başarıyla kayıt olundu.')
            Profile.objects.update_or_create(
                user=User.objects.get(username = request.POST['username']),
                bio=None,
                profile_photo=None,
                profile_code=None,
            )
            return redirect('login')
        else:
            messages.error(request, "Kayıt başarı ile gerçekleştirilemedi.")

    context = {
        'form': form,
    }
    return render(request, 'base/register.html', context)