from django.forms import ModelForm
from .models import Account
from Projects.models import projects
class AccountForm(ModelForm):
    class Meta:
        model=Account
        fields='__all__'

class projectForm(ModelForm):
    class Meta:
        model=projects
        fields=['description']

