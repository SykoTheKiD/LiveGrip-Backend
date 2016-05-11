from django import forms

class GCMForm(forms.Form):
	gcm_title = forms.CharField(label='Message Title')
	gcm_tickerText = forms.CharField(label='Message Ticker Text')
	gcm_message = forms.CharField(label='Message Contents', widget=forms.Textarea)
	gcm_url = forms.URLField(label='Message Image URL')
	small_message = forms.BooleanField(label='Small Notification?', required=False)