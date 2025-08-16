from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group,Permission
import re
from django.contrib.auth.forms import AuthenticationForm

class StyledFormMixin:
    """Mixin to apply consistent styling to form fields."""

    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CustomRegistrationForm(StyledFormMixin, UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must include at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must include at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            errors.append("Password must include at least one number.")
        if not re.search(r'[@#$%^&+=]', password):
            errors.append("Password must include at least one special character.")

        if errors:
            raise forms.ValidationError(errors)

        return password
    

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)



class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Select Role")

    fields = ['name', 'permissions']