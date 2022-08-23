from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Person
from replay.models import ReplayEpisode
from episodes.models import Episode

def person_list_view(request):
    person_list = Person.objects.all()
    paginator = Paginator(person_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'people/person_list.html', context=context)

def get_person_detail_view(request, person):
    episode_list = ReplayEpisode.objects.filter(Q(host=person) | Q(featuring=person)).distinct()
    paginator = Paginator(episode_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'person': person,
        'page_obj': page_obj,
    }
    return render(request, 'people/person_detail.html', context=context)

def person_detail_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return get_person_detail_view(request, person)

def person_detail_slug_view(request, slug):
    person = get_object_or_404(Person, slug=slug)
    return get_person_detail_view(request, person)