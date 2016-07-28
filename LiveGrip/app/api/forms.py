from django.contrib.admin.helpers import ActionForm
from django import forms

class SendFCMForm(ActionForm):
	title = forms.CharField()
	body = forms.CharField()