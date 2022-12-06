from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render


from .forms import RoomForm, UserForm, MyUserCreationForm
from .models import Room, Topic,Message, User


def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    room=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) 

    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))
    room_count= room.count
    topics = Topic.objects.all() [0:4]
    context=  {'room':room,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)


def rooms(request,pk):
    rooms = Room.objects.get(id=pk)
    room_messages= rooms.message_set.all()
    participants= rooms.participants.all()

    if request.method == 'POST':
        message= Message.objects.create(
         user= request.user,
         room= rooms,
         body= request.POST.get('body')   
        )
        rooms.participants.add(request.user)
        return redirect('rooms',pk=rooms.id)

    context = {'rooms': rooms,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


@login_required(login_url='login')
def createRoom(request):
    form= RoomForm()
    topics= Topic.objects.all
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic,created= Topic.objects.get_or_create(name= topic_name)

        Room.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('home')
    context= {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room= Room.objects.get(id=pk)
    topics= Topic.objects.all
    form= RoomForm(instance=room)
    if request.method== 'POST':
        topic_name= request.POST.get('topic')
        topic,created= Topic.objects.get_or_create(name= topic_name)
        
        room.name= request.POST.get('name')
        room.topic= topic
        room.description= request.POST.get('description')
        room.save()
        return redirect('home')

    if request.user != room.host:
        return HttpResponse("You are not the host of this room!")
            

    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
   
    return render(request,'base/delete.html',{'obj':room})


def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method== 'POST':
        email= request.POST.get('email').lower()
        password= request.POST.get('password')

        try:
            user= User.objects.get(email=email)
        except:
            messages.error(request,'User does not exist')
        
        user= authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username Or Password does not exist') 
    context={'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form= MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error ocurred during registration')
    
    return render(request,'base/login_register.html',{'form':form})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect('home')

    if request.user != message.user:
        return HttpResponse("You are not the host of this room!")
    return render(request,'base/delete.html',{'obj':message})


def userProfile(request,pk):
    user= User.objects.get(id=pk)
    room=user.room_set.all()
    room_count= room.count 
    topics= Topic.objects.all()
    room_messages= user.message_set.all()
    context={'user':user,'room':room,'room_count':room_count,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)



@login_required(login_url='login')
def updateUser(request):
    user= request.user
    form=UserForm(instance=user)
    if request.method == 'POST':
        form =UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile' ,pk=user.id)
    return render(request, 'base/edit-user.html',{'form':form})


def topicPage(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    topics= Topic.objects.filter(name__icontains=q)
    topic_count= topics.count
    context= {'topics':topics,'topic_count':topic_count}
    return render(request, 'base/topics.html',context)
