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
                                       'color': colors, 'quantity': quantity, 'image': product.image_1,
                                       'colors': product.colors, 'stock': product.stock}}
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


@cart.route('/items')
def get_items():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    grand_subtotal = 0
    discount = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        grand_subtotal += float(product['price']) * int(product['quantity'])
        grand_subtotal -= (discount * int(product['quantity']))

    return render_template('cart/show_items.html', grand_subtotal=grand_subtotal)


@cart.route('/update_cart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash(f"Item {item['name']} is updated", "success")
                    return redirect(url_for('.get_items'))
        except Exception as e:
            print(e)
            return redirect(url_for('.get_items'))
