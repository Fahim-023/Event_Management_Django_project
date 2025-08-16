from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, blank=True, related_name='rsvp_event')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', null=True, blank=True)


    image = models.ImageField(
        upload_to='events/', 
        default='events/default_event.jpg', 
        blank=True,null=True
    )

    def __str__(self):
        return self.name
