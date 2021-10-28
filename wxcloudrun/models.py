from datetime import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=64, default='')
    age = models.IntegerField(default=0)
    email = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=128, default='')
    create_time = models.DateTimeField(default=datetime.now(), )
    update_time = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
