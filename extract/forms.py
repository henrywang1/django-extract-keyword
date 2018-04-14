from django import forms
class NameForm(forms.Form):
    article = forms.CharField(label="", widget=forms.Textarea(
        attrs={'width':"100%", 'cols' : "80", 'rows': "20"}
    ))