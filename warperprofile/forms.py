from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profileimg', 'planet', 'star_system', 'species', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Tell the galaxy about yourself'}),
            'profileimg': forms.ClearableFileInput(attrs={'class': 'file-input'}),
            'planet': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your home planet'}),
            'star_system': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your star system'}),
            'species': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your species'}),
            'interests': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your interests'}),
        }
