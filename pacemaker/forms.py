from django import forms
from django.contrib.auth.forms import UserCreationForm


class SuperuserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        UserCreationForm.Meta.fields += ('email',)

    def save(self, commit=True):
        user = super(SuperuserCreationForm, self).save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

