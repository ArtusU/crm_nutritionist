import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views import generic
from leads.models import Nutritionist
from .forms import NutritionistModelForm
from .mixins import OrganiserAndLoginRequiredMixin

class NutritionistListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name= "nutritionists/nutritionist_list.html"
    
    def get_queryset(self):
        organization = self.request.user.organization
        return Nutritionist.objects.filter(organization=organization)


class NutritionistCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "nutritionists/nutritionist_create.html"
    form_class = NutritionistModelForm

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.is_organiser = False
        user.is_nutritionist = True
        user.set_password(f"{random.randint(0, 100000)}")
        user.save()  
        Nutritionist.objects.create(
            user=user,
            organization=self.request.user.organization
        )
        send_mail(
            subject="You are invited to be a Nutritionist",
            message="You were added as a nutritionist on ECF Participants Service. Please go to the service and use your email to reset default password and set up new one.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(NutritionistCreateView, self).form_valid(form)


    
class NutritionistDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "nutritionists/nutritionist_detail.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        organization = self.request.user.organization
        return Nutritionist.objects.filter(organization=organization)


class NutritionistUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "nutritionists/nutritionist_update.html"
    form_class = NutritionistModelForm
    
    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def get_queryset(self):
        organization = self.request.user.organization
        return Nutritionist.objects.filter(organization=organization)

class NutritionistDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "nutritionists/nutritionist_delete.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        organization = self.request.user.organization
        return Nutritionist.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    

