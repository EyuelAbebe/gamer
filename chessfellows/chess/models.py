import os
from django.db import models
from django.contrib.auth.models import User


def get_file_owner_username(instance, filename):
    parts = [instance.user.username]
    parts.append(os.path.basename(filename))
    path = u"/".join(parts)
    return path


class Match(models.Model):
    white = models.ForeignKey(User, related_name="White")
    black = models.ForeignKey(User, related_name="Black")
    moves = models.TextField()
    date_played = models.DateTimeField(auto_now=True, blank=True)
    winner = models.CharField(max_length=10, default='white')


class Player(models.Model):
    user = models.OneToOneField(User)
    rating = models.PositiveSmallIntegerField(default=1200)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    matches = models.ManyToManyField(Match, related_name="Player", blank=True)
    all_opponents_rating = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to=get_file_owner_username,
                              blank=True)

    def update_all_opponents_rating(self, other):
        self.all_opponents_rating += other.rating

    def calc_rating(self):
        numerator = (self.all_opponents_rating + 400 * (self.wins - self.losses))
        denom = self.wins + self.losses + self.draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator // denom

    def save(self, *args, **kwargs):
        self.rating = self.calc_rating()
        super(Player, self).save(*args, **kwargs)
