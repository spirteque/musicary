from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .token import account_activation_token
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            
            profile = Profile.objects.create(user=new_user)
            
            current_site = get_current_site(request)
            mail_subject = 'Link aktywacyjny do konta Musicary'
            message = render_to_string('account/register_conf_email.html',{
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user)
            })
            
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, 
                                 message, 
                                 to=[to_email])
            email.send()
            
            return render(request,
                          'account/register_act_link_send.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/register_succes.html')
    else:
        return render(request, 'account/register_error.html')
    

# TODO take query parameter from url and mark znajomi or kanał główny as focus
# ?views=friends / ?views=main_channel
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard',})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                     'profile_form': profile_form})