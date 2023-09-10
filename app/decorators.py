from functools import wraps
from flask import abort, current_app, request
from flask_login import current_user


def check_admin(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.email != current_app.config['ADMIN_EMAIL']:
            return abort(404)
        return f(*args, **kwargs)

    return decorated_view
