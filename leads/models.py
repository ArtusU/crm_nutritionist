from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_nutritionist = models.BooleanField(default=False)


class Organization(models.Model):
    user            = models.OneToOneField(User, related_name="organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Nutritionist(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    organization    = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.user.username} {self.organization}"


class Lead(models.Model):
    first_name      = models.CharField(max_length=20)
    last_name       = models.CharField(max_length=20)
    age             = models.IntegerField(default=0)
    description     = models.TextField()
    phone_number    = models.CharField(max_length=20)
    email           = models.EmailField()
    date_added      = models.DateTimeField(auto_now_add=True)
    organization    = models.ForeignKey("Organization", on_delete=models.CASCADE)
    nutritionist    = models.ForeignKey("Nutritionist", null=True, blank=True, on_delete=models.SET_NULL)
    category        = models.ForeignKey("Category", related_name="leads", blank=True, null=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    name            = models.CharField(max_length=30)
    organization    = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Organization.objects.create(user=instance)
        #Nutritionist.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)


