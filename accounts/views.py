from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import CustomUser

# Create your views here.

class CustomUserListView(generic.ListView):
    model = CustomUser

class CustomUserDetailView(generic.DetailView):
    model = CustomUser

def customuser_detail_slug_view(request, slug):
    customuser = get_object_or_404(CustomUser, slug=slug)
    return render(request, 'customuser_detail.html', context={ 
        'customuser': customuser,
    })