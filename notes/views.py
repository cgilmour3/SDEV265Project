from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm, RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from .forms import ImportNotesForm
from django.contrib import messages
from django.contrib.auth import login

#registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:note_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})
#create note view
@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})
#edit note view
@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})
#delete note view
@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

#export note view
@login_required
def export_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('created_at')
    note_data = []
    for note in notes:
        note_data.append({
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
        })
    json_data = json.dumps(note_data, cls=DjangoJSONEncoder, indent=4)

    
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="notes_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response
#import note view
@login_required
def import_notes(request):
    if request.method == 'POST':
        form = ImportNotesForm(request.POST, request.FILES)
        if form.is_valid():
            import_file = request.FILES['import_file']
            if not import_file.name.endswith('.json'):
                messages.error(request, 'Invalid file format. Please upload a JSON file.')
                return render(request, 'notes/import_notes.html', {'form': form})
            try:
                data = json.load(import_file)
                print(f"Data after json.load(): {data}")
                imported_count = 0
                for item in data:
                    print(f"Attempting to import: {item}")
                    try:
                        Note.objects.create(
                            user=request.user,
                            title=item.get('title', 'Untitled'),
                            content=item.get('content', ''),
                            created_at=item.get('created_at', timezone.now()),
                            updated_at=item.get('updated_at', timezone.now()),
                        )
                        imported_count += 1
                        print(f"Successfully imported: {item['title']}")
                    except Exception as e:
                        messages.error(request, f'Error importing note (general): {e}')
                        print(f"Failed to import (general): {item['title']} - Error: {e}")
                    except django.core.exceptions.ValidationError as e:
                        messages.error(request, f'Error importing note (validation): {e}')
                        print(f"Failed to import (validation): {item['title']} - Validation Error: {e}")
                messages.success(request, f'{imported_count} notes imported successfully.')
                return redirect('notes:note_list')
            except json.JSONDecodeError:
                messages.error(request, 'Invalid JSON format in the uploaded file.')
            except Exception as e:
                messages.error(request, f'An error occured during import (outer): {e}')
        else:
            messages.error(request, 'Please select a file to import.')
    else:
        form = ImportNotesForm()
    return render(request, 'notes/import_notes.html', {'form': form})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'