from django import forms

class creatlist(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description', 'rows':3, 'cols':5,'class': 'form-control',}))


