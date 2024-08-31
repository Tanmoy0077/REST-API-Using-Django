from django.db import models

class User(models.Model):
    staff_code = models.IntegerField()
    name = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    facility = models.CharField(max_length=20)

    def __str__(self):
        return self.name