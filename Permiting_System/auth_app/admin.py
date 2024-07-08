from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from staff_app.models import Trader, TraderLicense, District, Quarantine
from dvo_app.models import Animal, Permit, AnimalInfo
from trader_app.models import PermitRequest


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    # Define the fields to display in the User add form
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Trader)
admin.site.register(Animal)
admin.site.register(Permit)
admin.site.register(AnimalInfo)
admin.site.register(PermitRequest)
admin.site.register(TraderLicense)
admin.site.register(District)
admin.site.register(Quarantine)
