from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    A form to create and update posts.
    """
    class Meta:
        model = Post
        fields = ['title', 'description', 'thumbnail', 'status', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description...', 'rows': 5}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'js-simplemde', 'placeholder': 'Write Your Content Here!'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'thumbnail': 'Thumbnail',
            'status': 'Status',
        }
        help_texts = {
            'title': 'Enter the title of the post.',
            'description': 'Enter the description of the post.',
            'thumbnail': 'Upload an image for the post.',
            'status': 'Select the status of the post.',
            'content': 'Enter the content of the post.',
        }
        error_messages = {
            'title': {
                'required': 'This field is required.',
            },
            'content': {
                'required': 'This field is required.',
            },
        }
    


