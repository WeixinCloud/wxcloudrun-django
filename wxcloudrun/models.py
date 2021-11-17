from datetime import datetime

from django.db import models


# Create your models here.
class ToDoList(models.Model):
    id = models.AutoField
    title = models.CharField(max_length=64, default='')
    status = models.CharField(max_length=64, default='')
    create_time = models.DateTimeField(default=datetime.now(), )
    update_time = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'todo_list' #数据库表名
