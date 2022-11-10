from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

def upcoming_events(request):
    return render(request, 'events.html')

def past_events(request):
    return render(request, 'past_events.html')

def recorded_events(request):
    return render(request, 'recorded_events.html')

def members(request):
    return render(request, 'members.html')

def contact(request):
    return render(request, 'contact.html')
