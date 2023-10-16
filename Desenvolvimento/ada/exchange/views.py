from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# gource
@login_required
def exchange(request):
    if request.method == 'GET':
        return render(request, 'exchange/exchange.html')