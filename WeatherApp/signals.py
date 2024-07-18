from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ImageModel

@receiver(pre_save, sender=ImageModel)
def before_saving_image(sender, instance, **kwargs):
    
    print("Pre-save signal triggered for image")
    
    instance.title = instance.title.title()

@receiver(post_save, sender=ImageModel)
def after_saving_image(sender, instance, created, **kwargs):
    if created:
        print("Post-save signal triggered - new image instance created")
    else:
        print("Post-save signal triggered - image instance updated")
    
