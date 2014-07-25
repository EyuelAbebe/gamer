import os
from django.db import models
from django.contrib.auth.models import User
# from chessfellows import settings
import datetime
from django.db.models.signals import post_save  # , post_init

game_type_choices = ((0, 'Regular'), (1, 'Bullet'), (2, 'Bullet'))


def create_profile(sender, **kwargs):
    user_ = kwargs['instance']
    try:
        Player.objects.get(user=user_)
    except Player.DoesNotExist:
        p = Player(user=user_)
        p.save()


post_save.connect(create_profile, sender=User)


def get_file_owner_username(instance, filename):
    parts = [instance.user.username]
    parts.append(os.path.basename(filename))
    path = u"/".join(parts)
    return path


class Match(models.Model):
    white = models.ForeignKey(User, related_name="White")
    black = models.ForeignKey(
        User, related_name="Black", blank=True, null=True
        )
    moves = models.TextField(blank=True)
    date_played = models.DateTimeField(auto_now=True, blank=True)
    winner = models.CharField(max_length=10, blank=True)
    game_type = models.IntegerField(choices=game_type_choices, default=0)
    current_move = models.CharField(max_length=5, blank=True)
    current_state = models.CharField(max_length=72, blank=True)
    white_turn = models.BooleanField(default=True)

    def __unicode__(self):
        return self.game_type

    class Meta:
        verbose_name_plural = "Matches"


class Player(models.Model):
    user = models.OneToOneField(User)
    age = models.PositiveIntegerField(max_length=4, default=0)
    country = models.CharField(max_length=10, default='USA')
    date_joined = models.DateTimeField(
        auto_now=True, blank=True, default=datetime.date.today
        )
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
                              blank=True)

    def __unicode__(self):
        return self.user.username

    def update_all_opponents_rating(self, other_player):
        self.all_opponents_rating += other_player.rating

    def calc_reg_rating(self):
        numerator = (
            self.all_opponents_rating + 400 * (self.reg_wins - self.reg_losses)
            )
        denom = self.reg_wins + self.reg_losses + self.reg_draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator / denom

    def calc_bl_rating(self):
        numerator = (
            self.all_opponents_rating + 400 * (self.bl_wins - self.bl_losses)
            )
        denom = self.bl_wins + self.bl_losses + self.bl_draws

        if denom == 0:
            return 1200
        if numerator < 0:
            return 1200

        return numerator / denom

    def calc_bu_rating(self):
        numerator = (
            self.all_opponents_rating + 400 * (self.bu_wins - self.bu_losses)
            )
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
