from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d',
                              blank=True)
    
    private_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Profil {self.user.username}'
    

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='follow_from_set',
                                  on_delete=models.CASCADE)
    
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='follow_to_set',
                                on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    def __str__(self):
        return f'{self.user_from} obserwuje {self.user_to}'


User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))