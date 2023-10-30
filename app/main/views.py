from flask import session, render_template
from ..models import Product
from . import main


@main.route('/', methods=['GET'])
def hello():
    print(session.items())
    products = Product.query.filter(Product.stock > 0)
    return render_template('products/index.html', products=products)





"""
@main.route('/check1')
def check1():
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        print('Wow')
        return redirect(url_for('.add_brand'))

    else:
        print('Bruh')
"""



