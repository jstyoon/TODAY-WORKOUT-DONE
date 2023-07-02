""" docstring """
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from users.models import User


class UserCreationForm(forms.ModelForm):
    """ 새 사용자를 만들기 위한 양식으로 모든 필수 필드와 반복되는 암호를 포함합니다. """

    class Meta:
        """ 유저모델 필드 전부 """
        model = User
        fields = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'photo', 'about_me', 'is_superuser']

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput)

    def clean_password2(self):
        """ 두 비밀번호 항목이 일치하는지 확인. """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """ 제공된 비밀번호를 암호화 형식으로 저장 """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'photo', 'about_me', 'is_superuser']


class UserAdmin(BaseUserAdmin):
    """ 이 양식은 사용자를 추가하거나 사용자 개체를 변경하는 데 사용됩니다. """
    form = UserChangeForm
    add_form = UserCreationForm

    exclude = ("date_joined", "first_name", "last_name")

    list_display = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'created_at', 'updated_at', 'photo', 'about_me', 'is_superuser']

    list_filter = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'created_at', 'updated_at', 'photo', 'about_me', 'is_superuser']

    list_display_links = ["id", "email", "username"]

    search_fields = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'created_at', 'updated_at', 'photo', 'about_me', 'is_superuser']

    ordering = ['id', 'last_login', 'username', 'email', 'is_verified', 'is_active', 'is_staff', 'created_at', 'updated_at', 'photo', 'about_me', 'is_superuser']

    filter_horizontal = []


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
admin.site.unregister(Group)
# unregister the Group model from admin.
