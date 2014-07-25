__author__ = 'eyuelabebe'

from django.contrib.auth.models import User
from .models import Player
from django.db.models.signals import post_init
from django.dispatch import receiver


# # @receiver(post_save, sender=User)
# def create_profile(sender, **kwargs):
#     import pdb; pdb.set_trace()
#     user_ = kwargs['instance']
#     p = Player(user=user_)
#
#     p.save()
#
# post_init.connect(create_profile, sender=User)




