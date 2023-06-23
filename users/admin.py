from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
# Register your models here.


class UserAdmin(BaseUserAdmin):
    """ 유저를 추가하거나 유저 객체를 변경하는 양식입니다. """

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return("username", "created_at", )
        else:
            return("created_at", )

    # 유저 모델을 표시하는 데 사용할 필드입니다.
    # 'auth.User'의 특정 필드를 참조하여 'baseUserAdmin'을 재정의합니다.
    list_display = ["email", "username", "is_admin", "is_active"]
    list_display_links = ["username", ]
    list_filter = ["username", ]
    search_fields = ["username", "email", ]

    fieldsets = [
        (None, {"fields": ["username", "password", "created_at", ]}), # "email", 
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
    ]
    # 'add_fieldsets'는 'ModelAdmin' 표준 특성이 아닙니다.
    # 'get_fieldsets'를 재정의하면 'UserAdmin'은 유저를 만들 때 이 속성을 추가로 사용합니다.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2"], # password1,2 해싱
            },
        ),
    ]

    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# unregister the Group model from admin.