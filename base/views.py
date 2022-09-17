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
from django.contrib import messages

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
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Logged in successfully.</div>')
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
    profiles = []
    rooms_all = Room.objects.all()
    user_profile = get_object_or_404(Profile,user=request.user)
    rooms = []
    for i in rooms_all:
        if user_profile in i.profiles.all():
            rooms.append(i)

    for i in rooms:
        for profile in i.profiles.all():
            if profile not in profiles:
                profiles.append(profile)

    profiles.remove(user_profile)

    if request.method=="POST":
        form = ChatAddForm(request.POST,files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            obj.profiles.add(get_object_or_404(Profile,user=request.user))
            obj.room_admins.add(get_object_or_404(Profile,user=request.user))
            if request.POST.get('profiles'):
                for i in request.POST.get('profiles'):
                    obj.profiles.add(get_object_or_404(Profile,id=i))
            if request.POST.get('admins'):
                for i in request.POST.get('admins'):
                    obj.room_admins.add(get_object_or_404(Profile,id=i))
            form.save_m2m()
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Added a new chat successfully.</div>')
            return redirect("home")
    context = {
        'form':form,
        'profiles':profiles
    }
    return render(request,"base/add-chat.html",context)


@login_required(login_url='/login/')
def EditChat(request,pk):
    room = get_object_or_404(Room,id=pk)
    rooms_profiles = room.profiles.all()
    rooms_admins = room.room_admins.all()
    form = ChatAddForm(instance=room)
    profiles = []
    rooms_all = Room.objects.all()
    user_profile = get_object_or_404(Profile,user=request.user)
    rooms = []
    for i in rooms_all:
        if user_profile in i.profiles.all():
            rooms.append(i)

    for i in rooms:
        for profile in i.profiles.all():
            if profile not in profiles:
                profiles.append(profile)

    profiles.remove(user_profile)

    if request.method=="POST":
        form = ChatAddForm(data=request.POST,files=request.FILES,instance=room)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if request.POST.get('profiles'):
                for i in request.POST.get('profiles'):
                    obj.profiles.add(get_object_or_404(Profile,id=i))
            
            
            if request.POST.get('admins'):
                for i in request.POST.get('admins'):
                    obj.room_admins.add(get_object_or_404(Profile,id=i))


            obj.profiles.add(get_object_or_404(Profile,user=request.user))
            obj.room_admins.add(get_object_or_404(Profile,user=request.user))
            form.save_m2m()
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Chat successfully updated.</div>')
            return redirect("home")
    context = {
        'form':form,
        'profiles':profiles,
        'rooms_profiles':rooms_profiles,
        'rooms_admins':rooms_admins,
    }
    return render(request,"base/edit-chat.html",context)


@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Başarıyla çıkış yapıldı.</div>')
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
        dizi1=[]
        for i in User.objects.all():
            dizi1.append(i.username.lower())
        if request.POST['username'].lower() in dizi1:
            messages.error(request, 'Girdiğiniz kullanıcı adı kullanımda.')
            return redirect('register')
        
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Registered successfully.</div>')
            Profile.objects.update_or_create(
                user=User.objects.get(username = request.POST['username']),
                bio=None,
                profile_photo=None,
                profile_code=None,
            )
            return redirect('login')
        else:
            messages.error(request, '<div class="message btn btn-danger position-fixed me-3 mb-3 end-0 bottom-0">Couldnt register successfully.</div>')

    context = {
        'form': form,
    }
    return render(request, 'base/register.html', context)