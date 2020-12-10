from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,MaxValueValidator
from django.shortcuts import get_object_or_404


def user_diectory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.profile.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    avatar = CloudinaryField('Image')


    def __str__(self):
        return self.user.username

    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()

    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Delivery(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=50,blank=True,null=True)
    delviery_location = models.CharField(max_length=50,blank=True,null=True)
    package_size = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self):
        return self.package_size