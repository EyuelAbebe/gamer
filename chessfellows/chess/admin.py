from django.contrib import admin
from chess.models import Match, Player, Logedin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ('white',
                    'black',
                    'date_played',
                    'winner',
                    'moves',
                    "white_turn",
                    "pk",
                    "current_state",)

    list_filter = ('date_played',)



class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = ('user',
                    'reg_rating',
                    'reg_wins',
                    'reg_losses',
                    'reg_draws',
                    'bl_rating',
                    'bl_wins',
                    'bl_losses',
                    'bl_draws',
                    'bu_rating',
                    'bu_wins',
                    'bu_losses',
                    'bu_draws',
                    'photo')

    search_fields = ['user']


class PlayerInLine(admin.StackedInline):
    model = Player


class UserAdmin(UserAdmin):
    inlines = (PlayerInLine, )


class LogedinAdmin(admin.ModelAdmin):
    model = Logedin
    list_display = ('player',)


admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Logedin, LogedinAdmin)
