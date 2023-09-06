from . import main
from flask import render_template
from flask import session, request, flash, redirect, url_for
from ..models import Brand, Category, Product
from .. import db, photos
from .forms import AddProductForm
from flask_login import login_required
import secrets


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


@main.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm()
    if request.method == 'POST':
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        product = Product(name=form.name.data, price=form.price.data, discount=form.discount.data,
                          stock=form.stock.data, colors=form.colors.data, description=form.description.data,
                          brand_id=request.form.get('brand'),
                          category_id=request.form.get('category'), image_1=image_1, image_2=image_2, image_3=image_3
                          )

        flash(f'Product {product.name} was added successfully', 'success')
        db.session.add(product)

        db.session.commit()

        return redirect(url_for('.addproduct'))
    return render_template('products/addproduct.html', form=form, brands=brands, categories=categories)


@main.route('/showproduct')
@login_required
def show_products():
    product = Product.query.all()
    return render_template('products/show-all.html', product=product)
