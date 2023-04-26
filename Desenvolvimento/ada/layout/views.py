from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

@login_required
def home(request):
    trans = translate(language='pt-br')
    return render(request, "home.html", {'trans': trans})

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('Password')
        text = gettext('login')
        text = gettext('English')
        text = gettext('Português Brasileiro') #identifica o que mudar
    finally:
        activate(cur_language)
    return text