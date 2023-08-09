from django.shortcuts import render


def exchange(request):
    if request.method == 'GET':
        return render(request, 'exchange/exchange.html')