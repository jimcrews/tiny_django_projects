from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notes
from .forms import NotesForm


class NotesDeleteView(DeleteView):
    model = Notes
    success_url = "/smart/notes"
    template_name = "notes/notes_delete.html"

class NotesUpdateView(UpdateView):
    model = Notes
    form_class = NotesForm
    success_url = "/smart/notes"


class NotesCreateView(CreateView):
    model = Notes
    form_class = NotesForm
    success_url = "/smart/notes"

    # override to include user_id in create note
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/login"

    # override get request to get only logged in users notes
    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = "note"
    template_name = "notes/detail.html"