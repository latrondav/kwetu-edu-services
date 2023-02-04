from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('login/', views.homelogin),
    path('signup/', views.homesignup),
    path('profile/', views.profile),
    path('updateprofile/', views.update_profile),
    path('signout/', views.signout),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('reactivate/<uidb64>/<token>/', views.reactivate, name="reactivate"),
    path('about/', views.about),
    path('addnewtestimonial/', views.add_new_testimonial),
    path('deletetestimonial/<testimonialid>/', views.delete_testimonial),
    path('services/', views.services),
    path('addnewservice/', views.add_new_service),
    path('deleteservice/<serviceid>/', views.delete_service),
    path('team/', views.team),
    path('upcoming_events/', views.upcoming_events),
    path('past_events/', views.past_events),
    path('recorded_events/', views.recorded_events),
    path('members/', views.members),
    path('updatemember/', views.update_member),
    path('contact/', views.contact),

    #reset password path
    path('resetpasswordform/', auth_views.PasswordResetView.as_view(template_name="password_mgt/pw_reset_form.html"), name= "password_reset_form"),
    path('resetpassworddone/', auth_views.PasswordResetDoneView.as_view(template_name="password_mgt/pw_reset_done.html"), name= "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_mgt/pw_reset_confirm.html"), name= "password_reset_confirm"),
    path('resetpasswordcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_mgt/pw_reset_complete.html"), name= "password_reset_complete"),

]