from django.shortcuts import render,redirect

from django.views.generic import View

from my_app.forms import UserRegistrationForm, LoginForm, TaskForm, ForgotForm, OtperifyForm, ResetpasswordForm

from my_app.models import User, TaskModel, OtpModel

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

import random

from django.utils.decorators import method_decorator


def is_user(fn):  # def get(request, **kwargs)
    def wrapper(request,**kwargs):
        id = kwargs.get("pk")  #{"pk": 2}

        item = TaskModel.objects.get(id = id) #taskmodel obj1

        if item.user_id == request.user:
            return fn(request,**kwargs)
        
        return redirect("login")
    
    return wrapper


class UserRegistrationView(View):

    def get(self,request):

        form = UserRegistrationForm

        return render(request,"signup.html",{"form":form})
    
    def post(self,request):

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            email = form.cleaned_data.get('email')

            User.objects.create_user(username = username, password = password, email = email)  # create_user to make the password encrypted

        # return render(request,"signup.html", {"form":form})
        return redirect("login")
    
# login
# get => to map us to the html form page through url
# post => to get the data from the form to the server

class LoginView(View):

    def get(self,request):

        form = LoginForm

        return render(request, "login.html",{"form":form})
    
    def post(self,request):

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user_obj = authenticate(request, username = username, password = password)

            if user_obj:

                login(request,user_obj)

                return redirect("task_read")
            
            else:
                 
                 form = LoginForm

                 return render(request, "login.html",{"form": form})

# logout

class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("login")      


# to add task


class TaskView(View):

    def get(self,request):

        form = TaskForm

        return render(request, "addtask.html",{"form":form})
    
    def post(self,request):

        form = TaskForm(request.POST) # to store the data which holds in post 

        if form.is_valid():

            TaskModel.objects.create(user_id = request.user, **form.cleaned_data)

        return render(request,"addtask.html",{"form":form})

# to read task

class TaskReadView(View):

    def get(Self,request):

        # items = TaskModel.objects.all()

        items = TaskModel.objects.filter(user_id = request.user)

        return render(request,"readtask.html", {"items":items})
    
# to update a task

@method_decorator(decorator=is_user,name="dispatch")
class TaskUpdateView(View):

    def get(self,request,**kwargs):

        id = kwargs.get('pk')

        item = TaskModel.objects.get(id = id)

        form = TaskForm(instance=item)

        return render(request,"update.html",{"form":form})    
    
    def post(self,request,**kwargs):

        id = kwargs.get('pk')

        item = TaskModel.objects.get(id = id)

        form = TaskForm(request.POST,instance=item)

        if form.is_valid():

            form.save()

        form = TaskForm

        return render(request,"update.html",{"form":form})
    
# to delete a task

@method_decorator(decorator=is_user,name="dispatch")   
class TaskDeleteView(View):

    def get(self,request,**kwargs):

        id = kwargs.get('pk')

        item = TaskModel.objects.get(id = id)

        item.delete()

        return redirect("task_read")
    
# to read a specific task

@method_decorator(decorator=is_user,name="dispatch")
class TaskDetailView(View):

    def get(self,request,**kwargs):

        id = kwargs.get('pk')

        item = TaskModel.objects.get(id = id)

        return render(request,"detail.html",{"item":item})
    
# to make a task with completed_status as True

class TaskEditView(View):

    def get(Self,request,**kwargs):

        id = kwargs.get('pk')

        item = TaskModel.objects.get(id = id)

        item.completed_status = True

        item.save()

        return redirect("task_read")
    
# forgot password

class ForgotPasswordView(View):

    def get(self,request):

        form = ForgotForm

        return render(request,"forgotpwd.html",{"form":form})
    
    def post(self,request):

        form = ForgotForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            user = User.objects.get(email = email)  # to get the email from the table and check whether those are same

            otp = random.randint(1000,9999) # generating 4 digit otp randomly

            OtpModel.objects.create(user_id = user, otp = otp)

            # ncxs josi ndrk zipx => email key 

            send_mail(subject="otp for password reset", message=str(otp), from_email="swanamsuresh88@gmail.com",
                      recipient_list=[email])
            
            return redirect("otpverify")
            
        return render(request,"forgotpwd.html",{"form":form})

# verify otp

class OtpVerifyView(View):

    def get(self,request):

        form = OtperifyForm

        return render(request,"otpverify.html",{"form":form})
    
    def post(Self,request):

        form = OtperifyForm(request.POST)

        if form.is_valid():

            otp = form.cleaned_data.get('otp')

            item = OtpModel.objects.get(otp = otp)

            user_id = item.user_id

            user = User.objects.get(id = user_id.id) # getting object from User table with above user_id

            username = user.username

            if item:

                request.session['user'] = username  # dict format => its life will be upto the closing of the tab

                return redirect("resetpwd")
            
        return render(request,"otpverify.html",{"form":form})


# password and confirm password

class ResetPasswordView(View):

    def get(self,request):

        form = ResetpasswordForm

        return render(request,"resetpwd.html",{"form":form})
    
    def post(self,request):

        form = ResetpasswordForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get('password')

            confirm_password = form.cleaned_data.get('confirm_password')

            if password == confirm_password:

                username = request.session.get('user')  # get user from session storage

                user = User.objects.get(username = username)  # get user_id from User table

                user.set_password(password)  # password 

                user.save()

                return redirect("login")
            
        return render(request,"resetpwd.html",{"form":form})
    

# filtering View
# methods used => get => giving only url, not passing data 

class TaskFilterView(View):

    def get(Self,request):

        category = request.GET.get('catergory') # data is getting from Htmls GET Method => means during filtering for a product that name of theproduct will show in url itself thats because get method

        Task = TaskModel.objects.filter(user_id = request.user) # all tasks of the logged in user

        tasks= Task.filter(task_category = category)

        print(tasks)

        return render(request,"filter.html",{"tasks":tasks})


class IndexView(View):
    def get(self,request):
        return render(request,"index.html")