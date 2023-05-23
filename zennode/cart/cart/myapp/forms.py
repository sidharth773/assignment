from django import forms
from .models import User,Mycart

class UserForm(forms.ModelForm):
    """Form definition for User."""
    password=forms.CharField(
        widget=forms.PasswordInput())
    confirm_password=forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput())

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ['first_name','last_name','username','email','phone','password']

class MyCart(forms.ModelForm):

    class Meta:
        model = Mycart
        exclude=('product_a','product_b','product_c','price','costm')


class ProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)
    gift_wrap = forms.BooleanField(required=False)
