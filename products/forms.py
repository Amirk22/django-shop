from django import forms
from .models import Comment, CommentReply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','massage')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'نام شما'
            }),
            'massage': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            }),
            # 'reply': forms.Textarea(attrs={
            #     'class': 'form-control',
            #     'rows': 3,
            #     'placeholder': 'پاسخ خود را بنویسید...'
            # }),
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ('name','massage')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'نام شما'
            }),
            'massage': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }


