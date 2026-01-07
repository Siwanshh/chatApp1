from django.shortcuts import render,redirect
from .models import Room,Topic
from django.db.models import Count 
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
# Create your views here.
from django.http import HttpResponse
from .models import Message,Profile
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import MessageForm,CustomUserCreationForm
userss=[
    {'id':1,'name':'Hari'},
    {'id':2,'name':'Ram'},
    {'id':3,'name':'Shyam'},
    {'id':4,'name':'Krishna'},
    {'id':5,'name':'Ganesh'},
    {'id':6,'name':'Brahma'},
]





def home(request):
    
    #return HttpResponse('Hello, Welcome to the Homepage!')
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topic=Topic.objects.annotate(num_rooms=Count('room_set')).order_by('-num_rooms')
    
    userss=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    totalroom=userss.count()
    print(q)
    
    msg=Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')
    for mg in msg:
        print(mg.room)
    print(msg)
    
  
    context={'room':userss,'topic':topic,'countroom':totalroom,'msgs':msg}
    return render(request,'base/home.html',context)
@login_required(login_url='login')
def start(request,sttr):
    user=None
    userss=Room.objects.get(id=sttr)
    msg=userss.message_set.all().order_by('-created')
    # form=MessageForm(instance=userss)
    # form.fields['user'].disabled=True
    # form.fields['room'].disabled=True
    
    for mg in msg:
     userss.participants.add(request.user)
    ptns=userss.participants.all() 
    context={'room':userss,'msg':msg,'ptns':ptns}
    if request.method=="POST":
        # form=MessageForm(request.POST)
        # print(request.POST)
       
        bdy=request.POST.get('body')
        if bdy!=None:

            addmsg=Message.objects.create(body=bdy,
                                          room=userss,user=request.user)
        return redirect('start',sttr=userss.id)    
    # if request.GET.get('q')!=None:
    #        q= request.GET.get('q')
    #        delm=Message.objects.get(id=q)
    #        delm.delete()
    #        return redirect('start',sttr=userss.id)
        # for mg in msg:
        #     if mg.user == q:
        #         print(mg)
        #         mg.delete()
        #     else:
        #         print("user not found")
        #         print(q) 
        #         print(mg.user)   
    #return HttpResponse(' Welcome dear user,This is the start section')
    return render(request,'base/start.html',context)
@login_required(login_url='home')
def formrqst(request):
    form=RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid:
           room=form.save(commit=False)
           room.host=request.user
           room.save()
           return redirect('home')
    #room=Room.objects.all()
    #context={'room':room}
    context={'form':form}
    return render(request,'base/roomformact.html',context)
def submit(request):
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            # user=request.POST.get('user')
            # name=request.POST.get('name')
            # desc=request.POST.get('description')
            # topic=request.POST.get('topic')
            # Room.objects.create(host=user,topic=topic,name=user,description=desc)
            form.save()
            return HttpResponse("FORM SUBMITTED SUCCESSFULLY")
        else :
             return HttpResponse(form.errors)
@login_required(login_url='home')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('You are not allowed here')
    form=RoomForm(instance=room)
    form.fields['host'].disabled=True
    if request.method=="POST":
        if request.POST.get('btn')=='CONFIRM':
            form=RoomForm(request.POST,instance=room)
            form.fields['host'].disabled=True
            if form.is_valid():
                form.save()
       
                return redirect('home')
        else:
            return redirect(f'{request.META['HTTP_REFERER']}')     
    context={'form':form}
    return render(request,'base/roomformact.html',context)    
@login_required(login_url='home')    
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=="POST":
        if request.POST.get('btn')=="Confirm":
         room.delete()
         return redirect('home')
        else:
            return redirect('home')
    return render(request,'base/delete.html',{'obj':room})
def loginPage(request):
      page='login'
      context={'page':page} 
      if request.user.is_authenticated:
          return redirect('home')
      if request.method=="POST":
          username=request.POST.get('name')
          password=request.POST.get('password')
          try:
            usfound=User.objects.get(username=username)
          except:
              messages.error(request,'user not found')
              return render(request,'base/userlogin.html')
          user=authenticate(request,username=username,password=password)
          if user!=None:
              login(request,user)
              next_url=request.GET.get('next')
              if next_url:
                  return redirect(next_url)
              return redirect('home')    
          else:
             messages.error(request,"Username or Password doesn't match")
            


      return render(request,'base/userlogin.html')
def logoutsection(request):
    logout(request)
    return redirect('home')
def regPage(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form}

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # This automatically triggers the post_save signal
            user = form.save()

            # Update avatar if provided
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()

            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, "Couldn't Register, Please Try Again")

    return render(request, 'base/userlogin.html', context)


@login_required(login_url="login")
def commentAdd(request):
    form=MessageForm()
    print(form.fields)
    if request.method=="POST":
        form=MessageForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
    context={'form':form}        
    return render(request,'base/start.html',context)

def deleteMessage(request,pk):
    msg=Message.objects.get(id=pk)
    if msg!=None:
        msg.delete()
        return redirect(request.META['HTTP_REFERER'])   


def userProfile(request,pk):
    
    user=User.objects.get(id=pk)
    usroom=user.room_set.all()
    msgs=Message.objects.all().order_by('-created')
    tpc=Topic.objects.annotate(num_rooms=Count('room_set')).order_by('-num_rooms')
   
    room=Room.objects.all()
   
    context={'user':user,'room':usroom,'msgs':msgs,'topic':tpc}
    return render(request,'base/userprofile.html',context)      