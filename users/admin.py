""" docstring """
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    """ 유저를 추가하거나 유저 객체를 변경하는 양식입니다. """

    list_display = ['username', 'email', 'auth_provider', 'created_at']

    list_filter = ['username', 'email', 'auth_provider', 'created_at']

    list_display_links = ['username', 'email', 'auth_provider', 'created_at']

    search_fields = ['username', 'email', 'auth_provider', 'created_at']

    ordering = ['username', 'email', 'auth_provider', 'created_at']


    # fieldsets = (
    #     (None, {
    #         "fields": ["email", "username"],
    #         "classes": ["collapse", "wide"],
    #     }
    #     ),
    # )
    # add_fieldsets = (
    #     (None, {
    #          "fields": ["email", "username", "password1", "password2"],
    #          "classes": ["collapse", "wide"],
    #      }
    #      )
    # )


admin.site.register(User, UserAdmin)
# unregister the Group model from admin.
