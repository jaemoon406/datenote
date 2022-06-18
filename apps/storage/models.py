from django.db import models


# Create your models here.
class BoardImage(models.Model):
    board = models.ForeignKey('book.board', on_delete=models.CASCADE)
    path = models.ImageField()
