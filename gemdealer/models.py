from django.db import models


class Deals(models.Model):
    customer = models.CharField(max_length=100, null=False)
    item = models.CharField(max_length=50, null=False)
    total = models.IntegerField()
    quantity = models.IntegerField(null=False)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer} buy {self.quantity} {self.item}"
