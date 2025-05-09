from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#all forms for this project
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username",)

  

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

class ImportNotesForm(forms.Form):
    import_file = forms.FileField(
        label='Select JSON file to import',
        help_text='Upload a JSON file containing your notes.'
    )