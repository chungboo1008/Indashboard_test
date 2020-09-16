from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from mainsite.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from mainsite import models
import simplejson as json
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@login_required(login_url='/login')
def simple_upload(request):
    if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            logging.info("login")
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                user_plans = models.User_Plan.objects.filter(user_id_id=db_user.id)
                for user_plan in user_plans:
                    user_plan = user_plan
                plan_id_id = user_plan.plan_id_id
                plan = models.Plan.objects.get(id = plan_id_id)
                plan_name = plan.plan_name
                plan_id = plan.id # plan_id = 1
            
            except Exception as err:
                logging.error("The Error Message is {}".format(err))

    return render(request, 'upload.html',locals())

@login_required(login_url='/login')
def xml_upload(request):
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email

            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                user_plans = models.User_Plan.objects.filter(user_id_id=db_user.id)
                for user_plan in user_plans:
                    user_plan = user_plan
                plan_id_id = user_plan.plan_id_id
                plan = models.Plan.objects.get(id = plan_id_id)
                plan_name = plan.plan_name
                plan_id = plan.id # plan_id = 1
            
            except Exception as err:
                logging.INFO("The Error Message is {}".format(err))
            
   
        return render(request, 'xml_upload.html',locals())

@login_required(login_url='/login')
def num_simulation(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'num_simulation.html',locals())

@login_required(login_url='/login')
def exe(request):
    if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email

            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                user_plans = models.User_Plan.objects.filter(user_id_id=db_user.id)
                for user_plan in user_plans:
                    user_plan = user_plan
                plan_id_id = user_plan.plan_id_id
                plan = models.Plan.objects.get(id = plan_id_id)
                plan_name = plan.plan_name
                plan_id = plan.id # plan_id = 1
            
            except Exception as err:
                logging.INFO("The Error Message is {}".format(err))
            
    return render(request,'exe.html',locals())

@login_required(login_url='/login')
def alias(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'alias.html',locals())

@login_required(login_url='/login')
def deep_learning(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'deep_learning.html',locals())

@login_required(login_url='/login')
def opc(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'opc.html',locals())

@login_required(login_url='/login')
def preview(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'preview.html',locals())

@login_required(login_url='/login')
def usecase(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'use_case.html',locals())

@login_required(login_url='/login')
def batch(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_authenticated:  # if user pass verificated
            username = request.user.username  # get auth_user  username
            useremail = request.user.email
            messages.get_messages(request)
            try:
                db_user = User.objects.get(username=username)  # if username=admin then get admin row
                profile = Profile.objects.get(user_id=db_user.id)
                user_id = profile.user_id
                plan_id = profile.plan_id
            except:
                pass
    return render(request,'batch.html',locals())

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def logout(request):
    # request.session['username']=None
    # return redirect('/')
    auth.logout(request)
    messages.add_message(request,messages.INFO,"成功登出")
    return redirect('/')

def register(request):
    """Register a new user."""
    if request.method != 'POST':  
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            auth.login(request, authenticated_user)
            return HttpResponseRedirect('/login/') # go back to login

    context = {'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='/login/')
def analyse(request):
    if request.user.is_authenticated: # if user pass verificated
        username=request.user.username # get auth_user  username
        useremail=request.user.email
        messages.get_messages(request)
        try:
            db_user = User.objects.get(username=username)  # if username=admin then get admin row
            profile=Profile.objects.get(user_id=db_user.id)
            user_id=profile.user_id
            plan_id=profile.plan_id
        except:
            pass

    return render(request,'analysis_ajax.html',locals())

@login_required
def userinfo(request):
    if request.user.is_authenticated:
        username=request.user.username
        try:
            userinfo=User.objects.get(username=username)
        except:
            pass
    return render(request,'userinfo.html',locals())

@login_required
def elearning(request):
    if request.user.is_authenticated:
        username=request.user.username
        try:
            userinfo=User.objects.get(username=username)
        except:
            pass
    return render(request,'e-learning.html',locals())


@login_required(login_url='/login/')
def chart(request):
    if request.user.is_authenticated: # if user pass verificated
        username=request.user.username # get auth_user  username
        useremail=request.user.email
        messages.get_messages(request)
        try:
            db_user = User.objects.get(username=username)  # if username=admin then get admin row
            profile=Profile.objects.get(user_id=db_user.id)
            user_id=profile.user_id
            plan_id=profile.plan_id
        except:
            pass
    if request.user.is_authenticated:
        username=request.user.username
    else:
        return redirect('/login/')
    return render(request,'chart.html',locals())


def login(request):
    if request.method == 'POST':   #如果是 <login.html> 按登入鈕傳送
        name = request.POST['username']   #取得表單傳送的帳號、密碼
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password) #使用者驗證

        if user is not None:         #若驗證成功，以 auth.login(request,user) 登入
            if user.is_active:
                auth.login(request,user)
                return redirect('/index/')  #登入成功產生一個 Session，重導到<index.html>
                message = '登入成功!'
            else:
                message = '帳號尚未啟用!'
        else:
            message = '登入失敗!'
    return render(request,"login.html",locals())  #登入失敗則重導回<login.html>


@login_required(login_url='/login')
def index(request,pid=None,del_pass=None):
    if request.user.is_authenticated: # if user pass verificated
        username = request.user.username # get auth_user  username
        useremail =request.user.email
        first_name=request.user.first_name
        last_name=request.user.last_name
        name = last_name + first_name
        messages.get_messages(request)
        try:
            # user = User.objects.get(username=username)  # if username=admin then get admin row
            # profile = Profile.objects.get(user_id=user.id)
            # user_id = profile.user_id
            # plan_id = profile.plan_id

            user = User.objects.get(username=username)  # if username = admin then get admin row
            profile = Profile.objects.get(user_id=user.id)
            user_id = profile.user_id
            plan_id = profile.plan_id
            user_plans = models.User_Plan.objects.filter(user_id_id=user.id)
            for user_plan in user_plans:
                user_plan = user_plan
            plan_id_id = user_plan.plan_id_id
            plan = models.Plan.objects.get(id = plan_id_id)
            plan_name = plan.plan_name
            
        except Exception as err:
            logging.info("Error message is {}".format(err))
    return render(request,'index.html',locals())
