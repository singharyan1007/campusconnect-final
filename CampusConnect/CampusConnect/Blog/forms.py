from django.forms import ModelForm
from .models import Blogpost

class PostForm(ModelForm):
    class Meta:
        model=Blogpost
        fields=["content"]
        