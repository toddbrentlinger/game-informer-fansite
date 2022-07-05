from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Person

# Create your views here.

class PersonListView(generic.ListView):
    model = Person
    paginate_by = 20

class PersonDetailView(generic.DetailView):
    model = Person

def person_detail_slug_view(request, stub):
    person = get_object_or_404(Person, slug=stub)
    return render(request, 'people/person_detail.html', context={'person': person})