from django.template import RequestContext
from django.shortcuts import (
    render_to_response, get_object_or_404, render,
    HttpResponseRedirect, HttpResponse
    )
from .models import Player, Match, Logedin
from .forms import PlayerForm, UserForm, SignUpForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import engine
from django.contrib.auth.models import User
# from django.db.models import Q

loged_in_players = []


def Login(request):

    if request.user.is_authenticated():
        p = Player(user=request.user)
        logged_player = Logedin(player=p)
        logged_player.save()
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
            return HttpResponseRedirect('/register_success/')
    args = {}
    args.update(csrf(request))
    args['form'] = SignUpForm()
    print args
    return render(request, 'registration/registration_form.html', args)


def landing(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    sign_up_form = SignUpForm()
    return render(
        request, 'chess/landing.html', locals(),
        context_instance=RequestContext(request)
        )


def home_page(request):
    all_players = Player.objects.all()
    beginner, intermediate, advanced = [], [], []
    live_games = []
    logged_in_players = Logedin.objects.all()
    all_matches = Match.objects.filter(in_progress__exact=1)
    for user_ in logged_in_players:
        p = Player.objects.get(user=user_)
        if p.reg_rating <= 1200:
            beginner.append(p)
        elif 1201 < p.reg_rating < 1750:
            intermediate.append(p)
        else:
            advanced.append(p)
    return render_to_response('user_profile/home_page.html',
                              locals(),
                              context_instance=RequestContext(request))


def start_table(request):
    black = User.objects.get(pk=3)
    m = Match(white=request.user, black=black)
    m.save()
    return render_to_response(
        'user_profile/start_table.html', context_instance={}
        )


@csrf_exempt
def make_move(request):
    u"""Return state of a match after a move.

    Accept:
    Match id:
    position: Board state as 71 character string.
    move: Proposed move as 5 charcter string

    Instantiate a Match()
    """
    # Convert position from format sent by the front end to format
    # expected by the engine.
    # import pdb; pdb.set_trace()
    pos = request.POST['position']
    pos = pos.replace('2', '11')
    pos = pos.replace('3', '111')
    pos = pos.replace('4', '1111')
    pos = pos.replace('5', '11111')
    pos = pos.replace('6', '111111')
    pos = pos.replace('7', '1111111')
    pos = pos.replace('8', '11111111')
    move = str(request.POST['move'])
    requester = request.user
    # Get match by id
    match_id = 1
    # Get turn from match (Boolean value representing white's move)
    match = Match.objects.get(pk=match_id)
    white_player = match.white
    black_player = match.black
    # print "Requester: {}".format(requester)
    # print "White player: {}\nBlack player: {}".format(
    # white_player, black_player
    # )
    white_turn = match.white_turn
    new_pos = None
    current_pos = match.current_state
    # if black_player is None:
    #     match.black, black_player = requester, requester
    #     match.save()
    if (white_turn and requester == white_player) or \
       (not white_turn and requester == black_player):
        # Instantiate a Match to verify move validity
        if pos != current_pos:
            new_pos = current_pos
        else:
            m = engine.Match()
            new_pos, won = m._play_web(
                pos,
                move,
                white_turn)
            if new_pos != pos:
                move_history = match.moves
                move_history += move + ";"
                match.moves = move_history
                match.current_move = move
                match.white_turn = not white_turn
                match.current_state = new_pos
                match.save()
                # print "saved!"
    elif requester == white_player or requester == black_player:
        new_pos = match.current_state
        # print match.current_state
        # print "elif"
    response = {'moves': new_pos}
    # print new_pos
    return HttpResponse(json.dumps(response), mimetype="application/json")


def history_page(request):
    return render_to_response('user_profile/history_page.html',
                              locals(),
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
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=request.user)
    return HttpResponseRedirect(reverse('home'))


def profile_page(request):
    """Returns profile page for a logged in user."""
    user_ = request.user
    player = get_object_or_404(Player, user=user_)
    user_form = UserForm(instance=user_)
    player_form = PlayerForm(instance=player)
    player_info = {'age': player.age,
                   'country': player.country,
                   'photo': player.photo,
                   'date': player.date_joined}
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
