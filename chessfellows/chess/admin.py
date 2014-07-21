from django.contrib import admin
from chess.models import Match, Player
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class MatchAdmin(admin.ModelAdmin):

    list_display = ('white',
                    'black',
                    'date_played',
                    'winner')

    list_filter = ('date_played',)


class PlayerAdmin(admin.ModelAdmin):

    model = Player
    list_display = ('user',
                    'rating',
                    'wins',
                    'losses',
                    'draws',
                    'photo')

    search_fields = ['user']


class PlayerInLine(admin.StackedInline):
    model = Player

class UserAdmin(UserAdmin):
    inlines = (PlayerInLine, )

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)