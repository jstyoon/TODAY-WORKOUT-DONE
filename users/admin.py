from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
# Register your models here.

class UserCreationForm(forms.ModelForm):
    """ 새 유저를 생성하기 위한 양식입니다. 
    모든 필수 필드와 반복되는 암호를 포함합니다."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ 유저를 업데이트하기 위한 양식입니다. 
    유저의 모든 필드를 포함하지만 
    암호 필드를 관리자의 비활성화된 암호 해시 표시 필드로 바꿉니다."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "username", "password", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    """ 유저를 추가하거나 유저 객체를 변경하는 양식입니다. """
    form = UserChangeForm
    add_form = UserCreationForm

    # 유저 모델을 표시하는 데 사용할 필드입니다.
    # 'auth.User'의 특정 필드를 참조하는 'baseUserAdmin'의 정의를 재정의합니다
    list_display = ["email", "username", "is_admin", "is_active"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # 'add_fieldsets'는 표준 'ModelAdmin' 특성이 아닙니다.
    # 'UserAdmin'은 유저를 만들 때 이 속성을 사용하도록 'get_fieldsets'를 재정의합니다.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)