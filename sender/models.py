from django.db import models


class Chat(models.Model):
    instance_id = models.IntegerField()
    tocken = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
