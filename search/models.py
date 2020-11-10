from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

   