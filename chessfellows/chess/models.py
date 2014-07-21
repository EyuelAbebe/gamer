from django.db import models
from django.contrib.auth.models import User


class Match(models.Model):
    white = models.ForeignKey(User, related_name="White")
    black = models.ForeignKey(User, related_name="Black")
    moves = models.TextField()


class Player(models.Model):
    user = models.OneToOneField(User)
    rating = models.PositiveSmallIntegerField(default=1200)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    matches = models.ManyToManyField(Match, related_name="Player")
    opponent_rating = models.PositiveIntegerField(default=0)

    def calc_rating(self):
        numerator = (self.opponent_rating + 400 * (self.wins - self.losses))
        denom = self.wins + self.losses + self.draws
        return numerator // denom

    def save(self, *args, **kwargs):
        self.rating = self.calc_rating()
        super(Player, self).save(*args, **kwargs)
