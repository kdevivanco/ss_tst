from functools import wraps
from flask import session, redirect, flash


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            flash('You dont have access to this part of the site', 'error')
            return redirect('/')
        resp = route(*args, **kwargs)
        return resp
    
    return wrapper
