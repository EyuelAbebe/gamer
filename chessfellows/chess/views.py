from django.shortcuts import render


def base(request):
    context = {}
    return render(request, 'chess/base.html', context)
