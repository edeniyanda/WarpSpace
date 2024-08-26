from django import forms
from .models import Post

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea',  # Bulma's textarea class
                'placeholder': 'Tell the Universe what is popping...',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'file-input'
            }),
        }
