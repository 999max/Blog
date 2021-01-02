from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        labels = {'title': 'Title', 'text': 'Text'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Comment:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 90})}
