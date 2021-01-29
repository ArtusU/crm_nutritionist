from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.views import generic
from leads.models import Nutritionist
from .forms import NutritionistModelForm


class NutritionistListView(LoginRequiredMixin, generic.ListView):
    template_name= "nutritionists/nutritionist_list.html"
    
    def get_queryset(self):
        return Nutritionist.objects.all()


class NutritionistCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "nutritionists/nutritionist_create.html"
    form_class = NutritionistModelForm

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def form_valid(self, form):
        nutritionist = form.save(commit=False) 
        nutritionist.organization = self.request.user.userprofile
        nutritionist.save()
        return super(NutritionistCreateView, self).form_valid(form)

    
class NutritionistDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "nutritionists/nutritionist_detail.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        return Nutritionist.objects.all()


class NutritionistUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "nutritionists/nutritionist_update.html"
    form_class = NutritionistModelForm
    
    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

    def get_queryset(self):
        return Nutritionist.objects.all()


class NutritionistDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "nutritionists/nutritionist_delete.html"
    context_object_name = "nutritionist"

    def get_queryset(self):
        return Nutritionist.objects.all()

    def get_success_url(self):
        return reverse("nutritionists:nutritionist-list")

