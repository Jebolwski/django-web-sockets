from urllib import response
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
import json
from django.core import serializers
from django.http import HttpResponse

@login_required(login_url='/login/')
def Home(request):
    
    profile = get_object_or_404(Profile,user=request.user)
    rooms_all = Room.objects.all()
    rooms = []
    for i in rooms_all:
        if profile in i.profiles.all():
            rooms.append(i)


    if request.method=="POST":
        print(request.POST.get('search_text'))
        return redirect('add-friend',request.POST.get('search_text'))

    context = {
        'rooms':rooms,
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
            form.save()
            form.save_m2m()
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Added a new chat successfully.</div>')
            return redirect("home")
        else:
            print("non-valid")
    context = {
        'form':form,
        'user_profile':user_profile
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
            if i not in rooms:
                rooms.append(i)
        if user_profile in i.room_admins.all():
            if i not in rooms:
                rooms.append(i)

    for i in room.profiles.all():
        profiles.append(i)
    profiles.remove(user_profile)

    if request.method=="POST":
        form = ChatAddForm(data=request.POST,files=request.FILES,instance=room)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">'+ request.POST.get('room_name') +' successfully updated.</div>')
            return redirect("edit-chat",room.id)
    
    context = {
        'form':form,
        'profiles':profiles,
        'rooms_profiles':rooms_profiles,
        'user_profile':user_profile,
        'room':room
    }
    
    return render(request,"base/edit-chat.html",context)


@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    messages.success(request,'<div class="message btn btn-success position-fixed me-3 mb-3 end-0 bottom-0">Ba??ar??yla ????k???? yap??ld??.</div>')
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
            messages.error(request, 'Girdi??iniz kullan??c?? ad?? kullan??mda.')
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

@login_required(login_url='/login/')
def AddFriend(request,text):
    user_profile = Profile.objects.get(user=request.user)
    search_profiles = Profile.objects.filter(profile_code__icontains=text)
    if request.method=="POST":
        return redirect('add-friend',request.POST.get('search_text'))

    context = {
        'profiles' : search_profiles,
        'user_profile' : user_profile
    }
    return render(request,"base/add-friend.html",context)


def AddRemoveFriend(request,pk):
    user_profile = Profile.objects.get(user=request.user)
    profile = get_object_or_404(Profile,id=pk)
    if profile in user_profile.friends.all():
        user_profile.friends.remove(get_object_or_404(Profile,id=pk))
    else:
        user_profile.friends.add(get_object_or_404(Profile,id=pk))
    print(profile)
    return redirect("add-friend",profile.profile_code)

# @login_required(login_url='/login/')
# def AddFriendFetch(request):
#     text = request.POST.get('text').lower()
#     profiles = []
#     if text!=None:
#         for i in Profile.objects.all():
#             print(i.user.username.lower(),i.profile_code.lower())
#             if text in  i.user.username.lower():
#                 if i not in profiles:
#                     profiles.append(i)
#             if text in  i.profile_code.lower():
#                 if i not in profiles:
#                     profiles.append(i)
#     dizi = []
#     for i in profiles:
#         dizi.append({'username':i.user.username,'id':i.id})
    
#     return HttpResponse(json.dumps(dizi))  