from django.conf import settings
from django.db import models


# Create your models here.
class Income(models.Model):

    SOURCE_OPTIONS = [
        ("SALARY", "SALARY"),
        ("BUSSINESS", "BUSSINESS"),
        ("SIDE-HUSTLES", "SIDE-HUSTLES"),
        ("OTHERS", "OTHERS"),
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    description = models.TextField()
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.owner) + "'s expense"
