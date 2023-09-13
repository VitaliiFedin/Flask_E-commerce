import os

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


@admin.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
@check_admin
def edit_product(id):
    brands = Brand.query.all()
    get_brand = request.form.get('brand')
    categories = Category.query.all()
    get_category = request.form.get('category')
    form = AddProductForm()
    edit_product = Product.query.get_or_404(id)
    if request.method == 'POST':
        edit_product.name = form.name.data
        edit_product.price = form.price.data
        edit_product.discount = form.discount.data
        edit_product.stock = form.stock.data
        edit_product.colors = form.colors.data
        edit_product.description = form.description.data
        edit_product.brand_id = request.form.get('brand')
        edit_product.category_id = request.form.get('category')
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + edit_product.image_1))
                edit_product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            except:
                edit_product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + edit_product.image_2))
                edit_product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            except:
                edit_product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + edit_product.image_3))
                edit_product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            except:
                edit_product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        flash(f'Product {edit_product.name}  was updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('.show_products'))
    form.name.data = edit_product.name
    form.price.data = edit_product.price
    form.discount.data = edit_product.discount
    form.stock.data = edit_product.stock
    form.colors.data = edit_product.colors
    form.description.data = edit_product.description
    get_brand = edit_product.brand_id
    get_category = edit_product.category_id
    form.image_1.data = edit_product.image_1
    form.image_2.data = edit_product.image_2
    form.image_3.data = edit_product.image_3
    return render_template('products/edit-product.html', form=form, edit_product=edit_product, brands=brands,
                           categories=categories)


@admin.route('/delete-brand/<int:id>', methods=['POST'])
@login_required
@check_admin
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    flash(f'Brand {brand.name} was deleted', 'success')
    db.session.commit()
    return redirect(url_for('.get_brands'))


@admin.route('/delete-category/<int:id>', methods=['POST'])
@login_required
@check_admin
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    flash(f'Category {category.name} was deleted', 'success')
    db.session.commit()
    return redirect(url_for('.get_categories'))


@admin.route('/delete-product/<int:id>', methods=['POST'])
@login_required
@check_admin
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
    except Exception as e:
        print(e)

    db.session.delete(product)
    flash(f'Category {product.name} was deleted', 'success')
    db.session.commit()
    return redirect(url_for('.show_products'))
