from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import LoginMixin
from django.contrib.auth.models import User
from .models import UserProfile
from components.email import SendEmailMixin
from index_app.utils import ViewIndexPages


class LoginUser(LoginMixin, View):
    def __init__(self):
        super().__init__(model=UserProfile)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        return self.handle_login_attempt(request, username, password)

    def get(self, request):
        return redirect('login')


class LogoutUser(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('auth:login_user')


class VerifyEmail(ViewIndexPages, SendEmailMixin, View):
    def __init__(self):
        ViewIndexPages.__init__(self, template_name='auth_app/verify_email.html')
        SendEmailMixin.__init__(self)
        self.model = User

    def post(self, request):
        email = request.POST.get('email')
        queryset = self.model.objects.filter(email=email).first()
        user = queryset

        if user is None:
            messages.error(request, f'User with email {email} not found.')
            return render(request, self.template_name)

        self.send_reset_password_email(request, email)
        return redirect('login')


class IndexResetPassword(View):
    template_name = 'auth_app/index_reset_password.html'
    model = User

    def get(self, request, receiver_email):
        user = self.model.objects.filter(email=receiver_email).first()
        if user:
            return render(request, self.template_name, {'email': receiver_email})
        else:
            messages.error(request, 'User not found.')
            return redirect('login')

    def post(self, request, receiver_email):
        print(f"POST request received for email: {receiver_email}")
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('auth:reset_password', receiver_email=receiver_email)

        try:
            user = self.model.objects.get(email=receiver_email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        except self.model.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('auth:reset_password', receiver_email=receiver_email)


class ResetPassword(View):
    template_name = 'auth_app/reset_password.html'
    model = User

    def get(self, request):
        return render(request, self.template_name, context={})

    def post(self, request):
        id = request.user.id
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('auth:reset_password')

        try:
            user = self.model.objects.get(id=id)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        except self.model.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('auth:reset_password')
