import secrets

import pdfkit
import stripe
from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required

from .. import db
from ..models import CustomerOrder, User
from . import order


def delete_unnecessary():
    for key,product in session['Shoppingcart']:
        session.modified = True
        del product['image']
        del product['colors']
    return delete_unnecessary


@order.route('/payment', methods=['POST'])
def payment():
    return redirect(url_for('thanks'))

@order.route('/thanks')
def thanks():
    pass


@order.route('/get_order')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        delete_unnecessary()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('.get_invoice', invoice=invoice))

        except Exception as e:
            print(e)
            flash('Something went wrong', 'danger')
            return redirect(url_for('cart.get_items'))


@order.route('/<invoice>')
def get_invoice(invoice):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    customer_id = current_user.id
    order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()

    if not order:
        flash("No order found.", "info")
        return redirect(url_for('main.home_page'))

    grand_subtotal = ('%.2f' % sum(
        (float(product['price']) - (product['discount'] / 100) * float(product['price'])) * int(product['quantity'])
        for product in order.orders.values()
    ))
    amount_for_stripe = int(float(grand_subtotal) * 100)

    return render_template('order/order.html', invoice=invoice, customer=current_user, orders=order,
                            grand_total=0, subtotal=0, grand_subtotal=grand_subtotal,amount_for_stripe=amount_for_stripe)


@order.route('/decline/<invoice>', methods=['POST'])
def delete_invoice(invoice):
    order = CustomerOrder.query.filter_by(invoice=invoice).first()
    if not order:
        flash("Sorry, there's no such order", 'danger')
        return redirect(url_for('.get_invoice', invoice=invoice))
    db.session.delete(order)
    db.session.commit()
    flash(f'The order {order.invoice} was successfully declined', 'success')
    return redirect(url_for('main.home_page'))


@order.route('/get_pdf/<invoice>', methods=['POST'])
def get_pdf(invoice):
    if not current_user.is_authenticated:
        return redirect(url_for('.get_order'))

    customer_id = current_user.id
    order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()

    if not order:
        flash("No order found.", "info")
        return redirect(url_for('.get_order'))

    grand_subtotal = sum(
        (float(product['price']) - (product['discount'] / 100) * float(product['price'])) * int(product['quantity'])
        for product in order.orders.values()
    )

    path_to_wkhtmptopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmptopdf)
    rendered = render_template('order/pdf_order.html', invoice=invoice, customer=current_user, orders=order,
                                subtotal=0, grand_total=0, grand_subtotal=grand_subtotal)
    pdf = pdfkit.from_string(rendered, False, configuration=config, options={"enable-local-file-access": ""})
    response = make_response(pdf)
    response.headers['content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = f'inline; filename="{invoice}.pdf"'
    return response


