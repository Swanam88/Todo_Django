from django import forms

from my_app.models import User, TaskModel

class UserRegistrationForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ['username','password','email']

        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control w-75 mx-auto", "placeholder":"Enter your Username"}),
            "password":forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto", "placeholder": "password"}),
            "email":forms.EmailInput(attrs={"class":"form-control w-75 mx-auto","placeholder":"Enter email"})
        }

class LoginForm(forms.Form):

    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control w-75 mx-auto", "placeholder":"Enter your Username"}))

    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto", "placeholder": "password"}))


# form for CRUD => create,read,update,delete
# taskname,due_date(yyyy-mm-dd),description,task_category  => we need to give

class TaskForm(forms.ModelForm):

    class Meta:

        model = TaskModel

        exclude = ['created_date','completed_status','user_id']

# forgot password

class ForgotForm(forms.Form):

    email = forms.CharField(max_length=100)

# verify Otp

class OtperifyForm(forms.Form):

    otp = forms.CharField(max_length=10)

# password and confirm password

class ResetpasswordForm(forms.Form):

    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto", "placeholder": "Enter New password"}))

    confirm_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control w-75 mx-auto", "placeholder": "Confirm password"}))

    