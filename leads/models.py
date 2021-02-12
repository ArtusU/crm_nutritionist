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

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
'''
    def get_age_below_26(self):
        return super().get_queryset().filter(age__lt=26)

class BlankLeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category__isnull=True)
'''
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
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    converted_date  = models.DateTimeField(blank=True, null=True)

    objects = LeadManager()

    '''
    Lead.objects.get_age_below_26()
    blank_objects = BlankLeadManager()
    '''
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"



class Category(models.Model):
    name            = models.CharField(max_length=30)
    organization    = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Organization.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)


