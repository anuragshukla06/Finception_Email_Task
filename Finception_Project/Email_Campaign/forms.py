from django import forms
from . import models

class subscribe_form(forms.Form):
    first_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

    class Meta:
        model = models.User
        fields = ['first_name', 'email']

class blog_form(forms.Form):
    heading = forms.CharField(widget=forms.Textarea)
    article = forms.CharField(widget=forms.Textarea)

class email_form(forms.Form):
    subject = forms.CharField(max_length=50)
    op_message = forms.CharField(widget=forms.Textarea)