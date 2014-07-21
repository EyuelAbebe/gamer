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
    date_played = models.DateTimeField(auto_now=True)


class Player(models.Model):
    user = models.OneToOneField(User)
    rating = models.PositiveSmallIntegerField(default=1200)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    matches = models.ManyToManyField(Match, related_name="Player")
    all_opponents_rating = models.PositiveIntegerField(default=0)
    image_upload_folder = 'photos/'
    photo = models.ImageField(upload_to=image_upload_folder,
                              height_field='height',
                              width_field='width')

    def update_all_opponents_rating(self, other):
        self.all_opponents_rating += other.rating

    def calc_rating(self):
        numerator = (self.opponents_rating + 400 * (self.wins - self.losses))
        denom = self.wins + self.losses + self.draws
        return numerator // denom

    def save(self, *args, **kwargs):
        opponent = Match.objects.filter()
        self.update_all_opponents_rating(opponent)
        self.rating = self.calc_rating()
        super(Player, self).save(*args, **kwargs)
