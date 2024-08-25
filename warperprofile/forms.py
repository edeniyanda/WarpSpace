from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profileimg', 'planet', 'star_system', 'species', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'profileimg': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }
