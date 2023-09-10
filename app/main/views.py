from flask import session

from . import main


@main.route('/', methods=['GET'])
def hello():
    print(session.items())
    return 'Hello world'





"""
@main.route('/check1')
def check1():
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        print('Wow')
        return redirect(url_for('.add_brand'))

    else:
        print('Bruh')
"""



