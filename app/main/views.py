from . import main
from flask import render_template
from flask import session


@main.route('/', methods=['GET'])
def hello():
    print(session.items())
    return 'Hello world'
