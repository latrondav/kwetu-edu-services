from django.db.models import Q
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

        messages.success(request, "Kwetu Account Created. Please check your email to activate your account.")
        return redirect('/')
    else:
        messages.error(request, "Failed To Create Kwetu Account, Please Try Again Later Or Contact Tech Team.")
        return render(request, 'home.html')

def profile(request):
    context = {
        'user' : request.user,
    }
    return render(request, 'profilemodal.html', 'includes/header.html', context)

def update_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        profile.contact = request.POST.get('contact')
        profile.bio = request.POST.get('bio')
        profile.twitter = request.POST.get('twitter')
        profile.facebook = request.POST.get('facebook')
        profile.instagram = request.POST.get('instagram')
        profile.linkedin = request.POST.get('linkedin')

        image = request.FILES.get('image')
        if image:
            profile.image = image

        if user.email != new_email:
            user.email = new_email
            user.username = new_email
            user.is_active = False
            user.save()
            profile.save()

            # send email to the new email address for reactivation
            current_site = get_current_site(request)
            email_subject = "KWETU REACTIVATION EMAIL"
            message = render_to_string('email_reactivation.html', {
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

            logout(request)
            messages.success(request, 'Your Profile And New Email Address Have Been Updated Hence Deactivating Your Account Until New Email Is Confirmed. Please Check Your New Email To Reactivate Your Account.')
            return redirect('/')
        else:
            user.save()
            profile.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('/')
    else:
        messages.error(request, "Sorry, your account profile update failed. Please Contact Admin And try again later.")
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
        messages.success(request, "Kwetu Account Has Been Successfully Activated, Please Proceed To Login, Thank You.")
        return redirect('/')
    else:
        messages.info(request, "Kwetu Account Activation Failed, Please Contact Tech Team And Try Again.")
        return redirect('/')
    
def reactivate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Kwetu Account Has Been Successfully Re-Activated, Please Proceed To Login, Thank You.")
        return redirect('/')
    else:
        messages.info(request, "Kwetu Account Re-Activation Failed, Please Contact Tech Team And Try Again.")
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

def add_event(request):
    if request.method == 'POST':
        eimage = request.FILES.get('eimage')
        ename = request.POST.get('ename')
        edate = request.POST.get('edate')
        etime = request.POST.get('etime')
        edescription = request.POST.get('edescription')
        elink = request.POST.get('elink')

        event = Event(eimage=eimage, ename=ename, edate=edate, etime=etime, edescription=edescription, elink=elink)
        try:
            event.save()
            messages.success(request, 'Event Successfully Added.')
            return redirect('/uevents/')
        except:
            messages.error(request, 'Failed To Add Event. Please Contact Tech Team And Try Again Later.')
            return redirect('/uevents/')
    else:
        return render(request, 'upcoming_event.html')

def upcoming_events(request):
    context = {
        'UEvents': Event.objects.filter(Q(edate__gte=datetime.date.today()) | Q(edate=datetime.date.today(), etime__gte=datetime.datetime.now().time())),
    }
    return render(request, 'upcoming_events.html', context)

def update_upcoming_event(request, ueventid):
    uevent = Event.objects.get(id=ueventid)
    if request.method == 'POST':
        uevent.ename = request.POST['ename']
        uevent.edescription = request.POST['edescription']
        uevent.elink = request.POST['elink']

        if request.FILES.get('eimage'):
            uevent.eimage = request.FILES.get('eimage')

        if request.POST['edate']:
            uevent.edate = request.POST['edate']

        if request.POST['etime']:
            uevent.etime = request.POST['etime']

        try:
            uevent.save()
            messages.success(request, 'Upcoming Event Updated Successfully.')
            return redirect('/uevents/')
        except:
            messages.error(request, 'Failed To Update Upcoming Event, Please Contact Tech Team And Try Again Later.')
            return redirect('/uevents/')
    else:
        return render(request, 'upcoming_events.html')

def delete_upcoming_event(request, ueventid):
    try:
        event = Event.objects.get(id=ueventid)
        event.delete()
        messages.success(request, "Upcoming Event Deleted Successfully")
        return redirect('/uevents/')
    except:
        messages.error(request, "Upcoming Event Deletion Failed, Please Contact Tech Team And Try Again Later.")
        return redirect('/uevents/')

def past_events(request):
    context = {
        'PEvents': Event.objects.filter(Q(edate__lt=datetime.datetime.now().date()) | Q(edate=datetime.datetime.now().date(), etime__lt=datetime.datetime.now().time()))
    }
    return render(request, 'past_events.html', context)

def update_past_event(request, peventid):
    pevent = Event.objects.get(id=peventid)
    if request.method == 'POST':
        pevent.epytlink = request.POST.get('epytlink')

        if request.FILES.get('eparlink'):
            pevent.eparlink = request.FILES.get('eparlink')
    
        try:
            pevent.save()
            messages.success(request, 'Past Event Updated Successfully.')
            return redirect('/pevents/')
        except:
            messages.error(request, 'Failed To Update Past Event, Please Contact Tech Team And Try Again Later.')
            return redirect('/pevents/')
    else:
        return render(request, 'past_events.html')

def delete_past_event(request, peventid):
    try:
        event = Event.objects.get(id=peventid)
        event.delete()
        messages.success(request, "Past Event Deleted Successfully")
        return redirect('/pevents/')
    except:
        messages.error(request, "Past Event Deletion Failed, Please Contact Tech Team And Try Again Later.")
        return redirect('/pevents/')

def members(request):
    context={
        'Members': User.objects.all()
    }
    return render(request, 'members.html', context)

def update_member(request):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        position = request.POST['position']

        profile = Profile.objects.get(user=member_id)
        profile.position = position
        profile.save()

        messages.success(request, "Member Position Updated Successfully")
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
        try:
            new_message.save()
            messages.success(request, "Message Sent, Thank You For Contacting Kwetu.")
            return redirect('/contact/')
        except:
            messages.error(request, "Message Failed To Send, Try Again Later")
            return redirect('/contact/')
    else:
        return render(request, 'contact.html')
