# from django.db import models
# from django.contrib.auth.models import User


# class Player(models.Model):
#     user = models.OneToOneField(User)
#     rating = models.PositiveSmallIntegerField()
#     wins = models.PositiveIntegerField()
#     losses = models.PositiveIntegerField()
#     matches = models.ManyToManyField()


# class Match(models.Model):
#     white = models.ForiegnKey('Player')
#     black = models.ForiegnKey('Player')
#     moves = models.TextField()
