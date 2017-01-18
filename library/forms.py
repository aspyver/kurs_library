
from django import forms
from django.shortcuts import get_object_or_404
from library.models import AreaOfExpertise, Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
	
	
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError(u'Username is empty', code='validation_error')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError(
                u'Password is empty', code='validation_error')
        return password

    def save(self):
        user = authenticate(**self.cleaned_data)
        return user




'''
class AreaSearchForm(forms.Form):
	area = forms.CharField(widget = forms.Textarea)
	
	def clean_text(self):
		area = self.cleanned_data['area']
		if area.strip() == '':
			raise forms.ValidationError(u'Search form is empty', code='validation_error')
		return area
		
	return askquestion
'''


	
