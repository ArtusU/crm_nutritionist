from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class OrganiserAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organiser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_organiser:
            return redirect("nutritionists:nutritionist-list")
        return super().dispatch(request, *args, **kwargs)

