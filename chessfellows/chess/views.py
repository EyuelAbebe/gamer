from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from chess.models import Player, Match
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from board import Board


def landing(request):
    context = {}
    return render(request, 'chess/landing.html', context)


@csrf_exempt
def home_page(request):
    chess_board = Board()
    for i in request.POST:
        print request.POST[i]
        chess_board.set_board(request.POST[i])
    print chess_board.board
    return render_to_response('user_profile/home_page.html',
                              context_instance={})


def history_page(request):
    return render_to_response('user_profile/history_page.html',
                              context_instance={})


def profile_page(request):
    """Returns profile page for a logged in user."""

    user_ = get_object_or_404(User, pk=request.user.id)
    player = get_object_or_404(Player, user=request.user)
    player_info = {'age': player.age,
                   'country': player.country,
                   'photo': player.photo,
                   'date' : player.date_joined}
    regular = {'rating': player.reg_rating,
               'wins': player.reg_wins,
               'losses': player.reg_losses,
               'draws': player.reg_draws,
               'total': player.reg_wins + player.reg_losses + player.reg_draws
    }
    blitz = {'rating': player.bl_rating,
             'wins': player.bl_wins,
             'losses': player.bl_losses,
             'draws': player.bl_losses,
             'total': player.bl_wins + player.bl_losses + player.bl_draws
    }
    bullet = {'rating': player.bu_rating,
              'wins': player.bu_wins,
              'losses': player.bu_losses,
              'draws': player.bu_losses,
              'total': player.bu_wins + player.bu_losses + player.bu_draws
    }
    context = RequestContext(request, {'regular': regular,
                                       'blitz': blitz,
                                       'bullet': bullet,
                                       'user': user_,
                                       'player': player_info
                                       })
    return render_to_response('user_profile/profile.html',
                              context_instance=context)

