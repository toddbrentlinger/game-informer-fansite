from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from .models import Person
from fansite.models import ReplayEpisode

# Create your views here.

class PersonListView(generic.ListView):
    model = Person
    paginate_by = 20

class PersonDetailView(generic.DetailView):
    model = Person

def get_person_detail_view(request, person):
    replay_episodes = ReplayEpisode.objects.filter(Q(host=person) | Q(featuring=person)).distinct()

    context = {
        'person': person,
        'replay_episodes': replay_episodes
    }
    return render(request, 'people/person_detail.html', context=context)

def person_detail_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return get_person_detail_view(request, person)

def person_detail_slug_view(request, stub):
    person = get_object_or_404(Person, slug=stub)
    return get_person_detail_view(request, person)