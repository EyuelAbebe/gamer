from django.shortcuts import render


def base(request):
    context = {}
    return render(request, 'chess/base.html', context)


def profile(request, player_id):
    context = {
        'player_id' : player_id,
    }
    return render(request, 'chess/profile.html', context)


def match(request, match_id, wht_id, blk_id):
    context = {
        'match_id' : 1,
        'wht_id' : 1,
        'blk_id' : 1,
    }
    return render(request, 'chess/match.html', context)
