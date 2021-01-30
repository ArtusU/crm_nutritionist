import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from leads.models import Nutritionist
from .forms import NutritionistModelForm
from .mixins import OrganiserAndLoginRequiredMixin


class NutritionistListView(generic.ListView):
    template_name= "nutritionists/nutritionist_list.html"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Nutritionist.objects.filter(organization=organization)


class NutritionistCreateView(generic.CreateView):
    template_name = "nutritionists/nutritionist_create.html"
    form_class = NutritionistModelForm

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.is_nutritionist = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0, 100000)}")
        user.save()
        Nutritionist.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be a Nutritionist",
            message="You were added as a nutritionist on ECF Participants. Please login to start working.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(NutritionistCreateView, self).form_valid(form)

    
class NutritionistDetailView(generic.DetailView):
    template_name = "nutritionists/nutritionist_detail.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Nutritionist.objects.filter(organization=organization)


class NutritionistUpdateView(generic.UpdateView):
    template_name = "nutritionists/nutritionist_update.html"
    form_class = NutritionistModelForm
    
    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def get_queryset(self):
        return Nutritionist.objects.all()


class NutritionistDeleteView(generic.DeleteView):
    template_name = "nutritionists/nutritionist_delete.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Nutritionist.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

