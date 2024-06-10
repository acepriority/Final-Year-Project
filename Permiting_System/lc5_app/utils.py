from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


class LC5RequiredMixin(LoginRequiredMixin):
    template_name = None

    def get_template_name(self):
        if self.template_name is None:
            raise NotImplementedError("Subclasses must define a template_name")
        return self.template_name

    def get(self, request):
        if request.user.userprofile.is_lc5:
            return render(request, self.get_template_name(), context={})
        else:
            return HttpResponseForbidden(f"You are authenticated as {request.user}, but are not authorized to access this page.")