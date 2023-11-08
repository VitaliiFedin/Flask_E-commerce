from flask import render_template, request, redirect, url_for, flash, session, current_app
from . import cart
from ..models import Product


def merge_dicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@cart.route('/addcart', methods=['POST'])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.referrer and request.method == 'POST':
            dict_items = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount,
                                       'color': colors, 'quantity': quantity, 'image': product.image_1}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('Product exist in a cart ')
                else:
                    session['Shoppingcart'] = merge_dicts(session['Shoppingcart'], dict_items)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = dict_items
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
