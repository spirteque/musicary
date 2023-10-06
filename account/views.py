from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from main.forms import SearchForm
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, UserPasswordChangeForm, DeleteAccountForm, ProfilePrivacyEditForm
from .token import account_activation_token
from .models import Profile
from posts.models import Post
from common.decorators import is_ajax


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
            email = EmailMessage(subject=mail_subject, 
                                 body=message,
                                 from_email=settings.EMAIL_SENDER,
                                 to=[to_email])
            email.send()
            
            return render(request, 'account/register_act_link_send.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


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
        return render(request, 'account/register_link_error.html')
    

@login_required
def dashboard(request, action=None):
    user = request.user
    friends = user.following.all()
    posts = Post.objects.filter(author__in=friends) | Post.objects.filter(author=request.user)[:50]
    
    search_form = SearchForm()
    
    if action == 'all':        
        posts = Post.objects.filter(author__profile__private_mode=False)[:50]

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request, 'account/user/profile_ajax_list.html', {'user': user,
                                                                       'posts': posts})
    
    return render(request, 'account/dashboard.html', {'user': user,
                                                      'posts': posts,
                                                      'action': action,
                                                      'form': search_form})


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
            messages.success(request, 'Uaktualnienie profilu zakończyło się sukcesem.')
        else:
            messages.error(request, 'Wystąpił błąd podczas uaktualniania profilu.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit/edit_account.html', {'user_form': user_form,
                                                         'profile_form': profile_form})
    

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change")
    success_message = 'Zmiana hasła zakończyła się sukcesem.'

@login_required
def edit_privacy(request):
    if request.method =='POST':
        form = ProfilePrivacyEditForm(instance=request.user,
                                      data=request.POST)        
        if form.is_valid():
            private_mode = form.cleaned_data['private_mode']
            request.user.profile.private_mode = private_mode
            request.user.profile.save()
            messages.success(request, 'Zmiana ustawień prywatności zakończyła się sukcesem')
        else:
            messages.error(request, 'Wystąpił błąd podczas zmiany ustawień prywatności.')
    else:
        if request.user.profile.private_mode:
            form = ProfilePrivacyEditForm(data={'private_mode': ['on']})
        else:
            form = ProfilePrivacyEditForm()
    return render(request, 'account/edit/edit_privacy.html', {'form': form})
    

@login_required
def delete_profile_photo(request):
    photo = request.user.profile.photo
    photo.delete()
    if photo:
        messages.error(request, 'Nie udało się usunąć zdjęcia profilowego.')
    else:
        messages.success(request, 'Zdjęcie profilowe zostało usunięte.')
    return redirect('edit_account')


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            
            current_site = get_current_site(request)
            mail_subject = 'Link potwierdzający usunięcie konta na portalu Musicary'
            message = render_to_string('account/edit/delete_conf_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
                    
            to_email = user.email
            email = EmailMessage(subject=mail_subject, 
                                body=message,
                                from_email=settings.EMAIL_SENDER,
                                to=[to_email])
            email.send()
            
            return render(request, 'account/edit/delete_act_link_send.html', {'user': user})
    else:
        form = DeleteAccountForm()
    return render(request, 'account/edit/delete_account.html', {'form': form})
    

@login_required
def delete_account_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.delete()
        return redirect('home')
    else:
        return render(request, 'account/edit/delete_account_error.html')
      

@login_required
def user_profile(request, username, action=None):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    posts = Post.objects.filter(author=user)
    
    if action == 'tagged':
        posts = user.tagged_in.all()
    
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request, 'account/user/profile_ajax_list.html', {'user': user,
                                                                       'posts': posts})    
    return render(request, 'account/user/profile_posts.html', {'user': user,
                                                               'posts': posts,
                                                               'action': action})
    
@login_required
def followers_list(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    followers = user.followers.filter(is_active=True)
    
    return render(request, 'account/user/followers_list.html', {'followers': followers,
                                                                'user': user})
    
@login_required
def following_list(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    followings = user.following.filter(is_active=True)
    
    return render(request, 'account/user/following_list.html', {'followings': followings,
                                                                'user': user})

@login_required
@require_POST
def toggle_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                user.followers.add(request.user)
            else:
                user.followers.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})



