from django import forms 

from .models import Post


# title body image author 


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'body', 'image']

