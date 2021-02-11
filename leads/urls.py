from django.urls import path
from leads.views import (
    LeadListView, 
    LeadDetailView, 
    LeadCreateView, 
    LeadUpdateView, 
    LeadDeleteView, 

    AssignNutritionistView, 
    LeadCategoryUpdateView,

    CategoryListView, 
    CategoryDetailView, 
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    FollowUpCreateView
    )

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),

    path('<int:pk>/assign-nutritionist/', AssignNutritionistView.as_view(), name='assign-nutritionist'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='lead-followup-create'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create')
]

