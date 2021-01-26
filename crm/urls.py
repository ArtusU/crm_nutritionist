from leads.views import landing_page
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing-page'),
    path('leads/', include('leads.urls', namespace='leads'))
]
