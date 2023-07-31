from . import main
from flask import render_template


@main.route('/', methods=['GET'])
def hello():
    return 'Hello world'
