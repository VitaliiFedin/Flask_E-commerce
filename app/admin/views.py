from . import admin
from flask_login import login_required, current_user
from flask import current_app, abort, render_template, url_for, request, flash, redirect
import secrets
from ..models import Brand, Category, Product
from ..decorators import check_admin
from .. import db, photos
from .forms import AddProductForm
from ..decorators import check_admin


@admin.route('/products')
@login_required
@check_admin
def show_products():
    products = Product.query.all()
    return render_template('products/show-all.html', products=products)


@admin.route('/brands')
@login_required
@check_admin
def get_brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('brands/show-brands.html', brands=brands)


@admin.route('/categories')
@login_required
@check_admin
def get_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('categories/show-categories.html', categories=categories)


@admin.route('edit-brand/<int:id>', methods=['GET', 'POST'])
@login_required
@check_admin
def edit_brand(id):
    edit_brand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        edit_brand.name = brand
        flash('Brand was successfully update', 'success')
        db.session.commit()
        return redirect(url_for('.get_brands'))
    return render_template('brands/edit-brand.html', brand=brand, edit_brand=edit_brand)


@admin.route('edit-category/<int:id>', methods=['GET', 'POST'])
@login_required
@check_admin
def edit_category(id):
    edit_category = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        edit_category.name = category
        flash('Category was successfully update', 'success')
        db.session.commit()
        return redirect(url_for('.get_categories'))
    return render_template('brands/edit-brand.html', category=category, edit_category=edit_category)


@admin.route('/addbrand', methods=['GET', 'POST'])
@login_required
@check_admin
def add_brand():
    if request.method == 'POST':
        get_brand = request.form.get('brand').capitalize()
        check_brand = Brand.query.filter_by(name=get_brand).first()
        if not get_brand:
            flash('No brand ', 'danger')
        if check_brand is not None:
            flash(f'Brand {get_brand} already exist', 'danger')
            return redirect(url_for('.add_brand'))
        else:
            brand = Brand(name=get_brand)
            db.session.add(brand)
            flash(f'Brand {get_brand} was added successfully', 'success')
            db.session.commit()
            return redirect(url_for('.add_brand'))

    return render_template('brands/addbrand.html', brands='brands')


@admin.route('/addcat', methods=['GET', 'POST'])
@login_required
@check_admin
def add_cat():
    if request.method == 'POST':
        get_cat = request.form.get('category').capitalize()
        check_cat = Category.query.filter_by(name=get_cat).first()
        if not get_cat:
            flash('No category', 'danger')
        if check_cat is not None:
            flash(f'The category {get_cat} already exist', 'danger')
            return redirect(url_for('.add_cat'))
        else:
            cat = Category(name=get_cat)
            db.session.add(cat)
            flash(f'Cat {get_cat} was added successfully', 'success')
            db.session.commit()
            return redirect(url_for('.add_cat'))

    return render_template('brands/addbrand.html')


@admin.route('/addproduct', methods=['GET', 'POST'])
@login_required
@check_admin
def add_product():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm()
    if request.method == 'POST':
        check_product = Product.query.filter_by(name=form.name.data).first()
        if check_product is not None:
            flash(f'Product {check_product} is already exist', 'danger')
            return redirect(url_for('.add_product'))
        else:
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            product = Product(name=form.name.data, price=form.price.data, discount=form.discount.data,
                              stock=form.stock.data, colors=form.colors.data, description=form.description.data,
                              brand_id=request.form.get('brand'),
                              category_id=request.form.get('category'), image_1=image_1, image_2=image_2,
                              image_3=image_3
                              )

            flash(f'Product {product.name} was added successfully', 'success')
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('.add_product'))
    return render_template('products/addproduct.html', form=form, brands=brands, categories=categories)
