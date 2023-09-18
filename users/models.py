from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = CloudinaryField('image')
    bio = models.TextField(default='Hi! I am writing on varshneyblogs',null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # Check if the image field is not set or empty
        if not self.image:
            # Set the default image URL
            default_image_url = 'image/upload/v1693301786/samples/people/boy-snow-hoodie.jpg'  # Replace with your default image URL
            self.image = default_image_url
        super().save(*args, **kwargs)

