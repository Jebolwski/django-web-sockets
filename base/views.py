from django.shortcuts import render

# Create your views here.
def Lobby(request):
    return render(request,"base/lobby.html")
