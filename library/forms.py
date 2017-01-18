'''
from django import forms
from django.shortcuts import get_object_or_404
from library.models import AreaOfExpertise, Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AreaSearchForm(forms.Form):
	area = forms.CharField(widget = forms.Textarea)
	
	def clean_text(self):
		area = self.cleanned_data['area']
		if area.strip() == '':
			raise forms.ValidationError(u'Search form is empty', code='validation_error')
		return area
		
	return askquestion
'''


	
