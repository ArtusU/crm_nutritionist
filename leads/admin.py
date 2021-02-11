from django.contrib import admin
from .models import FollowUp, User, Lead, Nutritionist, Organization, Category


class LeadAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )

    list_display = ['date_added', 'first_name', 'last_name', 'age', 'email', 'nutritionist']
    list_display_links = ['first_name']
    list_editable = ['email']
    list_filter = ['category', 'nutritionist']
    search_fields = ['first_name', 'last_name', 'email']

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Nutritionist)
admin.site.register(Organization)
admin.site.register(FollowUp)



