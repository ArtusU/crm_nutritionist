from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import query
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from nutritionists.mixins import OrganiserAndLoginRequiredMixin
from .models import Lead, Category
from .forms import (
    LeadModelForm, 
    CustomUserCreationForm, 
    AssignNutritionistForm, 
    LeadCategoryUpdateForm, 
    CategoryModelForm
)

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class LeadListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.organization,  nutritionist__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.nutritionist.organization, nutritionist__isnull=False)
            queryset = queryset.filter(nutritionist__user=user)  #logged in nutritioninst
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.organization, nutritionist__isnull=True)

            context.update({
                "unassigned_leads": queryset
            })
        return context

class LeadDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.organization,  nutritionist__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.nutritionist.organization, nutritionist__isnull=False)
            queryset = queryset.filter(nutritionist__user=user)  #logged in nutritioninst
        return queryset

class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.organization
        lead.save()
        send_mail(
            subject="The Participant has been created.", 
            message="The Participant has been created. Go to ECF CRM Participants to assign Participant to the Nutritionist.",
            from_email="test@test.com",
            recipient_list=['test2@test.com']
        )
        messages.success(self.request, 'You have successfully created a lead')
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.organization)

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def lead_update(request, pk):
        lead = Lead.objects.get(id=pk)
        form = LeadModelForm(instance=lead)
        if request.method == "POST":
            form = LeadModelForm(request.POST, instance=lead)
            if form.is_valid():
                form.save()
                return redirect("/leads")
        context = {
            "form": form,
            "lead": lead
        }
        return render(request, "leads/lead_update.html", context)

class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.organization)



class AssignNutritionistView(generic.FormView):
    template_name = "leads/assign_nutritionist.html"
    form_class = AssignNutritionistForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignNutritionistView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        nutritionist = form.cleaned_data["nutritionist"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.nutritionist = nutritionist
        lead.save()
        return super(AssignNutritionistView, self).form_valid(form)
        


class CategoryListView(generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.nutritionist.organization)

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.nutritionist.organization)
        return queryset

class CategoryDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.nutritionist.organization)
        return queryset


class CategoryCreateView(generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.organization
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.nutritionist.organization)
        return queryset


class CategoryDeleteView(generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organiser:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.nutritionist.organization)
        return queryset



class LeadCategoryUpdateView(generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.nutritionist.organization)
            queryset = queryset.filter(nutritionist__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})