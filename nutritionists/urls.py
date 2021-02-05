from django.urls import path
from .views import (
    NutritionistListView, 
    NutritionistCreateView, 
    NutritionistDetailView, 
    NutritionistUpdateView, 
    NutritionistDeleteView
)

app_name = "nutritionists"

urlpatterns = [
    path('', NutritionistListView.as_view(), name='nutritionist-list'),
    path('<int:pk>/', NutritionistDetailView.as_view(), name='nutritionist-detail'),
    path('<int:pk>/update/', NutritionistUpdateView.as_view(), name='nutritionist-update'),
    path('<int:pk>/delete/', NutritionistDeleteView.as_view(), name='nutritionist-delete'),
    path('create/', NutritionistCreateView.as_view(), name='nutritionist-create')
]


