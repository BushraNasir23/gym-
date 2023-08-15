from django import forms
from .models import Members
class MemberForm(forms.ModelForm):
    class Meta:
        model=Members
        fields='__all__'