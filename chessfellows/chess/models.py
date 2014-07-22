import os
from django.db import models
from django.contrib.auth.models import User

game_type_choices = ((0, 'Regular'), (1, 'Bullet'), (2, 'Bullet'))


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
    game_type = models.IntegerField(choices=game_type_choices)

    def __unicode__(self):
        return self.game_type


class Player(models.Model):
    user = models.OneToOneField(User)
    reg_rating = models.DecimalField(
        default=1200.00,
        max_digits=6,
        decimal_places=2
        )
    reg_wins = models.PositiveIntegerField(default=0)
    reg_losses = models.PositiveIntegerField(default=0)
    reg_draws = models.PositiveIntegerField(default=0)
    bl_rating = models.DecimalField(
        default=1200.00,
        max_digits=6,
        decimal_places=2
        )
    bl_wins = models.PositiveIntegerField(default=0)
    bl_losses = models.PositiveIntegerField(default=0)
    bl_draws = models.PositiveIntegerField(default=0)
    bu_rating = models.DecimalField(
        default=1200.00,
        max_digits=6,
        decimal_places=2
        )
    bu_wins = models.PositiveIntegerField(default=0)
    bu_losses = models.PositiveIntegerField(default=0)
    bu_draws = models.PositiveIntegerField(default=0)
    matches = models.ManyToManyField(Match, related_name="Player", blank=True)
    all_opponents_rating = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to=get_file_owner_username,
                              default='http://lh5.googleusercontent.com/-b0-k99FZlyE/AAAAAAAAAAI/AAAAAAAAAAA/twDq00QDud4/s120-c/photo.jpg',
                              blank=True)

    def __unicode__(self):
        return self.user.username

    def update_all_opponents_rating(self, other):
        self.all_opponents_rating += other.rating

    def calc_reg_rating(self):
        numerator = (self.all_opponents_rating + 400 * (self.reg_wins - self.reg_losses))
        denom = self.reg_wins + self.reg_losses + self.reg_draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator / denom

    def calc_bl_rating(self):
        numerator = (self.all_opponents_rating + 400 * (self.bl_wins - self.bl_losses))
        denom = self.bl_wins + self.bl_losses + self.bl_draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator / denom

    def calc_bu_rating(self):
        numerator = (self.all_opponents_rating + 400 * (self.bu_wins - self.bu_losses))
        denom = self.bu_wins + self.bu_losses + self.bu_draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator / denom

    def save(self, *args, **kwargs):
        self.reg_rating = self.calc_reg_rating()
        self.bl_rating = self.calc_bu_rating()
        self.bu_rating = self.calc_bl_rating()
        super(Player, self).save(*args, **kwargs)
