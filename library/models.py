from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    status_choices = (('Reading', 'Reading'),
                      ('Completed', 'Completed'),
                      ('Stopped', 'Stopped'),
                      ('Available', 'Available'),)
    type_choices = (('Soft copy', 'Soft copy'),
                    ('Hard copy', 'Hard copy'),)
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edition = models.CharField(max_length=20, blank=True, default='N/A')
    author = models.CharField(max_length=100)
    rating = models.FloatField(null=True, blank=True)
    added = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,
                              choices=status_choices,
                              default='Reading')
    type = models.CharField(max_length=15,
                            choices=type_choices,
                            default='Hard copy')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-added']

    def total_books(self):
        return Book.objects.all().count()
