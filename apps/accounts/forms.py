from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'phone', 'male', 'female']


class MyUserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Date of birth",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = get_user_model()
        exclude = ( 'date_joined', 'last_login', 'is_active', 'created_at', 'is_staff', 'password', 'groups',
                    'is_superuser', 'user_permissions',)

