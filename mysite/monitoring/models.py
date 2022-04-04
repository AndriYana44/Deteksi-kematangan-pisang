from django.db import models

class Suhu(models.Model):
    suhu = models.FloatField()

    def __float__(self):
        return self.suhu