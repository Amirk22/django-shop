from django import forms

from contact_us.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'نام'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'ایمیل'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'subject',
                'placeholder': 'موضوع'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message',
                'placeholder': 'پیام',
                'rows': 4,
                'style': 'resize:none;'
            }),
        }