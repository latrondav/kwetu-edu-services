from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from kwetuproject import settings
from . token import generate_token
from . forms import ProfileForm
from . models import Profile, Contacts
from django.core.mail import EmailMessage, send_mail

# Create your views here.
def home(request):
    return render(request, 'home.html')

def homelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        try:
            remember = request.POST['remember-me']
            if remember:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        except:
            is_private = False
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

        if user is not None:
            login(request, user)
            messages.success(request, "LOGGED IN SUCCESSFULLY!")
        else:
            messages.error(request, "BAD CREDENTIALS")
            return redirect('/')

    return render(request, 'home.html')

def homesignup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Student number already exist! Please use your student number, thank you.")
            return redirect('/')

        if len(username)>10:
            messages.error(request, "Student number must only be under 10 characters")
            return redirect('/')

        if not username.isnumeric():
            messages.error(request, "Student number must only be Numeric!")
            return redirect('/')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('/')

        user = User.objects.create_user(username, email, pass1)
        user.first_name = firstname.upper()
        user.last_name = lastname.upper()
        user.is_active = False
        user.save()

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "KWETU WELCOME AND ACCOUNT CONFIRMATION"
        message = render_to_string('email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()
        messages.info(request, "KWETU ACCOUNT CREATED, NOW TO LOGIN, PLEASE CHECK YOUR EMAIL TO ACTIVATE ACCOUNT.")
        return redirect('/')

    return render(request, 'home.html')

def profile(request):
    context = {
        'user' : request.user,
        'Profile' : request.Profile
    }
    return render(request, 'profilemodal.html', 'includes/header.html', context)

def updateprofile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "YOUR KWETU ACCOUNT PROFILE HAS BEEN UPDATED SUCCESSFULLY")
            return redirect('/')
        else:
            messages.error(request, "SORRY, KWETU ACCOUNT UPDATE FAILED, TRY AGAIN LATERf")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "home.html")

def signout(request):
    logout(request)
    messages.success(request, "LOGGED OUT SUCCESSFULLY!")
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
    kwetu_members = User.objects.all()

    context={
        'kwetu_members': kwetu_members
    }
    
    return render(request, 'members.html', context)

def contact(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_subject = request.POST['contact_subject']
        contact_message = request.POST['contact_message']

        new_message = Contacts(contact_name = contact_name, contact_email = contact_email, contact_subjectt = contact_subject, contact_message = contact_message)
        new_message.save()
        messages.success(request, "MESSAGE SENT, THANK YOU FOR CONTACTING KWETU")

    return render(request, 'contact.html')
