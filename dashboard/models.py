from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime

class RegisterUser(models.Model):

    email_regex = RegexValidator(regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                                 message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.")  #^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  for custom

    userId = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)

    userName = models.CharField(max_length=500, null=True, blank=True)

    photo = models.FileField(blank=True, null=True, upload_to='static/UserProfileImages/')

    email = models.CharField(validators=[email_regex], max_length=500, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()

            usr_name = self.userName
            print(usr_name)
            user_obj = User.objects.create_user(
                username=usr_name, password=self.password, is_staff=False, email=self.email,
                first_name=self.name
            )

            user_data = list(User.objects.filter(username=user_obj).values('pk'))
            user_data[0].get('pk')
            print(user_data[0].get('pk'))
            self.userId = user_data[0].get('pk')
            self.user_id = user_data[0].get('pk')
            res = super(RegisterUser, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(RegisterUser, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res

