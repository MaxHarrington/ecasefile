from django import forms
from .models import RawFile
from ckeditor.widgets import CKEditorWidget

class TextForm(forms.Form):
	text = forms.CharField(label='', widget=CKEditorWidget(attrs={}))
	title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your amazing article title goes here...'}))

class CasefileForm(forms.Form):
	title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your amazing casefile title goes here...'}))
	description = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'A brief description of your casefile...'}))

class UploadCase(forms.ModelForm):
	class Meta:
		model = RawFile
		fields = 'title', 'file'