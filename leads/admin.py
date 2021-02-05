from django.contrib import admin
from .models import User, Lead, Nutritionist, Organization, Category


admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Nutritionist)
admin.site.register(Organization)
