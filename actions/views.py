from actions.models import Action
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType



@login_required
def show_notifications(request):
    actions = Action.objects.all().exclude(user=request.user)

    user_type = ContentType.objects.get(model='user')
    post_type = ContentType.objects.get(model='post')
    
    posts_id = [post.id for post in request.user.posts_created.all()]
    
    actions = actions.filter(target_ct=user_type, target_id=request.user.id) | actions.filter(target_ct=post_type, target_id__in=posts_id)
    actions = actions[:20]
            
    return render(request, 'actions/notifications.html', {'actions': actions})


@login_required
def show_activity(request):
    actions = Action.objects.all().filter(user=request.user)

    user_type = ContentType.objects.get(model='user')
    post_type = ContentType.objects.get(model='post')
    
    
    actions = actions.filter(target_ct=user_type) | actions.filter(target_ct=post_type)
    actions = actions[:20]
    
    print(actions)
    return render(request, 'actions/activity.html', {'actions': actions})