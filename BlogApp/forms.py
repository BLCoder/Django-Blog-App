from django import forms
from django.contrib.auth.models import User
from .models import article
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class registerUser(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update({'placeholder':'First Name '})
		self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
		self.fields['email'].widget.attrs.update({'placeholder':'Your Email'})
		self.fields['username'].widget.attrs.update({'placeholder':'Username'})
		self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'placeholder':'Repeat your password'})
	class Meta:
		model = User
		fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]
        

class getLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model=User
        fields=[
            'username',
            'password'
        ]

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model=article
        exclude = ['article_author']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post' # get or post
        self.helper.add_input(Submit('submit', 'Update')) 