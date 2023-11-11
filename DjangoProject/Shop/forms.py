from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from . models import Customer

# # Registration form start here...........
class Registration_form(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Your Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}


# //  Login form start here...........
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current_password', 'class':'form-control'}))



# // Password change form start here .. ..
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'current-password','autofocus':True,'placeholder':'Give your old password here'}))
    new_password1= forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new password', 'placeholder':'Create a new password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new password', 'placeholder':'Re-enter your new password'}))


#// Password Reset Form start here .....
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=50, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

#// Set password form
class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'new password', 'placeholder':'Re-enter your new password'}))


# // Customer Profile ..
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','division','district','thana', 'villorroad', 'zipcode']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'division':forms.Select(attrs={'class':'form-control'}),
            'district':forms.Select(attrs={'class':'form-control'}),
            'thana':forms.TextInput(attrs={'class':'form-control'}),
            'villorroad':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'})
                   }