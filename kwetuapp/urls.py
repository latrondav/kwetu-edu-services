from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.homelogin),
    path('signup/', views.homesignup),
    path('profile/', views.profile),
    path('updateprofile/', views.updateprofile),
    path('signout/', views.signout),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('about/', views.about),
    path('services/', views.services),
    path('team/', views.team),
    path('upcoming_events/', views.upcoming_events),
    path('past_events/', views.past_events),
    path('recorded_events/', views.recorded_events),
    path('members/', views.members),
    path('contact/', views.contact),
]