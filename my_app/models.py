from django.db import models

from django.contrib.auth.models import User  # imported user from application contrib.auth => where all the fields for user registration are already present

# if you need to create by your own way then -> need to inherit AbstractBaseUser class


class TaskModel(models.Model):

    task_name = models.CharField(max_length=100)

    created_date = models.DateField(auto_now_add=True)

    due_date = models.DateField()

    description = models.TextField(blank=True, null=True) # this field will be optional

    category = [('work','work'),
                ('personal','personal'),
                ('urgent','urgent')
                ]
    
    task_category = models.CharField(max_length=100,choices=category)

    completed_status = models.BooleanField(default=False)

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)  # relation will be one to many

    def __str__(self):
        return self.task_name
    

    
class OtpModel(models.Model):

    user_id = models.ForeignKey(User,on_delete=models.CASCADE) # relation => onte to many => because one user can select forgot pwd so many times

    otp = models.CharField(max_length=100)

    created_at = models.DateField(auto_now_add=True)
