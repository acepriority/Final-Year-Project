from django.shortcuts import render


class ViewIndexPages:
    """
    A base class for views that render index-like pages.

    This class provides a method, `get`, for rendering a template
    specified by the `template` attribute.

    Attributes:
        template: The template name to render.
    """
    def __init__(self, template_name=None):
        """
        Initializes the mixin with the specified template.

        Args:
            template: The template name to render the queryset.
        """
        self.template_name = template_name

    def get(self, request):
        """
        Render the specified template.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered template.
        """
        return render(request, self.template_name, {})

    def post(self, request):
        """
        Render the specified template.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered template.
        """
        return render(request, self.template_name, {})
