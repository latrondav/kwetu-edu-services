from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from kwetuproject import settings
from .token_1 import generate_token
from . forms import *
from . models import *
from django.core.mail import EmailMessage, send_mail

# Create your views here.
def home(request):
    return render(request, 'home.html')

def homelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        remember = request.POST.get('remember-me', None)
        if remember:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged In Successfully.")
                return redirect('/')
            else:
                messages.error(request, "Account is not activated, Please check your email for activation link or contact admin to activate your accunt.")
                return redirect('/')
        else:
            # check if the user exists
            try:
                User.objects.get(username=username)
                messages.error(request, "Wrong Password, Try Again Or You Can Reset Password.")
                return redirect('/')
            except User.DoesNotExist:
                messages.error(request, "Wrong Username Or Account DoesNot Exist.")
                return redirect('/')

def homesignup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('email')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if not all([firstname, lastname, username, email, pass1, pass2]):
            messages.error(request, "All fields are required.")
            return redirect('/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords did not match.")
            return redirect('/')

        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = firstname.upper()
        user.last_name = lastname.upper()
        user.save()

        # Email Address Confirmation Email
        # current_site = get_current_site(request)
        # email_subject = "KWETU WELCOME AND ACCOUNT CONFIRMATION"
        # message = render_to_string('email_confirmation.html', {
        #    'name': user.first_name,
        #    'domain': current_site.domain,
        #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #    'token': generate_token.make_token(user)
        # })
        # email = EmailMessage(
        #    email_subject,
        #    message,
        #    settings.EMAIL_HOST_USER,
        #    [user.email],
        # )
        # email.fail_silently = True
        # email.send()
        messages.info(request, "KWETU ACCOUNT CREATED. Please check your email to activate your account.")
        return redirect('/')

    return render(request, 'home.html')

def profile(request):
    context = {
        'user' : request.user,
    }
    return render(request, 'profilemodal.html', 'includes/header.html', context)

def updateprofile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Kwetu Account Profile Has Been Update Successfully.")
            return redirect('/')
        else:
            messages.error(request, "Sorry, your account update failed. Please try again later.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'home.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "KWETU ACCOUNT HAS BEEN SUCCESSFULLY ACTIVATED, PLEASE LOGIN, THANK YOU.")
        return render(request, 'home.html')
    else:
        messages.info(request, "KWETU ACCOUNT ACTIVATION FAILED, PLEASE TRY AGAIN!")
        return redirect('/')

def about(request):
    context = {
        'Testimonials' : Testimonial.objects.all(),
    }
    return render(request, 'about.html', context)

def add_new_testimonial(request):
    if request.method == 'POST':
        tname = request.POST['tname']
        ttitle = request.POST['ttitle']
        testimonial = request.POST['testimonial']

        new_testimonial = Testimonial(tname=tname, ttitle=ttitle, testimonial=testimonial)
        new_testimonial.save()
        messages.success(request, "New Testimonial Has Been Added Successfully.")
        return redirect('/about/')
    else:
        messages.error(request, "Failure To Add New Testimonial, Please Contact Tech Team And Try Again Later.")
        return redirect('/about/')
    
def delete_testimonial(request, testimonialid):
    if testimonialid:
        del_testimonial = Testimonial.objects.filter(id=testimonialid)
        del_testimonial.delete()
        messages.success(request, "Testimonial Deleted Successfully")
        return redirect('/about/')
    else:
        messages.error(request, "Failed To Delete Testimonial, Please Contact Tech Team And Try Again")
        return redirect('/about/')
    
def services(request):
    context = {
        'Services' : Service.objects.all(),
    }
    return render(request, 'services.html', context)

def add_new_service(request):
    if request.method == 'POST':
        simage = request.FILES['simage']
        stitle = request.POST['stitle']
        sdescription = request.POST['sdescription']

        new_service = Service(simage=simage, stitle=stitle, sdescription=sdescription)
        new_service.save()
        messages.success(request, "New Service Has Been Added Successfully.")
        return redirect('/services/')
    else:
        messages.error(request, "Failure To Add New Service, Please Contact Tech Team And Try Again Later.")
        return redirect('/services/')
    
def delete_service(request, serviceid):
    if serviceid:
        del_service = Service.objects.filter(id=serviceid)
        del_service.delete()
        messages.success(request, "Service Deleted Successfully")
        return redirect('/services/')
    else:
        messages.error(request, "Failed To Delete Service, Please Contact Tech Team And Try Again")
        return redirect('/services/')

def team(request):
    context = {
        'TeamMates' : Profile.objects.filter(position="Team Member"),
    }
    return render(request, 'team.html', context)

def upcoming_events(request):
    return render(request, 'events.html')

def past_events(request):
    return render(request, 'past_events.html')

def recorded_events(request):
    return render(request, 'recorded_events.html')

def members(request):
    context={
        'Members': User.objects.all()
    }
    return render(request, 'members.html', context)

def update_member(request):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        position = request.POST['position']

        Profile.objects.filter(user=member_id).update(position=position)
        messages.success(request, "Member Postion Updated Successfully")
        return redirect('/members/')
    else:
        messages.error(request, "Failed To Update Member Postion, Please Contact Tech Team And Try Again Later.")
        return redirect('/members/')

def contact(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_subject = request.POST['contact_subject']
        contact_message = request.POST['contact_message']
        #contact_admin_email = "latrondav@gmail.com"

        # Contact Email

        #subject = contact_subject
        #message = "Hello Vetogro Admin!! \n My name is " + contact_name + "\n" + contact_message + "\n\n Thanking you."
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [contact_admin_email, contact_email]
        #send_mail(subject, message, from_email, to_list, fail_silently=True)

        new_message = Contact(contact_name = contact_name, contact_email = contact_email, contact_subject = contact_subject, contact_message = contact_message)
        if new_message:
            new_message.save()
            messages.success(request, "Message Sent, Thank You For Contacting Kwetu.")
            return redirect('contact')
        else:
            messages.error(request, "Message Failed To Send, Try Again Later")
            return redirect('contact')
    else:
        return render(request, 'contact.html')
