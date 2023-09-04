from . import main
from flask import render_template
from flask import session, request, flash, redirect, url_for
from ..models import Brand, Category
from .. import db
from .forms import AddProductForm

@main.route('/', methods=['GET'])
def hello():
    print(session.items())
    return 'Hello world'


@main.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        if not getbrand:
            flash('No brand', 'danger')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Brand {getbrand} was added successfully', 'success')
        db.session.commit()
        return redirect(url_for('.addbrand'))

    return render_template('products/addbrand.html', brands='brands')


@main.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if request.method == 'POST':
        getcat = request.form.get('category')
        if not getcat:
            flash('No category', 'danger')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'Cat {getcat} was added successfully', 'success')
        db.session.commit()
        return redirect(url_for('.addcat'))

    return render_template('products/addbrand.html')


@main.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = AddProductForm()
    return render_template('products/addproduct.html',form=form)