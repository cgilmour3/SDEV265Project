from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

class ImportNotesForm(forms.Form):
    import_file = forms.FileField(
        label='Select JSON file to import',
        help_text='Upload a JSON file containing your notes.'
    )