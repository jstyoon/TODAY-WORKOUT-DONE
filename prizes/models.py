from django.db import models
from users.models import User

# Create your models here.

class Prize(models.Model):

    SOURCE_OPTIONS = [
        ('DAY1 WORKOUT DONE','DAY1 WORKOUT DONE'),
        ('DAY2 WORKOUT DONE','DAY2 WORKOUT DONE'),
        ('DAY3 WORKOUT DONE','DAY3 WORKOUT DONE'),
        ('DAY4 WORKOUT DONE','DAY4 WORKOUT DONE'),
        ('DAY5 WORKOUT DONE','DAY5 WORKOUT DONE'),
    ]

    source = models.CharField(choices=SOURCE_OPTIONS,max_length=256)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=256)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return str(self.owner)+'의 prize'