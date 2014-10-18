from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    text  = forms.Textarea()
    
    class Meta:
        model = Entry
        fields = ('title', 'text')
