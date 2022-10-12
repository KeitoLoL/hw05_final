from django import forms
from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'введите текст',
            'group': 'Выберите группу',
        }
        widgets = {
            'text': forms.Textarea(attrs={'row': 12, 'cols': 45})
        }
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет отноститься пост',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'введите текст',
        }
        widgets = {
            'text': forms.Textarea(attrs={'row': 40, 'cols': 10})
        }
        help_texts = {
            'text': 'Текст комментария',
        }
