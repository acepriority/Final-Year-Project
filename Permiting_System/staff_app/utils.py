from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


class StaffRequiredMixin(LoginRequiredMixin):
    template_name = None

    def get_template_name(self):
        if self.template_name is None:
            raise NotImplementedError("Subclasses must define a template_name")
        return self.template_name

    def get(self, request):
        if request.user.userprofile.is_staff:
            return render(request, self.get_template_name(), context={})
        else:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")


class ViewTablesMixin:
    def __init__(self, model=None, template=None):
        """
        Initializes the mixin with the specified model and template.

        Args:
            model: The model class representing the database table.
            template: The template name to render the queryset.
        """
        self.model = model
        self.template_name = template

    def get(self, request):
        """
        Retrieve all objects of the specified model and render a template with the queryset.

        Returns:
            HttpResponse: The response containing the rendered template with the queryset as context.
        """
        queryset = self.model.objects.all()
        return render(request, self.template_name, context={self.model.__name__.lower(): queryset})
