from django.db import models
from django.conf import settings


# Create your models here.
class Income(models.Model):

    SOURCE_OPTIONS = [
        ("SALARY", "SALARY"),
        ("BUSSINESS", "BUSSINESS"),
        ("SIDE-HUSTLES", "SIDE-HUSTLES"),
        ("OTHERS", "OTHERS"),
    ]

    source = models.CharField(max_length=255, choices=SOURCE_OPTIONS)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.owner) + "'s income"
