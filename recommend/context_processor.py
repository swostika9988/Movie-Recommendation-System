def get_user(request):
    if request.session.has_key('user'):
        return {'user_session': request.session['user']}
    else:
        return {'user_session': None}
