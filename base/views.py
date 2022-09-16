from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from base.forms import ChatAddForm, RegisterForm
from base.models import Message, Profile, Room
from django.http import HttpResponse

@login_required(login_url='/login/')
def Home(request):
    profile = get_object_or_404(Profile,user=request.user)
    rooms_all = Room.objects.all()
    rooms = []
    for i in rooms_all:
        if profile in i.profiles.all():
            rooms.append(i)
    context = {
        'rooms':rooms
    }
    return render(request,"base/index.html",context)


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
def Lobby(request,room_id):
    room = get_object_or_404(Room,id=room_id)
    if not room.RoomSecurity(request):
        return render(request,"base/404.html")
    room_messages = Message.objects.filter(room=room)
    context={
        'room':room,
        'room_messages':room_messages
    }
    return render(request,"base/lobby.html",context)

@login_required(login_url='/login/')
def AddChat(request):
    form = ChatAddForm()
    if request.method=="POST":
        form = ChatAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print("non valid")
    context = {
        'form':form
    }
    return render(request,"base/add-chat.html",context)

@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url='/login/')
def SendMessage(request):
    room_id = request.POST.get('room_id')
    text = request.POST.get('text')

    Message.objects.create(
        profile = get_object_or_404(Profile,user=request.user),
        room = get_object_or_404(Room,id=room_id),
        text = text,
    )

    return HttpResponse("messi")


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