from django import forms
from django.db.models import fields
from .models import PJArticles, PJComments

class PJArticleForm(forms.ModelForm):

    class Meta:
        model = PJArticles
        fields = ['title','description','content','pub_user']

class CommentForm(forms.ModelForm):

    class Meta:
        model = PJComments
        fields = ['user','comment']


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="Imię") 
    last_name = forms.CharField(max_length=50, label="Nazwisko") 
    c_mail = forms.EmailField(max_length=50, label="Mail") 
    text = forms.CharField(widget=forms.Textarea, max_length=1000, label="Treść") 
