from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import User


class LoginMixin:
    """
    A mixin for handling user login functionality.

    This mixin provides methods for logging in a user and redirecting them
    based on their user profile.

    Attributes:
        model: The model class representing user profiles.
    """

    def __init__(self, model=None):
        """
        Initializes the mixin with the specified model.

        Args:
            model: The model class representing the database table.
        """
        self.model = model

    def access_control(self, request, user):
        """
        Controls access to different parts of the application based on the user's profile.

        Args:
            request: The HTTP request object.
            user: The user object.

        Returns:
            HttpResponseRedirect or HttpResponse: A redirect response based on the user's profile or an error message.
        """
        user_profile = get_object_or_404(self.model, user=user)

        if user_profile.is_staff:
            return redirect('staff:staff')
        elif user_profile.is_dvo:
            return redirect('dvo:dvo')
        elif user_profile.is_lc5:
            return redirect('lc5:lc5')
        elif user_profile.is_trader:
            return redirect('trader:trader')
        else:
            return redirect('login')

    def login_user(self, request, user):
        """
        Log in the specified user and redirect them based on their profile.

        Args:
            request: The HTTP request object.
            user: The user object to log in.

        Returns:
            HttpResponseRedirect or HttpResponse: A redirect response
            based on the user's profile or a login error message.
        """
        login(request, user)
        return self.access_control(request, user)

    def handle_login_attempt(self, request, username, password):
        """
        Handle a login attempt, including checking for lockout and incrementing login attempts.

        Args:
            request: The HTTP request object.
            username: The username from the login form.
            password: The password from the login form.

        Returns:
            HttpResponseRedirect or HttpResponse: A response based on the success or failure of the login attempt.
        """
        MAX_LOGIN_ATTEMPTS = 3
        LOCKOUT_DURATION = 300
        GENERAL_LOCKOUT_DURATION = 300
        lockout_key = f'lockout_{username.lower()}'
        login_attempts_key = f'login_attempts_{username.lower()}'

        general_lockout_key = 'general_lockout'
        general_lockout_time = cache.get(general_lockout_key)

        if general_lockout_time and general_lockout_time > timezone.now():
            remaining_lockout_time = (general_lockout_time - timezone.now()).total_seconds()
            minutes, seconds = divmod(int(remaining_lockout_time), 60)
            messages.error(request, f'Login disabled. Try again after {minutes} minutes {seconds} seconds.')
            return redirect('login')

        lockout_time = cache.get(lockout_key)

        if lockout_time and lockout_time > timezone.now():
            remaining_lockout_time = (lockout_time - timezone.now()).total_seconds()
            minutes, seconds = divmod(int(remaining_lockout_time), 60)
            messages.error(request, f'Account locked. Try again after {minutes} minutes {seconds} seconds.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            cache.delete(login_attempts_key)
            cache.delete(lockout_key)
            return self.login_user(request, user)
        else:
            if User.objects.filter(username=username).exists():
                login_attempts = cache.get(login_attempts_key, 0) + 1
                cache.set(login_attempts_key, login_attempts, timeout=LOCKOUT_DURATION)

                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    lockout_time = timezone.now() + timezone.timedelta(seconds=LOCKOUT_DURATION)
                    cache.set(lockout_key, lockout_time, timeout=LOCKOUT_DURATION)
                    messages.error(request, f'Account locked. Try again after {int(LOCKOUT_DURATION // 60)} minutes {int(LOCKOUT_DURATION % 60)} seconds.')
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                cache.set(general_lockout_key, timezone.now() + timezone.timedelta(seconds=GENERAL_LOCKOUT_DURATION), timeout=GENERAL_LOCKOUT_DURATION)
                messages.error(request, 'Login disabled due to multiple invalid attempts. Try again after 5 minutes.')

            return redirect('login')
