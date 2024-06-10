from django.urls import path
from .views import (LoginUser,
                    LogoutUser,
                    VerifyEmail,
                    IndexResetPassword,
                    ResetPassword)


urlpatterns = [
    path('login_user/', LoginUser.as_view(), name='login_user'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('login/verify_email/', VerifyEmail.as_view(), name='verify_email'),
    path('index_reset_password/<str:receiver_email>/', IndexResetPassword.as_view(), name='index_reset_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password')
]
