from django.contrib import admin
from .models import User, Lead, Nutritionist


admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Nutritionist)
