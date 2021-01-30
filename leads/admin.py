from django.contrib import admin
from .models import User, Lead, Nutritionist, UserProfile, Category


admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Nutritionist)
admin.site.register(UserProfile)
