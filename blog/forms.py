from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'content', 'link', 'category']
        widgets = {
            'title':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content':  forms.Textarea(attrs={'class': 'form-control', 'rows': 7, 'placeholder': 'Write your content here… (optional if you provide a link)'}),
            'link':     forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com  (optional)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('content', '').strip() and not cleaned.get('link', '').strip():
            raise forms.ValidationError('Please provide at least some content or a link.')
        return cleaned
