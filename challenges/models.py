from django.db import models
from users.models import User

# Create your models here.

class Challenge(models.Model):

    CATEGORY_OPTIONS = [
        ('DAY1 HUSTLE','DAY1 HUSTLE'),
        ('DAY2 HUSTLE','DAY2 HUSTLE'),
        ('DAY3 HUSTLE','DAY3 HUSTLE'),
        ('DAY4 HUSTLE','DAY4 HUSTLE'),
        ('DAY5 HUSTLE','DAY5 HUSTLE'),
    ]

    category=models.CharField(choices=CATEGORY_OPTIONS,max_length=256)
    amount=models.DecimalField(max_digits=10, decimal_places=2, max_length=256)
    description=models.TextField()
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    date=models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return str(self.owner)+'의 challenge'
        