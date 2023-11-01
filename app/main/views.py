from flask import session, render_template, request
from ..models import Product, Brand, Category
from . import main


@main.route('/', methods=['GET'])
def home_page():
    print(session.items())
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=2)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)


@main.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand_id=get_brand.id).paginate(page=page, per_page=2)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories,
                           get_brand=get_brand)


@main.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Product.query.filter_by(category_id=get_cat.id).paginate(page=page, per_page=2)
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return render_template('products/index.html', category=category, categories=categories, brands=brands,
                           get_cat=get_cat)





"""
@main.route('/check1')
def check1():
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        print('Wow')
        return redirect(url_for('.add_brand'))

    else:
        print('Bruh')
"""
