from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import User
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import logging

logger = logging.getLogger(__name__)


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

    def lockout_account(self, request, lockout_time):
        """
        Handle the account lockout by calculating the remaining lockout time and displaying an error message.

        Args:
            request: The HTTP request object.
            lockout_time: The datetime object representing the end of the lockout period.

        Returns:
            HttpResponseRedirect: Redirects to the login page with an error message.
        """
        remaining_lockout_time = (lockout_time - timezone.now()).total_seconds()
        minutes, seconds = divmod(int(remaining_lockout_time), 60)
        messages.error(request, f'Account locked. Try again after {minutes} minutes {seconds} seconds.')
        logger.warning(f'User locked out for {minutes} minutes {seconds} seconds.')
        return redirect('login')

    def limit_attempts(self, request, username, lockout_key, LOCKOUT_DURATION):
        """
        Limit login attempts by setting a lockout period.

        Args:
            request: The HTTP request object.
            lockout_key: The cache key for lockout.
            LOCKOUT_DURATION: The duration for the lockout in seconds.

        Returns:
            HttpResponseRedirect: Redirects to the login page with an error message.
        """
        lockout_time = timezone.now() + timezone.timedelta(seconds=LOCKOUT_DURATION)
        cache.set(lockout_key, lockout_time, timeout=LOCKOUT_DURATION)
        messages.error(request, f'Account locked. Try again after {int(LOCKOUT_DURATION // 60)} minutes {int(LOCKOUT_DURATION % 60)} seconds.')

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
        LOCKOUT_DURATION = 60
        lockout_key = f'lockout_{username.lower()}'
        login_attempts_key = f'login_attempts_{username.lower()}'

        lockout_time = cache.get(lockout_key)

        if lockout_time and lockout_time > timezone.now():
            self.lockout_account(request, lockout_time)

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
                    self.limit_attempts(request, username, lockout_key, LOCKOUT_DURATION)
                    logger.warning(f'User {username} account locked due to too many login attempts.')

                else:
                    messages.error(request, 'Invalid username or password')
                    logger.warning(f'Invalid login attempt for user {username}. Attempts: {login_attempts}')
            else:
                messages.error(request, 'Invalid username or password')
                logger.warning(f'Invalid login attempt for non-existing user {username}.')

            return redirect('login')


class URLBuilder:
    """
    A utility class to build absolute URLs for the current site.

    Attributes:
        scheme (str): The URL scheme ('http' or 'https').
        host (str): The host/domain of the current site.
    """

    def __init__(self, request):
        """
        Initializes the URLBuilder with the scheme and host.

        Args:
            request: The Django request object.
        """
        self.scheme = 'https' if request.is_secure() else 'http'
        self.host = get_current_site(request).domain

    def build_url(self, view_name, *args, **kwargs):
        """
        Builds a full URL for the given view name.

        Args:
            view_name (str): The name of the view.
            *args: Positional arguments for the view.
            **kwargs: Keyword arguments for the view.

        Returns:
            str: The full URL for the given view.
        """
        path = reverse(view_name, args=args, kwargs=kwargs)
        return f"{self.scheme}://{self.host}{path}"
