from .models import Genres


def get_user(request):
    genres = Genres.objects.all()
    if request.session.has_key('user'):
        return {'user_session': request.session['user'],'genres_list_context': genres}
    else:
        return {'user_session': None,'genres_list_context': genres}
