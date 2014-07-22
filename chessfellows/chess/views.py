from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from chess.models import Player, Match
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


def home_page(request):
    return render_to_response('user_profile/home_page.html',
                              context_instance={})

def history_page(request):
    return render_to_response('user_profile/history_page.html',
                              context_instance={})

def logout_page(request):
    pass

def profile_page(request):
    "Returns profile page for a logged in user."
    player = get_object_or_404(Player, user=request.user)
    rating = player.rating
    wins = player.wins
    losses = player.losses
    draws = player.draws
    games_played = wins + losses + draws
    photo = player.photo
    user_ = get_object_or_404(User, pk=request.user.id)
    Session['username'] = user_.username
    context = RequestContext(request, {'player': player,
                                       'user': user_,
                                       'rating': rating,
                                       'wins': wins,
                                       'losses': losses,
                                       'total': games_played,
                                       'photo': photo
                                       })
    return render_to_response('user_profile/profile.html',
                              context_instance=context)
