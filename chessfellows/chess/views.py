from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, HttpResponseRedirect
from .models import Player, Match
from django.contrib.auth.models import User
from .forms import PlayerForm, UserForm, SignUpForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
import django.dispatch


def Login(request):

    if request.user.is_authenticated():
       return HttpResponseRedirect(reverse('profile'))

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user_ = authenticate(username=username, password=password)
        if user_ is not None:
            login(request, user_)

            return HttpResponseRedirect(reverse('home'))


    return HttpResponseRedirect(reverse('auth_login'))


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success/')
    args = {}
    args.update(csrf(request))
    args['form'] = SignUpForm()
    print args
    return render(request, 'register.html', args)


def landing(request):
    sign_up_form = SignUpForm()
    return render(request, 'chess/landing.html', locals(), context_instance=RequestContext(request))


def home_page(request):
    all_players = Player.objects.all()
    return render_to_response('user_profile/home_page.html',
                              locals(),
                              context_instance=RequestContext(request))


def history_page(request):
    return render_to_response('user_profile/history_page.html',
                              context_instance=RequestContext(request))


def update_user(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:

        form = UserForm(instance=request.user)

    return HttpResponseRedirect('/accounts/home/')


def update_player(request):
    player = get_object_or_404(Player, user=request.user)
    import pdb; pdb.set_trace()
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)

        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=request.user)

    return HttpResponseRedirect('/accounts/home/')


def profile_page(request):
    """Returns profile page for a logged in user."""


    user_ = request.user
    player = get_object_or_404(Player, user=user_)
    user_form = UserForm(instance=user_)
    player_form = PlayerForm(instance=player)
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
                              locals(),
                              context_instance=context)
