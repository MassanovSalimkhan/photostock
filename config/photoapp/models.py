from django.db import models

from django.contrib.auth import get_user_model

from imagekit.models import ImageSpecField

from imagekit.processors import ResizeToFill


class Photo(models.Model):

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250) 

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photoapp/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(350, 200)],
                                      format='JPEG',
                                      options={'quality': 500})

    

    def __str__(self):
        return self.title

